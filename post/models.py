from django.db import models
from django.utils import timezone

# MAX_UPLOAD_SIZE = settings.MAX_UPLOAD_SIZE
# ALLOWED_EXTENSIONS = settings.ALLOWED_EXTENSION


class PostManager(models.Manager):

    def new_thread(self, post_data, file_data):

        errors = []

        #     TODO: add errors for starting a thread : image and yada yada

        if len(errors) < 1:
            return Post.objects.create(
                content=post_data['content'],
                image=file_data['image'],
                image_name=post_data['image_name'],
                is_thread=True,
                is_sage=False,
            )
        else:
            return errors

    def new_reply(self, post_data, file_data, post_id):

        errors = []

        #     TODO: add errors for starting a thread : image and yada yada
        # TODO: sage
        if len(errors) < 1:
            post = Post.objects.create(
                content=post_data['content'],
                image_name=None if "image" not in file_data else post_data['image_name'],
                image=None if "image" not in file_data else file_data["image"],
                is_thread=False,
                is_sage=False,
            )
            thread = Post.objects.get(id=post_id)
            thread.replies.add(post)
            if not post.is_sage:
                thread.updated_at = timezone.now()
                thread.save()
            return post
        else:
            return errors


class Post(models.Model):
    content = models.TextField(max_length=2000)
    date_posted = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, null=True, upload_to='idm_pics')
    image_name = models.CharField(max_length=255, default=None, blank=True, null=True)
    is_thread = models.BooleanField()
    is_sage = models.BooleanField()
    replies = models.ManyToManyField("self", blank=True, related_name="thread")

    objects = PostManager()

    def __str__(self):
        return str(self.id)
