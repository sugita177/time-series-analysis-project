import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import optuna
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

df = pd.read_csv("../file_edit/edited_data.csv")

# 学習データとテストデータの分割
test_length = 365
df_train = df.iloc[:-test_length]
df_test = df.iloc[-test_length:]

# 目的関数の設定（ステップ1）
def objective(trial):
    #ハイパーパラメータの集合を定義する
    params = {'changepoint_prior_scale' : 
                 trial.suggest_uniform('changepoint_prior_scale',
                                       0.001,0.5
                                      ),
              'seasonality_prior_scale' : 
                 trial.suggest_uniform('seasonality_prior_scale',
                                       0.01,10
                                      ),
              'seasonality_mode' : 
                 trial.suggest_categorical('seasonality_mode',
                                           ['additive', 'multiplicative']
                                          )
             }
    #良し悪しを判断するメトリクスを定義する
    m = Prophet(**params)
    m.fit(df_train)
    df_future = m.make_future_dataframe(periods=test_length,freq='D')
    df_pred = m.predict(df_future) 
    preds = df_pred.tail(len(df_test))
    val_rmse = np.sqrt(mean_squared_error(df_test.y, preds.yhat))
    return val_rmse
# 目的関数の最適化を実行する（ステップ2）
study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=100)



model = Prophet(**study.best_params)
model.fit(df)

future = model.make_future_dataframe(periods=365)
forecast = model.predict(future)

fig, ax = plt.subplots(figsize=(10, 6))
model.plot(forecast, ax=ax)

ax.tick_params(axis="x", rotation=90)

plt.show()
