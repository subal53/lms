from django.db import models
from account.models import *

# Create your models here.
class Book(models.Model):
    bid = models.IntegerField(primary_key=True,null=False)
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=20)
    short_desc = models.CharField(max_length=50)
    quantity = models.IntegerField(null=False)
    issue = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    def add(self, qunt):
        self.quantity += qunt

    def req(self):
        self.quantity -= 1
        self.issue += 1
    
    def close(self):
        self.quantity += 1
        self.issue -= 1

    class Meta:
        db_table = 'Book' 

class issue(models.Model):
    bid = models.CharField(max_length=5)
    sid = models.CharField(max_length=5)
    uid = models.CharField(max_length=5,null=True)
    req_date = models.DateTimeField()
    issue_date = models.DateField(null=True)
    return_date = models.DateField(null=True)
    close_date = models.DateTimeField(null=True)
    actions = models.CharField(max_length=1, default='0')

    def __str__(self):
        return self.sid
    
    class Meta:
        db_table = 'issue'