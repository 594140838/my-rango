#coding=utf-8
from django import forms
from django.contrib.auth.models import User
from models import Category, Page, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the category name.")#CharField相当于定义<input type="text">的文本输入框
    #模版中通过{{field.help_text}}输出help_text字段
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0) #相当于设置了<input type='hidden' value=0>，学会django中定义表单隐藏属性的方法
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    # An inline class to provide additional information on the form.
    class Meta:
        # Provide an association between the ModelForm and a model
        model = Category#可见字段的设置是在ModelForm的Meta类中设置fields属性来实现的，模版中通过{% for field in form.visible_fields %}获取表单
        fields = ('name',)


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        # Provide an association between the ModelForm and a model
        model = Page #模型与表单关联起来后，调用form.save()方法可以将表单代表的对象保存到数据库，数据库模型中的字段与表单字段对应
        # What fields do we want to include in our form?
        # This way we don't need every field in the model present.
        # Some fields may allow NULL values, so we may not want to include them...
        # Here, we are hiding the foreign key.
        exclude = ('category',) #等同于 fields = ('title', 'url', 'views')
        
    def clean(self):
        cleaned_data = self.cleaned_data #获取表单数据，以字典返回。cleaned_data方法比request.POST更好。数据类型都会自动转换好
        url = cleaned_data.get('url')#如果没有该字段，.get()会返回None而不会抛出异常

        # If url is not empty and doesn't start with 'http://', prepend 'http://'.
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')    
