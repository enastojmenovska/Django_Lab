from django import forms
from .models import Post, BloggerBlockedUser


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Post
        exclude = ("author",)


class BloggerBlockedUserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BloggerBlockedUserForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = BloggerBlockedUser
        exclude = ("blogger",)
