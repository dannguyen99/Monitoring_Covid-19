from django.db import models

# Create your models here.


class Table(models.Model):
    csv_file = models.FileField(upload_to='data/upload')

    def __str__(self):
        return self.csv_file.name
