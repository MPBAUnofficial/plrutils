from django.db import models
from validators import validate_csv


class Database(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name='DB Name',
        help_text='The name of the DB in the settings.py file'
    )

    def __unicode__(self):
        return u'{0}'.format(self.name)

    class Meta(object):
        verbose_name = 'database'
        verbose_name_plural = 'databases'


class GraphFunction(models.Model):
    name = models.CharField(max_length=255, unique=True)
    database = models.ForeignKey(Database)
    params = models.TextField(null=True, blank=True, validators=[validate_csv],
                              help_text='name;type;name;type;...')

    def __unicode__(self):
        return u'{0} on {1}'.format(self.name, self.database.name)

    class Meta(object):
        verbose_name = 'graph function'
        verbose_name_plural = 'graph functions'
