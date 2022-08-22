from django.db import models


class GDP(models.Model):
    country = models.CharField(max_length=100)
    country_code = models.CharField(max_length=4)
    year = models.PositiveSmallIntegerField()
    gdp = models.FloatField()

    def __str__(self) -> str:
        return self.country
