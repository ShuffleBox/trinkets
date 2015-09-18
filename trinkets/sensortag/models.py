from django.db import models
from django.template.defaultfilters import slugify

class SensorTag(models.Model):
    '''
    Define the SensorTags
    '''
    
    mac_address = models.CharField(verbose_name = 'MAC Address', max_length = 17)
    slug = models.SlugField()   
    description = models.TextField()
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.mac_address)
        super(SensorTag, self).save(*args, **kwargs)
    
    @property
    def latest_data(self):
        """
        Latest entry
        """
        latest_reading = self.sensordata_set.latest('time_recorded')
        return latest_reading    
    

class SensorData(models.Model):
    '''
    Data logged
    '''
    sensor = models.ForeignKey(SensorTag)
    time_recorded = models.DateTimeField(auto_now=True)
    ir_temp = models.DecimalField(verbose_name="Infrared Temperature Sensor",
                                  max_digits=5,
                                  decimal_places=2,
                                  null=True)
    ambient_temp = models.DecimalField(verbose_name="Ambient Temperature Sensor",
                                       max_digits=5,
                                       decimal_places=2,
                                       null=True)
    humidity = models.DecimalField(verbose_name="Humidity Sensor",
                                   max_digits=5,
                                   decimal_places=2,
                                   null=True)
    lux = models.DecimalField(verbose_name="Luxometer",
                              max_digits=10,
                              decimal_places=5,
                              null=True)
    class Meta:
        ordering = ['time_recorded']
