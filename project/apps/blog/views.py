from django.views.generic import View
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseForbidden

from .models import Post, Tag


# redis = Redis(host='redis', port=6379)


class Index(View):
    template_name = 'home.html'

    def get(self, request):
        params = self.check_data_request(request)
        data = self.resources(params)
        return render(request, self.template_name, {'posts': data})

    def check_data_request(self, request):
        print(request)

    def resources(self, params):
        data = []
        posts = Post.objects.filter(status='public')[:10]
        for post in posts:
            data.append({
                'author': post.author,
                'title': post.title,
                'text': post.text,
                'tags': [tag.name for tag in post.tags.all()],
                'category': post.category,
                'media': post.media,
            })
        return data


class Post1(View):
    template_name = 'home.html'

    def get(self, request, title):
        post = Post.objects.filter(title=title)

        if not post:
            raise Http404

        return render(request, self.template_name, {'posts': post})
        # try:
        #     pk = int(pk)
        #     post = models.Post.objects.get(pk=pk)
        # except models.Post.DoesNotExist:
        #     raise Http404
        # data = {'post':post}
        # tags = post.tags.all()
        # data['tags'] = tags
