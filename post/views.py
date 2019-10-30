from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    """
    API endpoint that shows all posts.
    """
    queryset = Post.objects.all().order_by('date_posted')
    serializer_class = PostSerializer

    @action(detail=False, methods=['post'])
    def new_thread(self, request):
        thread = Post.objects.new_thread(request.POST, request.FILES)
        return Response('success')

    #         TODO: check if isinstance(list, post): if it is error

    @action(detail=True, methods=['post'])
    def new_reply(self, request, pk=None):
        post = Post.objects.new_reply(request.POST, request.FILES, self.kwargs['pk'])
        return Response('success')

    #         TODO: check if isinstance(list, post): if it is error

    @action(detail=True)
    def query(self, request, pk=None):
        thread_queryset = Post.objects.filter(id=self.kwargs['pk'])
        if thread_queryset:
            thread = Post.objects.get(id=self.kwargs['pk'])
            replies = thread.replies.all()
            serializer = self.get_serializer(thread_queryset.union(replies), many=True)
            return Response(serializer.data)
        return Response("thread doesn't exist")
