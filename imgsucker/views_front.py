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
from imgsucker.forms import LoginClientForm, LoginAdminForm, RegisterClientForm, EditClientForm
from imgsucker.decorators import required_client
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from imgsucker import settings

def home(request):
	template = loader.get_template('front/v_home.html')
	walls = Wallpaper.objects.all().order_by('-created_at')
	paginator = Paginator(walls, 16)
	form = LoginClientForm()
	context = {
		'page': 'Home',
		'wallpapers': paginator.page(1),
		'sort': 'date',
		'form': form,
		# 'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))

@login_required
def user(request):
	template = loader.get_template('front/v_user.html')
	context = {
		'page': 'User',
		'likes': User_action.objects.filter(user= request.user, is_liked=1).order_by('-created_at'),
		'favorites': User_action.objects.filter(user= request.user, is_favorited=1).order_by('-created_at'),
		'uploads': Wallpaper.objects.filter(uploader=request.user).order_by('-created_at'),
		# 'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))


def userprofile(request, username):
	user2 = get_object_or_404(User, username=username)
	template = loader.get_template('front/v_userprofile.html')
	context = {
		'page': 'User',
		'user2': user2,
		'likes': User_action.objects.filter(user= user2, is_liked=1).order_by('-created_at'),
		'favorites': User_action.objects.filter(user= user2, is_favorited=1).order_by('-created_at'),
		'uploads': Wallpaper.objects.filter(uploader= user2).order_by('-created_at'),
		# 'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))

@login_required
def useredit(request):
	template = loader.get_template('front/v_useredit.html')
	args= {}
	args['page']= 'Edit User'
	if request.method == 'POST':
		form = EditClientForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
			ne = form.save(commit=False)
			ne.save()
			messages.success(request, 'Edit User successed')
			print('successed')
		else:
			messages.success(request, 'Edit User failed')
			print('failed')
		return redirect('fr_useredit')

	else:
		form = EditClientForm(instance=request.user)
		args['form']= form
	return HttpResponse(template.render(args, request))


def loginclient(request):
	template = loader.get_template('front/login.html')
	args= {}
	args['page']= 'Login'
	if request.method == 'POST':
		form = LoginClientForm(request.POST)
		if form.is_valid():
			# form.save()
			# mcb=MyCustomBackend()
			# if  mcb.authenticateadmin(form.cleaned_data.get('username'),form.cleaned_data.get('password')):
			# print(str(form.cleaned_data.get('email')))
			# print(str(form.cleaned_data.get('password')))
			user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
			if  user:
				next_page = request.GET.get('next', '/')
				login(request, user)
				return HttpResponseRedirect(next_page)

			else:
				messages.error(request, 'Username and password do not match.')
				return redirect('fr_login')
	else:
		form = LoginClientForm()
		args['form']= form
	return HttpResponse(template.render(args, request))
	# return render(request, 'login.html', {'form': form})
	
def needloginclient(request):
	args= {}
	if request.method == 'POST':
		form = LoginClientForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
			next_page = request.GET.get('next', '/')
			if  user:
				login(request, user)
			else:
				messages.error(request, 'Username and password do not match.')
			return HttpResponseRedirect(next_page)
	return HttpResponse(template.render(args, request))


@login_required
def logoutclient(request):
	next_page = request.GET.get('next', '/')
	logout(request)
	return HttpResponseRedirect(next_page)

def registerclient(request):
	args = {}
	template = loader.get_template('front/register.html')
	if request.method == 'POST':
		form = RegisterClientForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Registration successed. Use your username and password for loging in.')
			return redirect('fr_login')
		else:
			args['form'] = form
			# messages.error(request, 'Registration failed. Try again.')

		args['validated'] = True
	else:
		args['form']  = RegisterClientForm()
	
	# return render(request, 'login.html', {'form': form})
	args['page'] = 'Register'
	return HttpResponse(template.render(args, request))

def search(request):
	queryresult=Wallpaper.objects.none()
	query = request.GET.get('query', '')
	page = request.GET.get('page', 1)
	if query:
		# query = request.GET.get('param', '')

		categories = Category.objects.filter(category__contains= query)
		tags = Tag.objects.filter(tag__contains=query)

		# cari full category & tag
		queryresult |= Wallpaper.objects.filter(category__in= categories)
		

		wall_tags= Wallpaper_tag.objects.filter(tag__in = tags)

		wts=[]
		for wt in wall_tags:
			wts.append(wt.wallpaper.id_wallpaper)

		queryresult |= Wallpaper.objects.filter(id_wallpaper__in= wts)


		# queryresult |= Wallpaper.objects.filter(wallpaper__in= categories)

		# cari full category & tag split
		for q in query.split(' '):
			categories_split= Category.objects.filter(category__contains= q)
			tags_split= Tag.objects.filter(tag__contains=q)

			queryresult |= Wallpaper.objects.filter(category__in= categories_split)

			wts2=[]
			wall_tags2= Wallpaper_tag.objects.filter(tag__in = tags_split)
			for wt2 in wall_tags2:
				wts2.append(wt2.wallpaper.id_wallpaper)

			queryresult |= Wallpaper.objects.filter(id_wallpaper__in= wts2)


		# queryresult= sorted(list(set(queryresult)), key=operator.attrgetter('created_at'))


	template = loader.get_template('front/v_search.html')
	paginator = Paginator(queryresult.order_by('-created_at'), 16)
	
	context = {
		'page': 'Search',
		'query': query,
		'wallpapers': paginator.page(page),
		'sort': 'date',
		'form': LoginClientForm(),
    }
	return HttpResponse(template.render(context, request))


def all(request, sort, page):
	template = loader.get_template('front/v_home.html')
	if sort == 'date':
		walls = Wallpaper.objects.all().order_by('-created_at')
	elif sort == 'likes':
		walls = Wallpaper.objects.all().order_by('-likes')
	elif sort == 'downloads':
		walls = Wallpaper.objects.all().order_by('-downloads')
	elif sort == 'views':
		walls = Wallpaper.objects.all().order_by('-views')
	else:
		raise Http404

	paginator = Paginator(walls, 16)
	context = {
		'page': 'Home',
		'wallpapers': paginator.page(page),
		'sort': sort,
		'form': LoginClientForm(),
		# 'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))

def tag(request, tag, sort='date', page='1'):
	# print(tag)
	template = loader.get_template('front/v_tag.html')
	tag_reco = Tag.objects.get(tag=tag.replace('-',' '))
	# print(sort)
	if sort == 'date':
		walls = Wallpaper_tag.objects.filter(tag=tag_reco).order_by('-wallpaper__created_at')
	elif sort == 'likes':
		walls = Wallpaper_tag.objects.filter(tag=tag_reco).order_by('-wallpaper__likes')
	elif sort == 'downloads':
		walls = Wallpaper_tag.objects.filter(tag=tag_reco).order_by('-wallpaper__downloads')
	elif sort == 'views':
		walls = Wallpaper_tag.objects.filter(tag=tag_reco).order_by('-wallpaper__views')
	else:
		raise Http404
	# print(walls)
	paginator = Paginator(walls, 16)
	context = {
		'page': 'Tag',
		'wallpaper_tags': paginator.page(page),
		'sort': sort,
		'tag' : tag_reco,
		'form': LoginClientForm(),
		# 'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))



from pathlib import Path
from PIL import Image
import os 
def image(request, title, id_wall, w, h):
	wallpaper = get_object_or_404(Wallpaper, id_wallpaper=id_wall)
	wallpaper.downloads+=1
	wallpaper.save()
	resss = Resolution.objects.filter(w=w, h=h)
	if not resss:
		raise Http404

	res = resss.first()

	if (wallpaper.wallpaper.width is w) and (wallpaper.wallpaper.height is h):
		filename = str(id_wall)+'.jpg'
	else:
		filename =  str(w)+'x'+ str(h)+'_'+ str(id_wall)+'.jpg'


	img_path= 'media/wallpaper/'+filename
	if not os.path.isfile(img_path):
		img = Image.open('media/'+str(wallpaper.wallpaper))
		print('not available')
		resi_w= res.w
		resi_w_proc= res.w/img.width
		resi_h= int(img.height*resi_w_proc)
		if resi_w<res.w or resi_h<res.h:
			resi_h=res.h
			resi_h_proc= res.h/img.height
			resi_w= int(img.width*resi_h_proc)
		print(str(res.w)+'x'+str(res.h))
		print(str(img.width)+'x'+str(img.height)+'('+str(img.width/img.height)+')'+' => '+str(resi_w)+'x'+str(resi_h)+'('+str(resi_w/resi_h)+')')
		proc_img = img.resize((resi_w, resi_h), Image.ANTIALIAS)
		crop_x= int((resi_w-res.w)/2)
		crop_y= int((resi_h-res.h)/2)
		proc_img.crop((crop_x, crop_y, crop_x+res.w, crop_y+res.h)).save('media/wallpaper/'+str(res.w)+'x'+str(res.h)+'_'+str(wallpaper.id_wallpaper)+'.jpg')

	# print(img_path)
	img = open(img_path, mode='rb').read()
	return HttpResponse(img, content_type="image/jpg")

def category(request, category, sort='date', page='1'):
	print(category)
	template = loader.get_template('front/v_category.html')
	category_reco = Category.objects.get(category=category.replace('-',' '))
	# print(sort)
	if sort == 'date':
		walls = Wallpaper.objects.filter(category=category_reco).order_by('-created_at')
	elif sort == 'likes':
		walls = Wallpaper.objects.filter(category=category_reco).order_by('-likes')
	elif sort == 'downloads':
		walls = Wallpaper.objects.filter(category=category_reco).order_by('-downloads')
	elif sort == 'views':
		walls = Wallpaper.objects.filter(category=category_reco).order_by('-views')
	else:
		raise Http404
	# print(walls)
	paginator = Paginator(walls, 16)
	context = {
		'page': 'Category',
		'wallpapers': paginator.page(page),
		'sort': sort,
		'category' : category_reco,
		'form': LoginClientForm(),
		# 'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))

def color(request, color, sort='date', page='1'):
	template = loader.get_template('front/v_color.html')
	# category_reco = Category.objects.get(id_category=id)
	# print(sort)
	if sort == 'date':
		walls = Wallpaper.objects.filter(colors__contains=color).order_by('-created_at')
	elif sort == 'likes':
		walls = Wallpaper.objects.filter(colors__contains=color).order_by('-likes')
	elif sort == 'downloads':
		walls = Wallpaper.objects.filter(color__contains=color).order_by('-downloads')
	elif sort == 'views':
		walls = Wallpaper.objects.filter(colors__contains=color).order_by('-views')
	else:
		raise Http404
	# print(walls)
	paginator = Paginator(walls, 16)
	context = {
		'page': 'Tag',
		'wallpapers': paginator.page(page),
		'sort': sort,
		'color' : color,
		'form': LoginClientForm(),
		# 'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))

from django.shortcuts import get_object_or_404
from django.db.models import Count

def wallpaper(request, tags, id):

	template = loader.get_template('front/v_wallpaper.html')
	wallpaper = get_object_or_404(Wallpaper, id_wallpaper=id)
	wallpaper.views+= 1
	wallpaper.save()

	is_liked= False
	is_disliked= False
	is_favorited= False

	if request.user.is_authenticated:
		action = User_action.objects.filter(wallpaper=wallpaper, user=request.user)
		if not action:
			User_action(wallpaper=wallpaper, user=request.user).save()

		act = User_action.objects.get(wallpaper=wallpaper, user=request.user)
		is_liked= act.is_liked
		is_disliked= act.is_disliked
		is_favorited= act.is_favorited

	context = {
		'page': 'Single',
		'wallpaper': wallpaper,
		'categories': Category.objects.all(),
		'tags': Tag.objects.all().order_by('?')[:50],
		# 'relatedwalls': Wallpaper.objects.order_by('?')[:6],
		'relatedwalls': getrelatedwallpaper(wallpaper,7, None, None),
		'availableresolutions':availableresolutions(wallpaper),
		'form': LoginClientForm(),
		'is_liked': is_liked,
		'is_disliked': is_disliked,
		'is_favorited': is_favorited,
		# 'admin': User.objects.get(id=request.session['admin']),
	}
	return HttpResponse(template.render(context, request))


def download(request, title, id_wall, w, h):
	template = loader.get_template('front/v_download.html')
	wallpaper = get_object_or_404(Wallpaper, id_wallpaper=id_wall)
	resss = Resolution.objects.filter(w=w, h=h)
	is_original=False
	if not resss:
		is_original=True

	resolution = resss.first()

	max_w=400
	max_h=250
	prosen = 0
	if h <= w:
		prosen = h/max_h
	else:
		prosen = w/max_w
	fix_w= int(w/prosen)
	fix_h= int(h/prosen)

	context = {
		'page': 'Download',
		'wallpaper': wallpaper,
		'categories': Category.objects.all(),
		'resolution':resolution,
		'relatedwalls': getrelatedwallpaper(wallpaper,9, w, h),
		'tags': Tag.objects.all().order_by('?')[:50],
		'w':w,
		'h':h,
		'is_original': is_original,
		'form': LoginClientForm(),
		'wh_thumb': str(fix_w)+'x'+str(fix_h),
	}

	return HttpResponse(template.render(context, request))

from django.db.models import Q
def getrelatedwallpaper(wall, limit, w, h):
	wall_tags= Wallpaper_tag.objects.filter(wallpaper=wall)
	tags = []
	for wt in wall_tags:
		tags.append(wt.tag)

	if w and h:
		print(h)
		related = Wallpaper_tag.objects.filter(~Q(wallpaper = wall)).filter(tag__in= tags, wallpaper__height__gte=h, wallpaper__width__gte=w).order_by('?').values('wallpaper').distinct()[:limit]
	else:
		related = Wallpaper_tag.objects.filter(~Q(wallpaper = wall)).filter(tag__in= tags).order_by('?').values('wallpaper').distinct()[:limit]
	ar_rw=[]
	for rw in related:
		ar_rw.append(rw['wallpaper'])

	related_walls= Wallpaper.objects.filter(id_wallpaper__in= ar_rw)
	# for rel in related:
	# 	related_walls.append(rel.wallpaper)
	return related_walls



def getrelatedtags(wall, limit):
	wall_tags= Wallpaper_tag.objects.filter(wallpaper=wall)
	tags = []
	for wt in wall_tags:
		tags.append(wt.tag)

	related = Wallpaper_tag.objects.filter(~Q(wallpaper = wall)).filter(tag__in= tags).order_by('?').values('tag').distinct()[:limit]
	ar_tg=[]
	for tg in related:
		ar_tg.append(tg['tag'])

	related_tags= Tag.objects.filter(id_tag__in= ar_tg)
	return related_tags
	
def availableresolutions(wall):
	available_ress= Resolution.objects.filter(w__lte=wall.wallpaper.width, h__lte=wall.wallpaper.height).order_by('h', 'w', 'resolution', 'category')
	av={}

	for re in available_ress:
		if re.category not in av:
			av[re.category]={}
		if str(re.w)+'x'+str(re.h) not in av[re.category]:
			av[re.category][str(re.w)+'x'+str(re.h)]=[]

		av[re.category][str(re.w)+'x'+str(re.h)].append(re)

	# print(av)
	return av

@login_required
def ajaxuseraction(request):
	wall = Wallpaper.objects.get(id_wallpaper=request.POST['id_wallpaper'])
	action = User_action.objects.get(wallpaper= wall, user=request.user)
	print(request.POST)
	is_liked = request.POST.get('is_liked', '')
	is_disliked = request.POST.get('is_disliked', '')
	is_favorited = request.POST.get('is_favorited', '')
	is_min_like = request.POST.get('is_min_like', '')
	is_min_dislike = request.POST.get('is_min_dislike', '')

	if is_liked:
		action.is_liked = int(is_liked)
		action.is_disliked = 0
		wall.likes += (1 if int(is_liked) else -1)
		if is_min_dislike:
			wall.dislikes -= int(is_min_dislike)
	
	if is_disliked:
		action.is_disliked = int(is_disliked)
		action.is_liked = 0
		wall.dislikes += (1 if int(is_disliked) else -1)
		if is_min_like:
			wall.likes -= int(is_min_like)

	if is_favorited:
		action.is_favorited = is_favorited
		wall.favorites += (1 if is_favorited else -1)

	action.save()
	wall.save()
	response_data = {}
	response_data= {
		'is_saved': True, 
		'id_wallpaper': action.wallpaper.id_wallpaper,
		'id_user': request.user.id,
		'is_liked': action.is_liked,
		'is_disliked': action.is_disliked,
		'is_favorited':action.is_favorited ,

	}
	return JsonResponse(response_data)