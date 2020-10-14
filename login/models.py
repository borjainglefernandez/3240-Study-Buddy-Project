from django.db import models

# Create your models here.
class Course(models.Model):
    idNumber = models.PositiveSmallIntegerField(primary_key=True)
    mnemonic = models.CharField(max_length=4)
    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return str(self.mnemonic) + " " + str(self.number) + " " + str(self.title)