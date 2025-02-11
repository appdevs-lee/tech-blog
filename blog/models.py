from django.db import models

# Create your models here.
# Post
# * 인기 게시글
# * 글 조회
# * 글 작성
# * 글 수정
# * 글 삭제
# * 조회수
# * 좋아요
# Comment
# * 기본 댓글
# Category
# * 카테고리

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.IntegerField(default=0)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)

    likes = models.ManyToManyField(
        'accounts.User',
        related_name='liked_posts',
        blank=True,
        verbose_name='좋아요'
    )
    
    @property
    def like_count(self):
        return self.likes.count()
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.content

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name