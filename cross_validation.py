from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation, performance_metrics
import pandas as pd

# Assuming df is your DataFrame with columns 'ds' for dates and 'y' for values
# and my_model is your trained Prophet model

# Perform cross-validation
df_cv = cross_validation(my_model, initial='730 days', period='180 days', horizon='365 days')

# Calculate performance metrics
df_p = performance_metrics(df_cv)

# Print Mean Squared Error, Mean Absolute Error, and R-squared
print(df_p[['mse', 'mae', 'r2']].mean())
