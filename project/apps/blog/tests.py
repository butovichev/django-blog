from datetime import datetime

import pytest
from faker import Faker

from django.contrib.auth.models import User

from project.apps.blog.models import Post, Tag, Category
from project.apps.blog.views import Index


@pytest.fixture
def f():
    return Faker()


@pytest.fixture
def user(db, f):
    return User.objects.create_user(username=f.first_name(),
                                    email=f.email(),
                                    password=f.password())


@pytest.fixture
def category(db, f):
    category = Category(name=f.first_name())
    category.save()
    return category


@pytest.fixture
def tag(db, f):
    tag = Tag(name=f.first_name())
    tag.save()
    return tag


@pytest.fixture
def posts_draft(db, f, user, category, tag):
    posts_draft = {}
    for i in range(5):
        post = Post(author=user,
                    title=f.last_name(),
                    text=f.text(),
                    status='draft',
                    category=category,
                    #media=1,
                    created_date=f.date())
        post.save()
        post.tags.add(tag)
        post.save()
        assert post
        posts_draft[post.id] = post
    return posts_draft


@pytest.fixture
def posts_public(db, f, posts_draft):
    posts_public = {}
    for post_id, post in posts_draft.items():
        post.status = 'public'
        post.public_date = datetime.now()
        post.save()
        posts_public[post.id] = post
    return posts_public


# @pytest.fixture(params=['posts_draft', 'post_public'], scope='function')
# def posts(request):
#     return request.getfixturevalue(request.param)

def test_check_posts_status_draft(posts_draft):
    params = {}
    data = Index().resources(params)
    assert len(data) == 0


def test_check_posts_status_public(posts_public):
    params = {}
    data = Index().resources(params)
    assert len(data) == len(posts_public)

    for post in data:
        assert post['title'] == posts_public[post['id']].title
        assert post['text'] == posts_public[post['id']].text
        assert post['category'] == posts_public[post['id']].category
