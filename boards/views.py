from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CreateNewTopicForm
from .models import Board, Post, User


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
    user = User.objects.first()  # TODO: get the currently logged in user

    if request.method == 'POST':
        form = CreateNewTopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=user
            )
            return redirect('board_topics', board_id=board.pk)  # TODO: redirect to the created topic page
    else:
        form = CreateNewTopicForm()

    return render(request, 'new_topic.html', {'board': board, 'form': form})
