from django import forms
from .constant import MAX_LENGHT_TEXT
from .models import Comments, Post


# class PostForm(forms.Form):
#     title = forms.CharField(label = 'Название', max_length=MAX_LENGHT_TEXT)
#     # text = forms.TextField('Текст')
#     description = forms.CharField(label = 'Описание', widget=forms.Textarea)
#     price = forms.IntegerField(label = 'Цена', help_text = 'Рекомендованная розничная цена',min_value = 10, max_value = 100)
#     comment = forms.CharField(label = 'Комментарий',required=False, widget=forms.Textarea)

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = (
                'title',
                'category',
                'location',
                'pub_date',
                'text',
                'image',
                )
    
        
# class CommentForm(forms.Form):
#     # title = forms.CharField(label = 'Название', max_length=MAX_LENGHT_TEXT)
#     # author = forms.CharField(label ='Текст')
#     text = forms.CharField(label ='Текст')
#     # description = forms.CharField(label = 'Описание', widget=forms.Textarea)
#     # price = forms.IntegerField(label = 'Цена', help_text = 'Рекомендованная розничная цена',min_value = 10, max_value = 100)
#     # comment = forms.CharField(label = 'Комментарий',required=False, widget=forms.Textarea)   

class CommentForm(forms.ModelForm):
    
    class Meta:
        model = Comments
        fields = ('text',) 