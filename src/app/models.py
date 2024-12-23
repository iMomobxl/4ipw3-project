from django.db import models

class Category(models.Model):
    id_cat = models.AutoField(primary_key=True)
    name_cat = models.CharField(max_length=32)

    class Meta:
        db_table = 't_category'
        managed = False # False si la table est deja creer et manager en dehors de Django

    def __str__(self):
        return self.name_cat

class Article(models.Model):
    id_art = models.AutoField(primary_key=True)
    date_art = models.DateField(null=True, blank=True)
    title_art = models.CharField(max_length=128)
    fk_category_art = models.ForeignKey(Category, db_column='fk_category_art', on_delete=models.CASCADE)
    hook_art = models.TextField(null=True, blank=True)
    image_art = models.CharField(max_length=64, null=True, blank=True)
    content_art = models.TextField()

    class Meta:
        db_table = 't_article'
        managed = False

    def __str__(self):
        return self.title_art




# class Article_Detail(models.Model):
#     id_art = models.AutoField(primary_key=True)
#     date_art = models.DateField(null=True, blank=True)
#     readtime_art = models.IntegerField(null=True, blank=True)
#     title_art = models.CharField(max_length=128)
#     #fk_category_art = models.IntegerField(null=True, blank=True)
#     content_art = models.TextField()
#     image_art = models.CharField(max_length=64, null=True, blank=True)
#
#     class Meta:
#         db_table = 't_article'
#         managed = False
#
#     def __str__(self):
#         return self.title_art