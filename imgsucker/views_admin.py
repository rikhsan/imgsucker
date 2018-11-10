# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import datetime
from imgsucker.forms import LoginAdminForm, GrabForm, ModelWallpaperForm
from django.contrib.auth import authenticate
from django.contrib import messages
from imgsucker.decorators import required_admin
# from django.contrib.auth.models import User
from django.http import JsonResponse
from imgsucker.models import Tag, Wallpaper_tag, Wallpaper, Resolution, Wallpaper_resoultion, Word, User, Category
from urllib.parse import urlparse
from imgsucker import settings
from datetime import timedelta
from django.utils import timezone

def suckimage(request):
    return HttpResponse('<h1>Page was found</h1>')

def login(request):
	template = loader.get_template('admin2/login.html')
	if request.method == 'POST':
		form = LoginAdminForm(request.POST)
		if form.is_valid():
			# form.save()
			# mcb=MyCustomBackend()
			# if  mcb.authenticateadmin(form.cleaned_data.get('username'),form.cleaned_data.get('password')):
			user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
			if  user:
				request.session['admin'] = user.id
				return redirect('home2')
			else:
				messages.error(request, 'You are not allowed to enter. Fuck Off!!')
				return redirect('home2')
	else:
		form = LoginAdminForm()
	
	# return render(request, 'login.html', {'form': form})
	return HttpResponse(template.render({'form': form}, request))

import sys
import json
from PIL import Image


# def test(request):
# 	sc = smartcrop.SmartCrop()
# 	crop_options = smartcrop.DEFAULTS
# 	img_path= 'media/wallpaper/66.jpg'
# 	img = Image.open(img_path)
# 	# print(img)
# 	template = loader.get_template('test.html')
# 	resolutions= Resolution.objects.all()
# 	for res in resolutions:
# 		# cek apakah besar gambar cukup untuk dicrop
# 		if res.w<=img.width and res.h<=img.height:
# 			resi_w= res.w
# 			resi_w_proc= res.w/img.width
# 			resi_h= int(img.height*resi_w_proc)
# 			if resi_w<res.w or resi_h<res.h:
# 				resi_h=res.h
# 				resi_h_proc= res.h/img.height
# 				resi_w= int(img.width*resi_h_proc)
# 			print(str(res.w)+'x'+str(res.h))
# 			print(str(img.width)+'x'+str(img.height)+'('+str(img.width/img.height)+')'+' => '+str(resi_w)+'x'+str(resi_h)+'('+str(resi_w/resi_h)+')')
# 			proc_img = img.resize((resi_w, resi_h), Image.ANTIALIAS)
# 			crop_options['width'] = res.w
# 			crop_options['height'] = res.h
# 			ret = sc.crop(proc_img, crop_options)
# 			print(ret['topCrop'])
# 			proc_img.crop((ret['topCrop']['x'], ret['topCrop']['y'], ret['topCrop']['width']+ret['topCrop']['x'], ret['topCrop']['height']+ret['topCrop']['y'])).save('media/wallpaper/'+str(res.w)+'x'+str(res.h)+'_66.jpg')
# 			wr = Wallpaper_resoultion(wallpaper= Wallpaper.objects.get(id_wallpaper=66), resolution= res, status=1)
# 			wr.save()
# 			print('saved')

# 			# break
# 	context = {
# 		'page': 'test',
#     }
# 	return HttpResponse(template.render(context, request))


# centered
def test(request):
	img_path= 'media/wallpaper/66.jpg'
	img = Image.open(img_path)
	# print(img)
	template = loader.get_template('test.html')
	resolutions= Resolution.objects.all()
	for res in resolutions:
		# cek apakah besar gambar cukup untuk dicrop
		if res.w<=img.width and res.h<=img.height:
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
			proc_img.crop((crop_x, crop_y, crop_x+res.w, crop_y+res.h)).save('media/wallpaper/'+str(res.w)+'x'+str(res.h)+'_66.jpg')
			wr = Wallpaper_resoultion(wallpaper= Wallpaper.objects.get(id_wallpaper=66), resolution= res, status=1)
			wr.save()
			print('saved')

			# break
	context = {
		'page': 'test',
    }
	return HttpResponse(template.render(context, request))


