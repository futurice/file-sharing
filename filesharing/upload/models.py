from django.db import models
import hashlib, datetime


class Zip(models.Model):
    filename = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=40)
    date_created = models.DateTimeField(auto_now_add=True)

    def encrypt(self, text):
        h = hashlib.sha1()
        h.update(self.filename)
        h.update(text)
        return h.hexdigest()

    def save(self, *args, **kwargs):
        self.password = self.encrypt(self.password)
        super(Zip, self).save(*args, **kwargs)

    def is_correct(self, passwordAttempt):
        return self.encrypt(passwordAttempt) == self.password
