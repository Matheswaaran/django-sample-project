from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import SignUpForm, UserEditForm, ProfileEditForm


# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


# class UserUpdateView(UpdateView):
#     model = User
#     fields = ('first_name', 'last_name', 'email')
#     template_name = 'my_account.html'
#     success_url = reverse_lazy('my_account')
#
#     def get_object(self):
#         return self.request.user

def UserUpdateView(request):
    if request.method == 'POST':
        user_update_form = UserEditForm(instance=request.user, data=request.POST)
        profile_update_form = ProfileEditForm(
            instance=request.user.profile,
            data=request.POST,
            files=request.FILES
        )
        if user_update_form.is_valid() and profile_update_form.is_valid():
            user_update_form.save()
            profile_update_form.save()
            messages.success(request, message='Profile Updated Successfully')
            return redirect('my_account')
        else:
            messages.error(request, message='Error updating your file. Please try again!')
    else:
        user_update_form = UserEditForm(instance=request.user)
        profile_update_form = ProfileEditForm(instance=request.user.profile)

    return render(request, 'my_account.html',
                  {'user_update_form': user_update_form, 'profile_update_form': profile_update_form})
