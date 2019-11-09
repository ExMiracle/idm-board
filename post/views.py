from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
from itertools import chain

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

    # TODO: do catalog with this api endpoint
    @action(detail=False)
    def catalog(self, request):
        queryset = Post.objects.filter(is_thread=True).order_by('-updated_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def index(self, request):
        queryset = Post.objects.filter(is_thread=True).order_by('-updated_at')
        if queryset:
            result = []
            for thread in queryset:
                thread = Post.objects.filter(id=thread.id)
                thread_replies = thread[0].replies.all()[:3]
                # container.extend(thread).extend(thread_replies)
                # if thread_replies:
                thread_with_replies = list(chain(thread, thread_replies))
                result.extend(thread_with_replies)

            serializer = self.get_serializer(result, many=True)
            return Response(serializer.data)
        return Response('No threads yet')
