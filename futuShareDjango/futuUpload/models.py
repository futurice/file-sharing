from django.db import models
from settings import PASSWORD_LENGTH, SECRET_KEY
import hashlib, datetime


class Zip(models.Model):
  filename = models.CharField(max_length=20, primary_key=True)
  password = models.CharField(max_length=40)
  date_created = models.DateTimeField()

  def encrypt(self, text):
    h = hashlib.sha1()
    h.update(SECRET_KEY)
    h.update(text)
    return h.hexdigest()

  def save(self, *args, **kwargs):
    self.password = self.encrypt(self.password)
    self.date_created = datetime.datetime.today()
    super(Zip, self).save(*args, **kwargs)

  def isCorrectPassword(self, passwordAttempt):
    return self.encrypt(passwordAttempt) == self.password
