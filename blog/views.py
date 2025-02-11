# views.py
from itertools import count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from django.db.models import F, Count
from django.contrib import messages
from .models import Post, Comment, Category
from .forms import PostForm, CommentForm
from django.db.models import Q

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query)
            ).distinct()
        return queryset
    
    def get_queryset(self):
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by == 'views':
            return Post.objects.order_by('-view_count')
        return Post.objects.order_by(sort_by)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class PostDetailView(DetailView, FormMixin):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not request.session.get(f'post_viewed_{self.object.id}'):
            Post.objects.filter(id=self.object.id).update(view_count=F('view_count') + 1)
            request.session[f'post_viewed_{self.object.id}'] = True
        return response

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        return self.get_object().user == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.pk})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')
    
    def test_func(self):
        return self.get_object().user == self.request.user

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        content = request.POST.get('content')
        
        if content:
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )
            
            # 새로 생성된 댓글 HTML 렌더링
            context = {'comment': comment, 'user': request.user, 'post': post}
            comment_html = render_to_string('blog/comment_item.html', context, request)
            
            return JsonResponse({
                'status': 'success',
                'comment_html': comment_html,
                'comment_count': post.comments.count()
            })
        return JsonResponse({'status': 'error'}, status=400)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'
    
    def test_func(self):
        return self.get_object().user == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    
    def test_func(self):
        comment = self.get_object()
        return comment.user == self.request.user or comment.post.user == self.request.user
    
    def get_success_url(self):
        return reverse_lazy('post_detail', kwargs={'pk': self.object.post.pk})

@require_POST
def post_like(request, pk):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=401)
    
    post = get_object_or_404(Post, pk=pk)
    
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'count': post.likes.count(),
    })