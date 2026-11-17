from django.contrib.gis.db import models


class Facility(models.Model):
    SCHOOL = "school"
    HEALTH = "health"
    WATER = "water"
    OTHER = "other"
    KIND_CHOICES = [
        (SCHOOL, "School"),
        (HEALTH, "Health"),
        (WATER, "Water"),
        (OTHER, "Other"),
    ]

    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES, default=OTHER)
    added = models.DateTimeField(auto_now_add=True)
    geom = models.PointField(srid=4326)

    class Meta:
        verbose_name_plural = "facilities"
        ordering = ["-added"]

    def __str__(self):
        return self.name
