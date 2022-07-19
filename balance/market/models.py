from django.db import models
from django.forms import ValidationError


def email_valid(value):
    if '@gmail.com' in value:
        return value
    else:
        raise ValidationError('only google')


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255)
    # если 10 жалоб на этот пользователь 
    # то меняете на black_list - TRUE
    black_list = models.BooleanField(default=False)
    email = models.EmailField(validators=[email_valid])

    @property
    def user_ban_count(self):
        q = self.user_ban_1.count()
        return q

    
    @property
    def user_post_count(self):
        post = self.users.count()
        return post


    def get_full_name(self): 
        full_name  =  '%s %s %s' % (self.first_name, self.last_name,  self.middle_name)
        return full_name.strip()

    def __str__(self) -> str:
        return self.get_full_name()


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    post = models.CharField(max_length=255)
    descr  = models.TextField()
    
    @property
    def like_count(self):
        return self.post_like.count()

    @property
    def user_like_post(self):
        s = []
        for i in self.post_like.all():
            s.append(i.author.get_full_name())
        return s


    def __str__(self) -> str:
        return f'Author{self.author.first_name} post{self.post}'


class Like(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_like')

    def clean(self):
        a = Like.objects.filter(author=self.author, post=self.post).exists()
        if a:
            raise ValidationError('Вы уже лайкнули этот пост')
        super().clean()

    def __str__(self) -> str:
        return f'Post_id: {self.post.id}'

class Ban(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ban')
    reseiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ban_1')

    # def save(self, *args, **kwargs) -> None:
    #     if self.band.id >=5:
    #         self.band.black_list = True
    #         self.band.save()
    #     super(Band, self).save(*args, **kwargs)


    def clean(self) -> None:
        check_count = self.reseiver.user_ban_count
        check_active = self.reseiver.black_list
        if check_active is True:
            raise ValidationError('Пользователь уже заблокирован')
        if check_count >= 3 and check_active is False:
            self.reseiver.black_list = True
        self.reseiver.save()
        super().clean()
