from django import forms
from .models import Article
from pagedown.widgets import PagedownWidget

class ArtcleCreate_Update(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget())
    published = forms.BooleanField(initial=True, label="Publish")
    class Meta:
        model = Article
        fields = ('title', 'thumbnail',)

class Artcle_Update(forms.ModelForm):
    thumbnail = forms.ImageField(required=False)
    content = forms.CharField(widget=PagedownWidget())
    published = forms.BooleanField(initial=True, label="Publish")

    class Meta:
        model = Article
        fields = ('title', )