import random
def resizeall(wp):
	img_path= 'media/wallpaper/'+str(wp.id_wallpaper)+'.jpg'
	img = Image.open(img_path)
	# print(img)
	# template = loader.get_template('test.html')
	resolutions= Resolution.objects.all()
	for res in resolutions:
		# cek apakah besar gambar cukup untuk dicrop
		if res.w<=img.width and res.h<=img.height:
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
			proc_img.crop((crop_x, crop_y, crop_x+res.w, crop_y+res.h)).save('media/wallpaper/'+str(res.w)+'x'+str(res.h)+'_'+str(wp.id_wallpaper)+'.jpg')

			judul_name=''
			wall_tag= Wallpaper_tag.objects.filter(wallpaper=wp)
			# print('count : '+str(wall_tag.count()))
			if wall_tag.count() >1:
				first_rand=random.randint(0,wall_tag.count()-1)
				second_rand=random.randint(0,wall_tag.count()-1)
				while first_rand == second_rand:
					second_rand=random.randint(0,wall_tag.count()-1)

				judul_name= wall_tag[first_rand].tag.tag.title()+' '+ wall_tag[second_rand].tag.tag.title()
			else:
				print(wall_tag[0])
				judul_name= wall_tag[0].tag.tag.title()

			judul= (Word.objects.filter(word_type=0).order_by('?').first().word)+' '+judul_name+' '+(Word.objects.filter(word_type=1).order_by('?').first().word)+' '+res.resolution+' '+str(res.w)+'x'+str(res.h)
			wr = Wallpaper_resoultion(wallpaper= wp, resolution= res, status=1, title=judul)
			wr.save()
			print('saved')

# from sorl.thumbnail import get_thumbnail
# from sorl.thumbnail import delete
# def resizeall(wp):
# 	img_path= 'media/wallpaper/'+str(wp.id_wallpaper)+'.jpg'
# 	img = Image.open(img_path)
# 	# print(img)
# 	# template = loader.get_template('test.html')

# 	resolutions= Resolution.objects.all()
# 	for res in resolutions:
# 		im = get_thumbnail(img_path, str(res.w)+'x'+str(res.h), crop='center', quality=100)
# 		im.save('media/wallpaper/'+str(res.w)+'x'+str(res.h)+'_'+str(wp.id_wallpaper)+'.jpg')
# 		wr = Wallpaper_resoultion(wallpaper= wp, resolution= res, status=1)
# 		wr.save()

