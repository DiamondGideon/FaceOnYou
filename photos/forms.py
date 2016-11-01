from django import forms
from django.contrib.auth.models import User

from .models import Post, Coment, Mask


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['post_title', 'hashtag', 'photo']


countries_list = Mask.objects.all()

class MaskForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(MaskForm, self).__init__(*args, **kwargs)
        self.fields['selectedImage'] = forms.ChoiceField(choices=countries_list)


class ComentForm(forms.ModelForm):
    class Meta:
        model = Coment
        fields = ['text']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


