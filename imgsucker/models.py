from __future__ import unicode_literals

from django.db import models
from django.contrib.humanize.templatetags.humanize import naturalday, naturaltime
from django.utils import timezone
import datetime
from django.contrib.auth.models import AbstractUser
from sorl.thumbnail import ImageField

class User(AbstractUser):
	avatar= models.ImageField(blank=True, null=True, upload_to='users')
	email = models.EmailField(unique=True, null=True)

class Resolution(models.Model):
	id_resolution= models.AutoField(primary_key=True)
	resolution= models.CharField(max_length=500, null=False, default=None)
	ct= (
        (0, 'Fullscreen'),
        (1, 'Widescreen'),
        (2, 'Mobile'),
        (3, 'Tablet'),
    )
	category= models.IntegerField(choices=ct, null=False, default=1)
	w= models.IntegerField(null=False, default=0)
	h= models.IntegerField(null=False, default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return '('+str(self.w)+'x'+str(self.h)+') - '+self.ct[self.category][1]+' - '+self.resolution


class Category(models.Model):
	id_category= models.AutoField(primary_key=True)
	# sekolah= models.ForeignKey(Sekolah, on_delete=models.SET_NULL,null=True)
	category= models.CharField(max_length=100, null=False, default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.category

from django.template.defaultfilters import slugify
class Wallpaper(models.Model):
	id_wallpaper= models.AutoField(primary_key=True)
	height = models.IntegerField()
	width = models.IntegerField()
	wallpaper= models.ImageField(blank=True, null=True, upload_to='wallpaper', height_field='height', width_field='width')
	created_at = models.DateTimeField(auto_now_add=True)
	# filename= models.CharField(max_length=500, null=False, default=None)
	source = models.CharField(max_length=500, null=False, default=None)
	link = models.CharField(max_length=500, null=False, default=None)
	colors = models.CharField(max_length=100, null=True, default=None)
	uploader = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
	likes= models.IntegerField(null=False, default=0)
	dislikes= models.IntegerField(null=False, default=0)
	views= models.IntegerField(null=False, default=0)
	downloads= models.IntegerField(null=False, default=0)
	favorites= models.IntegerField(null=False, default=0)
	rating= models.IntegerField(null=False, default=0)
	category= models.ForeignKey(Category, on_delete=models.SET_NULL,null=True)
	owner= models.CharField(max_length=500, null=True, default=None)

	owner_license= models.CharField(max_length=500, null=True, default=None)
	owner_link= models.CharField(max_length=500, null=True, default=None)
	st= (
		(0, 'Deactive'),
		(1, 'Active'),
	)
	status= models.IntegerField(choices=st, null=False, default=1)
	grab_host= models.CharField(max_length=100, null=True, default=None)
	stag= (
	    (0, 'Deactive'),
	    (1, 'Active'),
	)
	stage= models.IntegerField(choices=stag, null=True, default=1)
	post_at= models.DateTimeField(null=True, default=None)


	def tagsplit(self):
		return Wallpaper_tag.objects.filter(wallpaper=self)

	def tagtotitleslugify(self):
		title=''
		tagsplit=Wallpaper.tagsplit(self)
		for i, ta in enumerate(tagsplit):
			title=title+ta.tag.tag
			if i != (len(tagsplit) - 1):
				title=title+' '
		return slugify(title)

	def resolutionsplit(self):
		return Wallpaper_resoultion.objects.filter(wallpaper=self).order_by('resolution__resolution','resolution__category')

	def colorlist(self):
		return filter(None,self.colors.replace('#','').split(';'))

	def slugtags(self):
		slugtag=''
		tagsplit=Wallpaper.tagsplit(self)
		for i, tag in enumerate(tagsplit):
			slugtag=slugtag+slugify(tag.tag.tag)
			if i != (len(tagsplit) - 1):
				slugtag=slugtag+'_'
		return slugtag

	def alt(self):
		slugtag=''
		tagsplit=Wallpaper.tagsplit(self)
		for i, tag in enumerate(tagsplit):
			slugtag=slugtag+slugify(tag.tag.tag)
			if i != (len(tagsplit) - 1):
				slugtag=slugtag+', '
		return slugtag

	def test(self):
		return 'asdasdasd'

	def timehuman(self):
		result= self.post_at
		# result = naturaltime(self.post_at)
		# if (datetime.datetime.now()-self.post_at).days==0:
		# 	result = naturaltime(self.post_at)
		# elif (datetime.datetime.now()-self.post_at).days==1:
		# 	result = naturalday(self.post_at)
		return result

	def get_absolute_url(self):
		return "/wallpaper/%s_%s/" % (Wallpaper.slugtags(self), str(self.id_wallpaper))

	# def thumbnailsize(self, w, h):
	# 	max_w=400
	# 	max_h=250

	# 	prosen = 0
	# 	if self.wallpaper.height >= self.wallpaper.width:
	# 		prosen = self.wallpaper.height/max_h
	# 	else:
	# 		prosen = self.wallpaper.width/max_w

	# 	fix_w= int(self.wallpaper.width/prosen)

	# 	fix_h= int(self.wallpaper.height/prosen)

	# 	return str(fix_w)+'x'+str(fix_h)

	def __str__(self):
		return self.id_wallpaper

class User_action(models.Model):
	user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True)
	wallpaper = models.ForeignKey(Wallpaper, on_delete=models.SET_NULL,null=True)
	is_liked = models.BooleanField(default=False)
	is_disliked = models.BooleanField(default=False)
	is_favorited = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

class Wallpaper_resoultion(models.Model):
	wallpaper= models.ForeignKey(Wallpaper, on_delete=models.SET_NULL,null=True)
	resolution= models.ForeignKey(Resolution, on_delete=models.SET_NULL,null=True)
	title= models.CharField(max_length=300, null=False, default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	st= (
        (0, 'Deactive'),
        (1, 'Active'),
    )
	status= models.IntegerField(choices=st, null=False, default=1)

class Tag(models.Model):
	id_tag= models.AutoField(primary_key=True)
	# sekolah= models.ForeignKey(Sekolah, on_delete=models.SET_NULL,null=True)
	tag= models.CharField(max_length=100, null=False, default=None)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.tag



class Wallpaper_tag(models.Model):
	wallpaper= models.ForeignKey(Wallpaper, on_delete=models.SET_NULL,null=True)
	tag= models.ForeignKey(Tag, on_delete=models.SET_NULL,null=True)

class Word(models.Model):
	id_word= models.AutoField(primary_key=True)
	# sekolah= models.ForeignKey(Sekolah, on_delete=models.SET_NULL,null=True)
	word= models.CharField(max_length=100, null=False, default=None)
	created_at = models.DateTimeField(auto_now_add=True)
	wt= (
        (0, 'adj'),
        (1, 'add1'),
        (2, 'add2'),
    )
	word_type= models.IntegerField(choices=wt, null=False, default=None)

	def __str__(self):
		return self.tag