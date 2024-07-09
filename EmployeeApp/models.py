from django.db import models
import uuid

class Ticket(models.Model):
    # tid = models.UUIDField(primary_key=True,default=uuid.uuid4,max_length=6)  # Auto-generated primary key
    tid = models.CharField(max_length=10)
    assigned_to = models.IntegerField()
    assigned_by = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"Ticket {self.tid}"


from django.db import models

class Employee(models.Model):
    userid = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    # tid = models.IntegerField()
    # tid = models.UUIDField(primary_key=True,default=uuid.uuid4,max_length=6)  # Auto-generated primary key
    tid = models.CharField(max_length=10)


    def __str__(self):
        return self.username








