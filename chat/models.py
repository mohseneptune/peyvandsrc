from django.db import models
from django.contrib.auth import get_user_model
from account.choices import RELATION_CHOICES


User = get_user_model()

class Relation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", verbose_name='فرستنده')
    reciver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reciver", verbose_name='گیرنده')
    status = models.CharField(max_length=1, choices=RELATION_CHOICES)
    created_at = models.DateTimeField("تاریخ ثبت درخواست", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ ویرایش", auto_now=True)

    def __str__(self):
        return self.status

    class Meta:
        db_table = 'relations'
        managed = True
        verbose_name = 'رابطه'
        verbose_name_plural = 'رابطه ها'


class Room(models.Model):
    name = models.CharField(max_length=255)
    relation = models.OneToOneField(Relation, on_delete=models.CASCADE)
    members = models.ManyToManyField(User)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'rooms'
        managed = True
        verbose_name = 'اتاق'
        verbose_name_plural = 'اتاق ها'


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'messages'
        managed = True
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'
        ordering = ('date_added',)