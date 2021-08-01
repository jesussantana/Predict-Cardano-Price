# Light GBM Regresor Hyperparameter Tunning Grid Search
################################################################


####################################
#  Libraries
####################################
import pandas as pd
import multiprocessing
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error
from lightgbm import LGBMRegressor


####################################
# Grid Search & LGBM
#################################### 

def modeling(X_train, y_train, X_test, y_test, name):
    
    # Grid of evaluated hyperparameters
    # ==============================================================================
    param_grid = {'n_estimators'     : [100, 500, 1000, 5000],
                'max_depth'        : [-1, 1, 3, 5, 10, 20],
                'subsample'        : [0.5, 1],
                'learning_rate'    : [0.001, 0.01, 0.1],
                'boosting_type'    : ['gbdt']
                }

    # Search by grid search with cross validation
    # ==============================================================================
    grid = GridSearchCV(
            estimator  = LGBMRegressor(random_state=1234),
            param_grid = param_grid,
            scoring    = 'neg_root_mean_squared_error',
            n_jobs     = multiprocessing.cpu_count() - 1,
            cv         = RepeatedKFold(n_splits=3, n_repeats=1, random_state=1234), 
            refit      = True,
            verbose    = 0,
            return_train_score = True
        )

    grid.fit(X = X_train, y = y_train)

    # Results
    # ==============================================================================
    resultados = pd.DataFrame(grid.cv_results_)
    
    results = resultados.filter(regex = '(param.*|mean_t|std_t)') \
    .drop(columns = 'params') \
    .sort_values('mean_test_score', ascending = False) \
    .head(4)
    
    
    #resultados.to_csv(f'../notebooks/models/results/{name}.csv', index = False)
    
    # Better hyperparameters by cross-validation
    # ==============================================================================
    print("----------------------------------------")
    print("Best hyperparameters found (cv)")
    print("----------------------------------------")
    print(grid.best_params_, ":", grid.best_score_, grid.scoring)

    # Final model test error
    # ==============================================================================   
    modelo_final = grid.best_estimator_
    predicciones = modelo_final.predict(X = X_test,)
    rmse = mean_squared_error(
            y_true  = y_test,
            y_pred  = predicciones,
            squared = False
        )
    modelo_final.fit(X = X_train, y = y_train)
    r_squared = modelo_final.score(X_test, y_test)

    print(f"The test error (r2) is: {r_squared}")
    print(f"The test error (rmse) is: {rmse}")
    
    return resultados, results