from django.db import models


class Mode(models.Model):
    Name = models.CharField(max_length=30, primary_key=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Name

    def to_dict(self):
        return dict(Name=self.Name, updated_at=self.updated_at.isoformat())


class Region(models.Model):
    Name = models.CharField(max_length=30, primary_key=True, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Name

    def to_dict(self):
        return dict(Name=self.Name, updated_at=self.updated_at.isoformat())


class Link(models.Model):
    Mode = models.ForeignKey(Mode, on_delete=models.CASCADE)
    Region = models.ForeignKey(Region, on_delete=models.CASCADE)
    Link = models.URLField()
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Link

    def to_dict(self):
        return dict(Link=self.Link, updated_at=self.updated_at.isoformat())


class Readings(models.Model):
    Mode = models.ForeignKey(Mode, on_delete=models.CASCADE)
    Region = models.ForeignKey(Region, on_delete=models.CASCADE)
    Year = models.IntegerField()
    JAN = models.FloatField(null=True, blank=True)
    FEB = models.FloatField(null=True, blank=True)
    MAR = models.FloatField(null=True, blank=True)
    APR = models.FloatField(null=True, blank=True)
    MAY = models.FloatField(null=True, blank=True)
    JUN = models.FloatField(null=True, blank=True)
    JUL = models.FloatField(null=True, blank=True)
    AUG = models.FloatField(null=True, blank=True)
    SEP = models.FloatField(null=True, blank=True)
    OCT = models.FloatField(null=True, blank=True)
    NOV = models.FloatField(null=True, blank=True)
    DEC = models.FloatField(null=True, blank=True)
    WIN = models.FloatField(null=True, blank=True)
    SPR = models.FloatField(null=True, blank=True)
    SUM = models.FloatField(null=True, blank=True)
    AUT = models.FloatField(null=True, blank=True)
    ANN = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.Year

    def to_dict(self):
        return dict(
            Year=self.Year, JAN=self.JAN, FEB=self.FEB, MAR=self.MAR, APR=self.APR, MAY=self.MAY,
            JUN=self.JUN, JUL=self.JUL, AUG=self.AUG, SEP=self.SEP, OCT=self.OCT, NOV=self.NOV,
            DEC=self.DEC, WIN=self.WIN, SPR=self.SPR, SUM=self.SUM, AUT=self.AUT, ANN=self.ANN,
            updated_at=self.updated_at.isoformat())


class Kudos(models.Model):
    count = models.IntegerField(default=1)

    def __unicode__(self):
        return self.count


def add_kudos():
    default_kwargs = {
        'count': '1'
    }
    Kudos.objects.create(**default_kwargs)


def get_kudos():
    return Kudos.objects.all().count()
