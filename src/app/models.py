from django.db import models

class Category(models.Model):
    id_cat = models.AutoField(primary_key=True)
    name_cat = models.CharField(max_length=255)

    class Meta:
        db_table = 't_category'
        managed = False # If the table is already created and managed outside Django

    def __str__(self):
        return self.name_cat