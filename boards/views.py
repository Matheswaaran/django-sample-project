from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView, ListView

from .forms import CreateNewTopicForm, PostForm
from .models import Board, Post, Topic


# Create your views here.

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


class TopicsListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('board_id'))
        query_set = self.board.topics.order_by('-updated_at').annotate(replies=Count('posts') - 1)
        return query_set


# def board_topics(request, board_id):
#     board = get_object_or_404(Board, pk=board_id)
#     query_set = board.topics.order_by('-updated_at').annotate(replies=Count('posts') - 1)
#
#     page = request.GET.get('page', 1)
#
#     paginator = Paginator(query_set, 10)
#
#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         topics = paginator.page(1)
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)
#
#     return render(request, 'topics.html', {'board': board, 'topics': topics})

class PostsListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        self.topic.views += 1
        self.topic.save()
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('board_id'), pk=self.kwargs.get('topic_pk'))
        query_set = self.topic.posts.order_by('created_at')
        return query_set


# def topic_posts(request, board_id, topic_pk):
#     topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_pk)
#     topic.views += 1
#     topic.save()
#     return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def create_new_topic(request, board_id):
    board = get_object_or_404(Board, pk=board_id)

    if request.method == 'POST':
        form = CreateNewTopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', board_id=board.pk, topic_pk=topic.pk)
    else:
        form = CreateNewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})


@login_required
def reply_topic(request, board_id, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_pk)

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()

            return redirect('topic_posts', board_id=board_id, topic_pk=topic_pk)
    else:
        form = PostForm()

    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    # def get_form(self, form_class):
    #     form = super(PostUpdateView, self).get_form(form_class)
    #     form.fields['message'] = forms.CharField(
    #         widget=forms.Textarea(
    #             attrs={'rows': 5, 'placeholder': 'Post your reply here'}
    #         ))
    #     return form

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', board_id=post.topic.board.pk, topic_pk=post.topic.pk)
