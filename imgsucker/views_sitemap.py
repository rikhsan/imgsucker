# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from django.http import Http404  
from django.contrib.auth.models import User
from imgsucker.models import Wallpaper, Category, Tag, Wallpaper_tag, Wallpaper_resoultion, Resolution, User_action, User
from django.core.paginator import Paginator

from django.utils import timezone
import datetime

def wallpaper(request):
	template = loader.get_template('sitemap/wallpaper.xml')
	walls = Wallpaper.objects.filter(post_at__lte=datetime.datetime.now(tz=timezone.utc)).order_by('-post_at')[:100]
	# paginator = Paginator(walls, 100)
	context = {
		'page': 'Sitemap Wallpaper',
		'wallpapers': walls,
    }
	return HttpResponse(template.render(context, request), content_type='text/xml')

def tag(request):
	template = loader.get_template('sitemap/tag.xml')
	tags = Tag.objects.all().order_by('-created_at')[:100]
	# paginator = Paginator(tags, 100)
	context = {
		'page': 'Sitemap Tag',
		# 'tags': paginator.page(1),
		'tags': tags,
    }
	return HttpResponse(template.render(context, request), content_type='text/xml')

def category(request):
	template = loader.get_template('sitemap/category.xml')
	categories = Category.objects.all().order_by('-created_at')[:100]
	# paginator = Paginator(tags, 100)
	context = {
		'page': 'Sitemap Category',
		# 'tags': paginator.page(1),
		'categories': categories,
    }
	return HttpResponse(template.render(context, request), content_type='text/xml')