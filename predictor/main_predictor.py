from sklearn.ensemble import GradientBoostingRegressor
from sklearn import model_selection
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