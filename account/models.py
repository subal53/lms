from django.db import models

# Create your models here.
class Student(models.Model):
    sid = models.IntegerField(primary_key=True,null=False)
    name = models.CharField(max_length=30)
    roll = models.IntegerField()
    dept = models.CharField(max_length=10)
    reg = models.CharField(max_length=10,unique=True)
    address = models.CharField(max_length=50)
    phone_no = models.CharField(max_length=12)
    password=models.CharField(max_length=150)
    checked = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    checked_by = models.CharField(max_length=20, default="")


    def __str__(self):
        return self.name
    

    class Meta:
        db_table = 'Student'
    


class Librarian(models.Model):
    uid = models.IntegerField(primary_key=True,null=False)
    name = models.CharField(max_length=30)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=30,unique=True)
    phone_no = models.CharField(max_length=12)


    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Librarian'


  



