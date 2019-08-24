from django.db import models

class Downloads(models.Model):
    url_id = models.AutoField()
    url = models.CharField()
    media = models.CharField
    download_date = models.DateField()
    download_size = models.ImageField()