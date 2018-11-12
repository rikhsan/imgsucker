from django.contrib.sitemaps import Sitemap
from imgsucker.models import Wallpaper, Wallpaper_tag
import datetime
from django.utils import timezone

class BlogSitemap(Sitemap):
	# changefreq = "never"
	# priority = 0.5
	limit = 100

	def items(self):
		return Wallpaper.objects.filter(post_at__lte=datetime.datetime.now(tz=timezone.utc)).order_by('-post_at')

	def lastmod(self, obj):
		return obj.post_at	

	def title(self, obj):
		tit = ""
		for i, tag in enumerate(Wallpaper_tag.objects.filter(wallpaper = obj)):
			tit = tit+tag.tag
			if i != len(Wallpaper_tag.objects.filter(wallpaper = obj)):
				tit = tit + ', '

		return 'Wallpaper '+ tit
