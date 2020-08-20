from sklearn.ensemble import GradientBoostingRegressor
from sklearn import model_selection
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from catboost import CatBoostRegressor
import pandas as pd


def simple_pipeline(dataframe):
    scoring = []
    n_trees = [1] + list(range(10, 155, 5))

    X = dataframe[['model', 'year', 'mileage', 'body_type', 'fuel_type',
             'engine_volume', 'drive', 'engine_power', 'gearbox']]
    y = dataframe['price'].apply(lambda x: x * 0.001)
    cat_columns = ['body_type', 'fuel_type', 'drive', 'gearbox']
    new_X = pd.get_dummies(X, columns=cat_columns)

    for n_tree in n_trees:
        #     estimator = xgb.XGBRegressor( n_estimators=n_tree)
        estimator = GradientBoostingRegressor(n_estimators=n_tree, max_depth=50)
        score = model_selection.cross_val_score(estimator, new_X, y,
                                                scoring='neg_mean_absolute_error', cv=5, n_jobs=-1)
        scoring.append(score.mean())

    print(scoring)


def catboost_pipeline(filename = './database/mazda2.csv'):
    data = pd.read_csv(filename)
    car_data = data.dropna(axis=1)
    car_data['age'] = car_data.year.apply(lambda x: 2020 - x)
    car_data.drop(axis=1, columns=['Unnamed: 0', 'year', 'url', 'id'], inplace=True)

    distinct_cars = car_data.drop(axis=1, columns=['age', 'mileage', 'price'])
    distinct_cars.drop_duplicates(inplace=True, ignore_index=True)
    distinct_cars['model_id'] = pd.Series(data=list(range(distinct_cars.shape[0])))

    join_on = list(distinct_cars.columns)[:-1]
    merged_data = car_data.merge(distinct_cars, on=join_on)

    merged_data['counts'] = merged_data.model_id.apply(lambda x: merged_data.model_id.value_counts()[x])
    merged_data.drop(axis=0, index=merged_data[merged_data.counts <= 10].index, inplace=True)

    X = merged_data.drop(axis=1, columns=['brand',
                                          'model',
                                          'body_type',
                                          'fuel_type',
                                          'engine_volume',
                                          'drive',
                                          'engine_power',
                                          'gearbox',
                                          'counts'])
    y = X.price
    X.drop(axis=1, columns=['price'], inplace=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    regressor = CatBoostRegressor(learning_rate=1, depth=6, loss_function='RMSE')
    regressor.fit(X_train, y_train, cat_features=['model_id']);
    y_pred = regressor.predict(X_test)
    print(mean_absolute_error(y_test, y_pred))