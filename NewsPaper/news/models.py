from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum



class Author(models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('postRating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.author_user.comment_set.aggregate(commentRating=Sum('commentRating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)


class Post(models.Model):
    news = 'NW'
    article = 'AR'
    CATEGORY_TYPE = [
        (news, 'Новость'),
        (article, 'Статья')
    ]
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    categoryType = models.CharField(max_length=2, choices=CATEGORY_TYPE, default=news)
    createDate = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=128)
    text = models.TextField()
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    postRating = models.IntegerField(default=0)

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.createDate.strftime("%Y-%m-%d %H:%M:%S")} {self.title}: {self.text[:20]}...'

    def like(self):
        self.postRating += 1
        self.save()

    def dislike(self):
        self.postRating -= 1
        self.save()


class PostCategory(models.Model):
    postLink = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryLink = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    commentText = models.TextField()
    commentDate = models.DateTimeField(auto_now_add=True)
    commentRating = models.IntegerField(default=0)

    def like(self):
        self.commentRating += 1
        self.save()

    def dislike(self):
        self.commentRating -= 1
        self.save()
