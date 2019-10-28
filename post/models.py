from django.db import models
from django.utils import timezone
from django.urls import reverse


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    image = models.ImageField(blank=True, null=True, upload_to='idm_pics')

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': self.pk})