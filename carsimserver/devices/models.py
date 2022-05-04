from django.db import models
from django.contrib.auth import get_user_model

class Device(models.Model):
    class DeviceType(models.TextChoices):
        CONTROLLER = 'controller'
        MOBILE_DEVICE = 'mobile_device'
        BOT = 'bot'

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    device_type = models.CharField(max_length=20, choices=DeviceType.choices)

    def __str__(self) -> str:
        return "{} - {}".format(self.name, self.device_type)

    def get_device_type(self) -> DeviceType:
        return self.DeviceType[self.device_type]

class Group(models.Model):
    controller = models.ForeignKey(Device, on_delete=models.CASCADE)
    mobile_device = models.ForeignKey(Device, on_delete=models.CASCADE)
    bot = models.ForeignKey(Device, on_delete=models.CASCADE)
