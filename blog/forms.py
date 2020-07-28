from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from blog.models import Blog, BlogType


class ArticleForm(forms.Form):
    title = forms.CharField(label="标题",
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入文章标题'}))
    content_type = forms.ModelChoiceField(label="文章类型", queryset=BlogType.objects.all(),
                                          widget=forms.Select(attrs={'class': 'form-control'}))
    text = forms.CharField(label="文章内容", widget=CKEditorUploadingWidget(config_name='default'),
                           error_messages={'required': '博客内容不能为空'})
    cover = forms.ImageField(label="封面")

    class Meta:
        model = Blog
        fields = ('title', 'text', 'content_type', 'cover')
