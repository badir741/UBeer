from django.db import models
from django.contrib.auth.models import User


class Establishments(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    address = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=5)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=2)

    image = models.ImageField(default='/static/images/establishment_icon.png', upload_to='media/gallery')
    name = models.CharField(max_length=255, default="{NAME}")
    rating = models.IntegerField(default=-1)
    info = models.CharField(max_length=255, default="{INFO}")
    ride_time = models.IntegerField(default=-1)
    minimum_tab = models.IntegerField(default=-1)

    # def save(self, *args, **kwargs):
    #     try:
    #         int(self.zip_code)
    #     except ValueError:
    #         raise Exception("Invalid value for zip_code")
    #
    #     if self.minimum_tab < 0:
    #         raise Exception("Invalid value for minimum_tab")
    #
    #     super(Establishments, self).save(self, *args, *kwargs)


class Riders(models.Model):
    user = models.ForeignKey(User, on_delete=None)


class Trips(models.Model):
    RIDE_CHOICES = (
        ("R", "Reserved"),  # Tab has been reserved
        ("A", "Arrived"),   # Rider has arrived
        ("C", "Complete")   # Trip is complete
    )

    rider = models.ForeignKey(Riders, on_delete=None)
    establishment = models.ForeignKey(Establishments, on_delete=None)
    tab = models.FloatField()
    status = models.CharField(choices=RIDE_CHOICES, max_length=4)

    def save(self, *args, **kwargs):
        if self.tab < self.establishment.minimum_tab:
            raise Exception("Tab must be greater than or equal to establishment.minimum_tab")

        super(Trips, self).save(self, *args, *kwargs)


class Transactions(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    total = models.FloatField()
    date = models.DateTimeField()
