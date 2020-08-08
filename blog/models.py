import os

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

# Create your models here.
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from read_statistics.models import ReadNumExpandMethod, ReadDetail


def user_directory_path(instance, filename):
    ext = filename.split('.').pop()
    filename = '{0}_{1}.{2}'.format(instance.author, instance.title, ext)
    return os.path.join(str(instance.blog_type.type_name), filename)  # 系统路径分隔符差异，增强代码重用性


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod):
    title = models.CharField(max_length=50)
    blog_img = models.ImageField(blank=True, null=True, upload_to=user_directory_path)
    blog_cover = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='blog_img',
        processors=[ResizeToFill(300, 200)],  # 处理成一寸照片的大小
        format='JPEG',  # 处理后的图片格式
        options={'quality': 85}  # 处理后的图片质量
    )
    blog_show = ImageSpecField(  # 注意：ImageSpecField 不会生成数据库表的字段
        source='blog_img',
        processors=[ResizeToFill(1280, 800)],
        format='JPEG',  # 处理后的图片格式
        options={'quality': 85}  # 处理后的图片质量
    )
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog: %s>" % self.title
        # 这里定义一个方法，作用是当用户注册时没有上传照片，模板中调用 [ModelName].[ImageFieldName].url 时赋予一个默认路径

    def photo_url(self):
        if self.blog_img and hasattr(self.blog_img, 'url'):
            return self.blog_img.url
        else:
            return '/media/default/cover.jpg'

    def photo_cover_url(self):
        if self.blog_cover and hasattr(self.blog_cover, 'url'):
            return self.blog_cover.url
        else:
            return '/media/default/cover.jpg'

    def photo_show_url(self):
        if self.blog_show and hasattr(self.blog_show, 'url'):
            return self.blog_show.url
        else:
            return '/media/default/cover.jpg'

    class Meta:
        ordering = ['-created_time']
