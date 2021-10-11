from django.db import models
from django.db.models.base import Model

# Create your models here.

class Article(models.Model):
    author = models.ForeignKey("auth.User",on_delete = models.CASCADE,verbose_name="Yazar")
    title = models.CharField(max_length=50,verbose_name="Başlık")
    content = models.TextField(verbose_name="içerik")
    created_date = models.DateTimeField(auto_now_add=True,verbose_name="oluşturma tarihi")
    def __str__(self):
        return self.title