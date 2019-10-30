from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import action
from rest_framework.response import Response


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
        queryset = Post.objects.filter(id=self.kwargs['pk'])
        # return queryset

        # return JsonResponse({queryset})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
