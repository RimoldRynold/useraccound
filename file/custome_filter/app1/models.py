from django.db import models



class Mymodel(models.Model):
    distance = models.CharField(max_length=100)
    date = models.DateField()
    name = models.CharField(max_length=100,null=True)
    roll = models.CharField(max_length=100,null=True)
    
    def __str__(self):
        return self.distance
    