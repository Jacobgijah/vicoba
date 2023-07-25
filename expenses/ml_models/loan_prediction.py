import joblib, pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

def preprocessor_data(*args, **kwargs):   
    # Create a dictionary with column names as keys and the corresponding values from args
    data_dict = {
        'profession': [args[0]],
        'marital': [args[1]],
        'house': [args[2]],
        'car': [args[3]],
        'age': [args[4]],
        'income': [args[5]],
        'experience': [args[6]]
    }

    # Convert the data dictionary to a pandas DataFrame
    data = pd.DataFrame.from_dict(data_dict)
    
    # Define the preprocessor for one-hot encoding categorical features
    categorical_features = ["marital", "house", "car"]
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Create the column transformer to apply the preprocessing to the appropriate columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', categorical_transformer, categorical_features)
        ]
    )
    
    # Fit and transform the data using the preprocessor
    processed_data = preprocessor.fit_transform(data)
    
    return processed_data

