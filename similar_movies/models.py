from django.db import models

# Create your models here.

class YTS(models.Model):
	movie_id = models.IntegerField()
	imdb_code = models.CharField(max_length=15)
	title = models.TextField()
	title_english = models.TextField()
	year = models.IntegerField()
	rating = models.FloatField()
	runtime = models.IntegerField()
	genres = models.TextField()
	description = models.TextField()
	language = models.CharField(max_length=20)
	mpa_rating = models.CharField(max_length=10)

	def __str__(self):
		return self.movie_id
	def save(self,*args,**kwargs):
		super().save(*args,**kwargs)
