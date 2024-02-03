# models.py
from django.db import models

class User(models.Model):
    username = models.CharField(max_length=255)
    # Add more user fields as needed
# models.py
from django.db import models


class Form(models.Model):
    id = models.CharField(primary_key=True, max_length=24) 
    #id = models.AutoField(primary_key=True)
    form_name = models.CharField(max_length=255)
    questions = models.JSONField()
    # Add more form fields as needed

class Response(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    responses = models.JSONField()
    # Add more response fields as needed
