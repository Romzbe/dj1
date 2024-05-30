from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    authorUser = models.OneToOneField(User,on_delete=models.CASCADE)
    ratingA = models.SmallIntegerField(default=0)
    def update_rating(self):
        postRat = self.post_set.aggregate(postRatting=Sum('ratingP'))
        pRat = 0
        pRat += postRat.get('postRating') or 0.0

        comRat = self.authorUser.comment_set.aggregate(comRating=Sum('rating'))
        cRat = 0
        cRat += comRat.get('comRating') or 0.0

        self.ratingA= pRat*3 + cRat
        self.save()



class Category(models.Model):
    name = models.CharField(max_length=70,
                            unique=True)

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    NEWS = "NW"
    ARTICLE = "AR"
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья')
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dataCreat=models.DateTimeField(auto_now_add=True)
    postCategory=models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    ratingP = models.SmallIntegerField(default=0)

    def preview(self):
        return self.text[0:123]+'...'

    def like(self):
        self.ratingP +=1
        self.save()

    def dislike(self):
        self.ratingP -=1
        self.save()

class PostCategory(models.Model):
    postThr = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThr = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    CommentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    CommentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    textFild = models.TextField()
    dateCreat = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def like(self):
        self.rating +=1
        self.save()

    def dislike(self):
        self.rating -=1
        self.save()