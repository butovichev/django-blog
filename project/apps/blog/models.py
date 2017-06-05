from django.db.models import (
    Model,
    ForeignKey,
    CharField,
    TextField,
    DateField,
    ImageField,
    ManyToManyField,
)
from django.utils import timezone


class Post(Model):
    STATUS_CHOICES = (
        ('draft', 'draft'),
        ('public', 'public'),
        ('delete', 'delete')
    )

    author = ForeignKey('auth.User')

    title = CharField(max_length=200)

    index_url = CharField(max_length=256, blank=True)

    description = TextField(blank=True)

    text = TextField()

    created_date = DateField(default=timezone.now)

    public_date = DateField(blank=True)

    status = CharField(choices=STATUS_CHOICES, default='draft', max_length=10)

    tags = ManyToManyField('Tag', related_name='tags_post')

    category = ForeignKey('Category', null=True)

    media = ImageField(upload_to='media/%Y/%m/%d',
                       null=True,
                       blank=True,
                       help_text="Upload your photo for post")

    def public_at(self):
        if self.status == 'public':
            self.public_date = timezone.now
            self.save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Detail Post'
        verbose_name_plural = 'Posts'
        # ordering = ["-public_date"]


class Tag(Model):
    name = CharField(max_length=256)

    def __str__(self):
        return self.name


class Category(Model):
    name = CharField(max_length=256)

    def __str__(self):
        return self.name
