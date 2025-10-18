from django.db import models


class Email(models.Model):
    
    subject = models.CharField(max_length=255),
    sender = models.CharField(max_length=255),
    snippet = models.TextField()

    def __str__(self):
        return f"{self.subject} from {self.sender}"
    
class msg(models.Model):
    msg_id = models.CharField(max_length=255)

    def __str__(self):
        return self.msg_id