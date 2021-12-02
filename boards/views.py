from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreateNewTopicForm, PostForm
from .models import Board, Post, Topic


# Create your views here.

def home(request):
    active_boards = Board.objects.filter(is_active=True)
    inactive_boards = Board.objects.filter(is_active=False)
    inactive_boards_count = len(inactive_boards)
    return render(request, 'home.html', {'active_boards': active_boards, 'inactive_boards': inactive_boards,
                                         'inactive_boards_count': inactive_boards_count})


def board_topics(request, board_id):
    board = get_object_or_404(Board, pk=board_id)
    return render(request, 'topics.html', {'board': board})


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


def topic_posts(request, board_id, topic_pk):
    topic = get_object_or_404(Topic, board__pk=board_id, pk=topic_pk)
    return render(request, 'topic_posts.html', {'topic': topic})


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
