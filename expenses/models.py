from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler

# Load the trained model
pipeline = joblib.load("expenses/ml_models/pipeline_model.pkl")


class Loan(models.Model):
    prof_choices = [
        ("Mechanical_engineer", "MECHANICAL_ENGINEER"),
        ("Software_Developer", "SOFTWARE_DEVELOPER"),
        ("Technical_writer", "TECHNICAL_WRITER"),
        ("Civil_servant", "CIVIL_SERVANT"),
        ("Librarian", "LIBRARIAN"),
        ("Economist", "ECONOMIST"),
        ("Flight_attendant", "FLIGHT_ATTENDANT"),
        ("Architect", "ARCHITECT"),
        ("Designer", "DESIGNER"),
        ("Physician", "PHYSICIAN"),
        ("Financial_Analyst", "FINANCIAL_ANALYST"),
        ("Air_traffic_controller", "AIR_TRAFFIC_CONTROLLER"),
        ("Politician", "POLITICIAN"),
        ("Police_officer", "POLICE_OFFICER"),
        ("Artist", "ARTIST"),
        ("Surveyor", "SURVEYOR"),
        ("Design_Engineer", "DESIGN_ENGINEER"),
        ("Chemical_engineer", "CHEMICAL_ENGINEER"),
        ("Hotel_Manager", "HOTEL_MANAGER"),
        ("Dentist", "DENTIST"),
        ("Comedian", "COMEDIAN"),
        ("Biomedical_Engineer", "BIOMEDICAL_ENGINEER"),
        ("Graphic_Designer", "GRAPHIC_DESIGNER"),
        ("Computer_hardware_engineer", "COMPUTER_HARDWARE_ENGINEER"),
        ("Petroleum_Engineer", "PETROLEUM_ENGINEER"),
        ("Secretary", "SECRETARY"),
        ("Computer_operator", "COMPUTER_OPERATOR"),
        ("Chartered_Accountant", "CHARTERED_ACCOUNTANT"),
        ("Technician", "TECHNICIAN"),
        ("Microbiologist", "MICROBIOLOGIST"),
        ("Fashion_Designer", "FASHION_DESIGNER"),
        ("Aviator", "AVIATOR"),
        ("Psychologist", "PSYCHOLOGIST"),
        ("Magistrate", "MAGISTRATE"),
        ("Lawyer", "LAWYER"),
        ("Firefighter", "FIREFIGHTER"),
        ("Engineer", "ENGINEER"),
        ("Official", "OFFICIAL"),
        ("Analyst", "ANALYST"),
        ("Geologist", "GEOLOGIST"),
        ("Drafter", "DRAFTER"),
        ("Statistician", "STATISTICIAN"),
        ("Web_designer", "WEB_DESIGNER"),
        ("Consultant", "CONSULTANT"),
        ("Chef", "CHEF"),
        ("Army_officer", "ARMY_OFFICER"),
        ("Surgeon", "SURGEON"),
        ("Scientist", "SCIENTIST"),
        ("Civil_engineer", "CIVIL_ENGINEER"),
        ("Industrial_Engineer", "INDUSTRIAL_ENGINEER"),
        ("Technology_specialist", "TECHNOLOGY_SPECIALIST"),
    ]

    amount = models.FloatField(
        validators=[MinValueValidator(1000), MaxValueValidator(100000)]
    )
    date = models.DateField(default=now)
    description = models.TextField()
    category = models.CharField(max_length=266)
    age = models.FloatField(validators=[MinValueValidator(18), MaxValueValidator(65)])
    income = models.FloatField(validators=[MinValueValidator(1000)])
    profession = models.CharField(max_length=50, choices=prof_choices)
    experience = models.FloatField(validators=[MinValueValidator(1)])
    marital = models.CharField(max_length=266)
    house = models.CharField(max_length=266)
    car = models.CharField(max_length=266)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    prediction = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Create the data dictionary with column names as keys and the corresponding values from args
        data_dict = {
            "Id": [1],
            "Income": [int(self.income)],
            "Age": [int(self.age)],
            "Experience": [int(self.experience)],
            "Married/Single": [self.marital],
            "House_Ownership": [self.house],
            "Car_Ownership": [self.car],
            "Profession": [self.profession],
            "CITY": [2],
            "STATE": [3],
            "CURRENT_JOB_YRS": [4],
            "CURRENT_HOUSE_YRS": [5],
        }
        # data = {
        #     "Id",
        #     "Income",
        #     "Age",
        #     "Experience",
        #     "Married/Single",
        #     "House_Ownership",
        #     "Car_Ownership",
        #     "Profession",
        #     "CITY",
        #     "STATE",
        #     "CURRENT_JOB_YRS",
        #     "CURRENT_HOUSE_YRS",
        # }
        print(data_dict)
        # Convert the data dictionary to a pandas DataFrame
        data = pd.DataFrame(data_dict)

        # Make predictions using the model
        predictions = pipeline.predict(data)

        # Assign the prediction to the 'prediction' field of the model
        print(f"The predictions are: {predictions}")
        if predictions[0] == 0:
            self.prediction = "Elligible for a loan"
        elif predictions[0] == 1:
            self.prediction = "Not Elligible for a Loan"
        # self.prediction = predictions[0]
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ["-date"]


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "Categories"

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
