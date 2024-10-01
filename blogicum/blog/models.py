from django.db import models
from django.contrib.auth import get_user_model

from .constant import MAX_LENGHT_TEXT

User = get_user_model()


class BaseMainModel(models.Model):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True, help_text='Снимите галочку, чтобы скрыть публикацию.')
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True


class Category(BaseMainModel):
    title = models.CharField('Заголовок', max_length=MAX_LENGHT_TEXT)
    description = models.TextField('Описание')
    slug = models.SlugField('Идентификатор', unique=True,
                            help_text='Идентификатор страницы для URL;\
 разрешены символы латиницы, цифры, дефис и подчёркивание.')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title

class Location(BaseMainModel):
    name = models.CharField('Название места', max_length=MAX_LENGHT_TEXT)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name
    
class Post(BaseMainModel):
    title = models.CharField('Название', max_length=MAX_LENGHT_TEXT)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата и время публикации',
                                    help_text='Если установить дату и время в\
 будущем — можно делать отложенные публикации.')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации')
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Местоположение')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория')
    image = models.ImageField('Фото', upload_to='posts_images', blank=True)

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        

class Comments(models.Model):
    text = models.TextField(verbose_name='Текст комментария')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
        
    class Meta:
        ordering = ('created_at',)
        
    def __str__(self) -> str:
        return self.text[:250]
        


