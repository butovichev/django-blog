from django.views.generic import View
from django.shortcuts import render
from django.utils import timezone
from django.http import HttpResponse, Http404, HttpResponseForbidden

from .models import Post, Tag
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



# redis = Redis(host='redis', port=6379)


class Index(View):
    template_name = 'index.html'

    def get(self, request):
        params = self.check_data_request(request)
        data = self.resource(params)
        return render(request, self.template_name, {'posts': data})

    def check_data_request(self, request):
        return {}

    def resource(self, params):
        data = []
        posts = Post.objects.filter(status='public')

        paginator = Paginator(posts, 2)
        for post in posts[:10]:
            data.append({
                'id': post.id,
                'author': post.author,
                'title': post.title,
                'text': post.text,
                'tags': [tag.name for tag in post.tags.all()],
                'category': post.category,
                'media': post.media,
                'public_date': post.public_date,
                'description': post.description,
                'index_url': post.index_url,
            })
        return {
            'data': data,
            'pagination': {
                'range': list(range(1, paginator.num_pages + 1)),
                'current_page': 1,
            }
        }


class PostView(View):
    template_name = 'post.html'

    def check_data_request(self, request, ):
        pass

    def get(self, request, index_url):
        params = self.check_data_request(request)
        data = self.resource(params, index_url)
        return render(request, self.template_name, {'posts': data})

    def resource(self, params, index_url):
        post = Post.objects.filter(index_url=index_url)

        if not post:
            raise Http404
        else:
            return post


class PostsList(View):
    template_name = 'index.html'

    def check_data_request(self, request, ):
        pass

    def get(self, request, page):
        data = self.resource(page)
        return render(request, self.template_name, {'posts': data})

    def resource(self, page):
        posts = Post.objects.filter(status='public')

        paginator = Paginator(posts, 2)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)

        return {
            'data': posts,
            'pagination': {
                'range': list(paginator.page_range),
                'current_page': int(page),
            }
        }
