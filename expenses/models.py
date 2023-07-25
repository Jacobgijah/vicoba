from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now   
from django.core.validators import MaxValueValidator, MinValueValidator
from .ml_models.loan_prediction import preprocessor_data
import joblib, numpy as np, pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the trained model    
ml_model = joblib.load('expenses/ml_models/defaulters.pkl')

class Loan(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(1000), MaxValueValidator(100000)], null=True)
    date = models.DateField(default=now, null=True)
    description = models.TextField()
    category = models.CharField(max_length=266)
    age = models.FloatField(validators=[MinValueValidator(18), MaxValueValidator(65)], null=True)
    income = models.FloatField(validators=[MinValueValidator(1000)], null=True)
    profession = models.TextField(null=True)
    experience = models.FloatField(validators=[MinValueValidator(1)], null=True)
    marital = models.CharField(max_length=266)
    house = models.CharField(max_length=266)
    car = models.CharField(max_length=266)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=100, blank=True)
    

    def save(self, *args, **kwargs):
         # Define the preprocessor for one-hot encoding categorical features
        categorical_features = ["profession", "marital", "house", "car"]
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])

        # Create the column transformer to apply the preprocessing to the appropriate columns
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, categorical_features)
            ]
        )
        
        # Convert the numerical features into a numpy array
        features = np.array([
            self.amount,
            self.age,
            self.income,
            self.experience
        ])

        # Create the data dictionary with column names as keys and the corresponding values from args
        data_dict = {
            'profession': [self.profession],
            'marital': [self.marital],
            'house': [self.house],
            'car': [self.car]
        }

        # Convert the data dictionary to a pandas DataFrame
        data = pd.DataFrame(data_dict)

        # Process the data using the preprocessor
        processed_data = preprocessor.fit_transform(data)

        # Combine the numerical and one-hot encoded features
        processed_data = np.hstack([features.reshape(1, -1), processed_data])

        # Make predictions using the model
        prediction = ml_model.predict(processed_data)

        # Assign the prediction to the 'prediction' field of the model
        self.prediction = prediction[0]

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']
    
    
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Marital(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class House(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Car(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name