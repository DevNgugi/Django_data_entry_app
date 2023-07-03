from django.db import models

class Data(models.Model):
    category=models.CharField(max_length=50)
    data=models.JSONField()
    
    def __str__(self):
        return self.category
    