@required_admin
def home(request):
	template = loader.get_template('admin2/base.html')
	context = {
		# 'page': 'Admin Home',
		'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))

@required_admin
def grab(request):
	template = loader.get_template('admin2/v_grab.html')
	context = {
		'page': 'Sucking',
		'form': GrabForm(),
		'modalform': ModelWallpaperForm(),
		'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))

@required_admin
def grabhost_wallpaperscraft0com(request):
	host = 'wallpaperscraft.com'
	template = loader.get_template('admin2/v_grabhost_wallpapercraft-com.html')
	context = {
		'page': 'Sucking host wallpaperscraft.com',
		# 'form': GrabForm(),
		# 'modalform': ModelWallpaperForm(),
		'admin': User.objects.get(id=request.session['admin']),
    }
	return HttpResponse(template.render(context, request))


import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.request
from pathlib import Path
import random
def ajax_grabhost_wallpaperscraft0com_single(request):
	response_data = {}
	if request.method == 'POST':
		id_wallpapercraft0com= request.POST['id']
		url = 'https://wallpaperscraft.com/wallpaper/'+id_wallpapercraft0com
		page = requests.get(url)
		soupz = BeautifulSoup(page.content, 'html.parser')
		title = soupz.find('title').text
		# print(title)
		if title != 'Page Not Found':
			link=""
			source=""
			owner=""
			owner_license=""
			owner_link=""
			category=""

			tags=[]

			for tag in soupz.find("div", attrs={'class':'wallpaper__tags'}).findAll('a'):
				t=tag.text
				tags.append(t)
				# print(t)

			category = soupz.findAll('option', selected=True)[1].text.strip()
			# print(category)
			source = soupz.findAll("div", attrs={'class':'wallpaper-info__item'})[1].find('a')['href']
			source_split= source.split('/')
			link='https://images.wallpaperscraft.com/image/'+source_split[2]+'_'+source_split[3]+'.jpg'
			print(link)
			if soupz.findAll("div", attrs={'class':'author__row'})[0].text.strip() == 'License:  No licence' :
				owner = 'No licence'
				owner_license = ''
				owner_link = ''
			else:
				owner = soupz.findAll("div", attrs={'class':'author__row'})[0].text.strip().replace('Author: ','')
				owner_license = soupz.findAll("div", attrs={'class':'author__row'})[1].text.replace('License: ','')
				owner_link = soupz.find("a", attrs={'class':'author__link'})['href']
			# owner = soupz.findAll("div", attrs={'class':'author__row'})[0].text.strip().replace('Author: ','')
			# owner_license = soupz.findAll("div", attrs={'class':'author__row'})[1].text.replace('License: ','')
			# owner_link = soupz.find("a", attrs={'class':'author__link'})['href']
			print(owner)
			print(owner_license)
			print(owner_link)


			filename = link[link.rfind("/")+1:]
			ext = filename.split('.')[-1]
			urllib.request.urlretrieve(link, settings.BASE_DIR+'/media/test/'+filename)

			my_file = Path(settings.BASE_DIR+'/media/test/'+filename)
			if my_file.is_file():
				cats = Category.objects.filter(category=category)
				if not cats:
					cat =Category(category=category)
					cat.save()
				else:
					cat= cats[0]

				im = Image.open(my_file)
				wi, he = im.size
				im.close()

				wp = Wallpaper(link=link, source='https://wallpaperscraft.com'+source, owner=owner, owner_license=owner_license, owner_link=owner_link, category=cat, grab_host='wallpaperscraft.com', uploader= User.objects.order_by('?').first(), status=0, height=he, width=wi)
				wp.save()

				old_path= settings.BASE_DIR+'/media/test/'+filename
				new_path= settings.BASE_DIR+'/media/wallpaper/'+str(wp.id_wallpaper)+'.'+ext
				shutil.move(old_path, new_path)
				loc= new_path.replace(settings.BASE_DIR+'/media/', '')
				wp.wallpaper=loc

				color_thief = ColorThief(new_path)
				pale=''
				pallet = color_thief.get_palette(color_count=6)
				for x, colo in enumerate(pallet):
					c = ('#%02x%02x%02x' % (colo[0], colo[1], colo[2]))
					pale=pale+c+';'
				wp.colors=pale
				wp.save()
				# print(wp)
				for t in tags:
					tags = Tag.objects.filter(tag=t)
					if not tags:
						newtag =  Tag(tag=t)
						newtag.save()
					tag= Tag.objects.get(tag=t)
					wallpaper_tag = Wallpaper_tag(tag=tag, wallpaper=wp)
					wallpaper_tag.save()
				wp.status=1
				last_walls = Wallpaper.objects.exclude(post_at__isnull=True).order_by('-post_at')
				if last_walls:
					lw = last_walls[0]
					post_time= lw.post_at+timedelta(minutes=random.randint(3,5))
				else:
					post_time= datetime.datetime.now(tz=timezone.utc)
				wp.post_at=post_time
				wp.save()
				print('saved')
			# for lic in soupz.findAll("div", attrs={'class':'author__row'}):
			# 	print(lic.text)
		response_data= {
			'is_saved': True, 
			'id_wallpapercraft0com': id_wallpapercraft0com,
			'link': url,
			'title': title,
		}
	return JsonResponse(response_data)





@required_admin
def logout(request):
	request.session.flush()
	return redirect('home2')

import json
import shutil
import os


from google_images_download import google_images_download
from colorthief import ColorThief


@required_admin
def ajax_grab(request):
	shutil.rmtree('media/sucker', ignore_errors=True)
	response_data = {}
	if request.method == 'POST':
		response = google_images_download.googleimagesdownload()
		arguments = {
			"keywords": request.POST['keywords'],
			"limit": request.POST['limit'],
			"offset": request.POST['offset'],
			"size": request.POST['size'],
			"specific_site": request.POST['specific_site'],
			"no_numbering": True,
			"format": "jpg",
			"extract_metadata": True,
			"output_directory": 'media/sucker',
			"print_urls":True}
		paths = response.download(arguments)

		return JsonResponse(paths)
	else:
		return JsonResponse(response_data)

def readmeta(keyword):
	data2 = []
	with open('logs/'+keyword+'.json') as myfile:
		data2 = json.load(myfile)
	for i, dt in enumerate(data2):
		# filename = os.path.basename(urlparse.urlparse(data2[i]['image_link']).path)
		filename = data2[i]['image_link'].split("/")[-1] 
		data2[i]['path']= settings.MEDIA_URL+'sucker/'+keyword+'/'+filename
		# color_thief = ColorThief('media/sucker/'+keyword+'/'+filename)
		# pale=[]
		data2[i]['uploader'] = User.objects.order_by('?').first().id
		data2[i]['tags'] = keyword.lower()
		wallpapers = Wallpaper.objects.filter(link=data2[i]['image_link'])
		data2[i]['is_exist'] = True if wallpapers else False
		# if not wallpapers:
		# 	pallet = color_thief.get_palette(color_count=6)
		# 	for x, colo in enumerate(pallet):
		# 		# print('#%02x%02x%02x' % (colo[0], colo[1], colo[2]))
		# 		c = ('#%02x%02x%02x' % (colo[0], colo[1], colo[2]))
		# 		pale.append(c)
		# 	print(pale)
		# data2[i]['colors'] =pale
	return JsonResponse(data2,safe=False)

@required_admin
def ajax_refreshresult(request):
	if request.method == 'POST':
		return readmeta(request.POST['keywords'])
	else:
		return JsonResponse({})

import shutil
@required_admin
def ajax_submitwallpaper(request):
	response_data = {}
	if request.method == 'POST':
		form = ModelWallpaperForm(request.POST)
		if form.is_valid():
			f = form.save()
			filename = f.link.split("/")[-1]
			ext = filename.split('.')[-1]
			old_path='media/sucker/'+request.POST['keywords']+'/'+filename
			new_path='media/wallpaper/'+str(f.id_wallpaper)+'.'+ext
			shutil.copyfile(old_path, new_path)
			loc= new_path.replace('media/', '')
			f.wallpaper=loc
			f.save()
			color_thief = ColorThief('media/'+f.wallpaper.name)
			pale=''
			pallet = color_thief.get_palette(color_count=6)
			for x, colo in enumerate(pallet):
				c = ('#%02x%02x%02x' % (colo[0], colo[1], colo[2]))
				pale=pale+c+';'
			f.colors=pale
			f.save()
			post_tags= request.POST['tags']
			for t in filter(None,post_tags.split(',')):
				tags = Tag.objects.filter(tag=t)
				if not tags:
					newtag =  Tag(tag=t)
					newtag.save()
				tag= Tag.objects.get(tag=t)
				wallpaper_tag = Wallpaper_tag(tag=tag, wallpaper=f)
				wallpaper_tag.save()
			resizeall(f)
			response_data= {'is_valid': True, 'id': f.id_wallpaper}
	return JsonResponse(response_data)


@required_admin
def json_tags(request):
	response_data = []
	tags = Tag.objects.all()
	print(tags)
	for t in tags:
		response_data.append(t.tag)
	return JsonResponse(response_data, safe=False)

def archive(request, wallpaper_resolution_id=0, title=""):
	wr= Wallpaper_resoultion.objects.get(id=wallpaper_resolution_id)

	return HttpResponse('<h1>'+wr.title+'</h1>')
