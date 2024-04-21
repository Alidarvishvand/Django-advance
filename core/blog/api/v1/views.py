from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response
from .serializers import PostSerializer, CategorySerializers
from ...models import Post, Category
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework import mixins, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .permissions import IsOwnerOrReadOnly
from .paginations import DefaultPagination

# 1from django.shortcuts import get_object_or_404


# data = {
#     "title":"Hello World",
# }


"""
@api_view(["Get", "Post"])
@permission_classes(IsAuthenticated)
def postlist(request):
    if request.method == "GET":
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    """


"""
@api_view(["Get", "PUT", "Delete"])
def postDetail(request,id):
    post = Post.objects.get(pk=id)
    try:
        if request.method == "GET":
            #1post = get_object_or_404(Post,pk=id)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = PostSerializer(post,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == "Dlete":
            post.delete()
            return Response("item deleted")
    except Post.DoesNotExist:
        return Response({"message":"Post does not exist"},status=status.HTTP_404_NOT_FOUND)
    
    """


"""class PostList(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get(self,request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)
    
    
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)  
        

"""
"""class PostDetail(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get(self, request,id):
        post = Post.objects.get(pk=id)
        serializer = self.serializer_class(post)
        return Response(serializer.data)
    
    def put(self, request,id):
        post = Post.objects.get(pk=id)
        serializer = self.serializer_class(post,data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request,id):
        post = Post.objects.get(pk=id)
        post.delete()
        return Response("item deleted")
    """

"""class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    
     

    
class PostDetail(RetrieveUpdateDestroyAPIView):
        
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    """


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = CategorySerializers
    queryset = Category.objects.all()

    @action(detail=False, methods=["get"])
    def get_ok(self, request):
        return Response({"detail": "ok"})


class PostModelsViewset(viewsets.ModelViewSet):
    """
    in model view set we have to create a serializer class  you can use all function defualt
    """

    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "author", "status"]
    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination

    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     print(context)
    #     context["request"]= self.request
    #     return  context

    # def  get_serializer_context(self,request,**kwargs):
    #     context = super().get_serializer_context(**kwargs)
    #     context["request"]= request
    #     return context


"""using a view set when you want to use view set you should create a view set class

    def retrieve(self, request, pk=None):
            post = self.queryset.get(pk=pk)
            serializer = self.serializer_class(post)
            return Response(serializer.data)    
        
    
    def create(self, request):
            pass
    def update(self, request, pk=None):
            pass
    def partial_update(self, request, pk=None):
            pass
    def destroy(self, request, pk=None):
            pass
            """
