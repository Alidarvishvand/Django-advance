from typing import Any
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic.base import TemplateView,RedirectView
from django.views.generic import ListView,DetailView,FormView,CreateView
from .models import Post
from .forms import PostForm
from django.urls import reverse
# Create your views here.unresolved import ‘django.shortcuts’


# def indexView(request):
#     name  = 'ali'
#     context = {'name':name}
#     return render(request, 'index.html',context)


class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self,**kwargs):
       context= super().get_context_data(**kwargs)
       context["name"] = "ali"
    #    context["posts"] = Post.objects.all()
       return context


# def RedirecTOMaktab(request):
#     return redirect(request, 'https://maktabkhooneh.com')


class RedirecTOMaktab(RedirectView):
    url = 'https://maktabkhooneh.com'
    
    def get_redirect_url(self,**kwargs):
        post = get_object_or_404(Post,pk=kwargs['pk'])
        print(post)
        return super().get_redirect_url(**kwargs)
    
    
class PostListView(ListView):
    queryset = Post.objects.all()
    model = Post
    context_object_name = 'posts'
    # paginate_by = 1
    ordering = '-id'
    def get_queryset(self):
         posts = Post.objects.filter(status=True)
         return posts
    
        
class PostDetailView(DetailView):
    model = Post
    

'''
class PostCreateView(FormView):
    template_name = 'blog/contact.html'
    form_class = PostForm
    success_url = '/blog/post/'
    def form_valid(self,form):
        form.save()
        return super().form_valid(form)    
'''   

class PostCreateView(CreateView):
    model = Post
    fields = ['author','title','content','status','category','published_date']
    success_url= '/blog/post'