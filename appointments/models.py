from django.db import models
from django.utils import timezone
import uuid

# Create your models here.

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Department(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=80)

    class Meta:
        db_table = 'department'
    
    def __str__(self):
        return self.name
    
class City(models.Model):
    id = models.IntegerField(primary_key=True)
    id_department = models.ForeignKey('Department',  db_column='id_department' ,on_delete=models.PROTECT)
    name = models.CharField(max_length=80)

    class Meta:
        db_table = 'city'
    
    def __str__(self):
        return self.name


class DocumentType(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'document_type'
    def __str__(self):
        return self.name

class PersonType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    class Meta:
        db_table = 'person_type'
    
    def __str__(self):
        return self.name

class Person(models.Model):
    id = models.AutoField(primary_key=True)
    id_type_person = models.ForeignKey('PersonType',  db_column='id_type_person',on_delete=models.PROTECT)
    id_type_doc = models.ForeignKey(DocumentType,  db_column='id_type_doc',on_delete=models.PROTECT)
    identification = models.CharField(max_length=20)
    name = models.CharField(max_length=80)
    lastname = models.CharField(max_length=80)
    phone = models.CharField(blank=True, max_length=20)
    cellphone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    id_depto_address = models.ForeignKey(Department,  db_column='id_depto_address' ,on_delete=models.PROTECT)
    id_city_address = models.ForeignKey(City,  db_column='id_city_address' ,on_delete=models.PROTECT)

    class Meta:
        db_table = 'person'

    def __str__(self):
        return self.name+" "+self.lastname

class Functionary(models.Model):
    id = models.AutoField(primary_key=True)
    id_type_doc = models.ForeignKey(DocumentType, db_column='id_type_doc' ,on_delete=models.PROTECT)
    identification = models.CharField(max_length=20)
    name = models.CharField(max_length=80)
    lastname = models.CharField(max_length=80)
    cellphone = models.CharField(blank=True, max_length=20)
    email = models.CharField(max_length=50)
    id_place = models.ForeignKey('Place',  db_column='id_place', on_delete=models.PROTECT)
    
    def __str__(self):
        return self.name+' '+self.lastname


class Place(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'place'
    def __str__(self):
        return self.name

class Process(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    id_place = models.ForeignKey('Place',  db_column='id_place',on_delete=models.PROTECT)
    id_functionary = models.ForeignKey('Functionary',  db_column='id_functionary', on_delete=models.PROTECT)
    time = models.IntegerField()# tiempo en minutos de atención
    timetable = models.CharField(max_length=5000)#almacena en formato json el horario posible de citas


    class Meta:
        db_table = 'process'
    def __str__(self):
        return self.name
### no se usa ------
class Constraint(models.Model):
    id = models.AutoField(primary_key=True)
    id_process = models.ForeignKey('Process',  db_column='id_process',on_delete=models.PROTECT)
    day = models.IntegerField()
    time = models.IntegerField()
    
    def __str__(self):
        return self.id_process+" - "+self.day+" "+self.time

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'state'
    def __str__(self):
        return self.name
    
class Citation(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=True)
    status = models.CharField(max_length=1, default='A')
    id_person = models.ForeignKey('Person',  db_column='id_person' ,on_delete=models.PROTECT)
    id_process = models.ForeignKey('Process',  db_column='id_process' ,on_delete=models.PROTECT)
    date = models.DateField()
    time = models.TimeField()
    date_creation = models.DateField(default=timezone.now)

class Holiday(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    
    def __str__(self):
        return current_date_format(self.date) 

def current_date_format(date):
    months = ("Enero", "Febrero", "Marzo", "Abri", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre")
    day = date.day
    month = months[date.month - 1]
    year = date.year
    messsage = "{} de {} del {}".format(day, month, year)
    return messsage
