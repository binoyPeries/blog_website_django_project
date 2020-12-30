from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required


# important
# when you submit the form it gets re-routed
# back to this page hence we use the post method find whether its a re route if so we handle the  data
def register(request):
    if request.method == 'POST':
        # request.post is use to get the posted data
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created successfully')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    # instance is added to fill the form with existing user data
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        # request.files is needed cuz this is a image
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account info was updated successfully')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'user_update': u_form, 'pro_update': p_form}
    return render(request, 'users/profile.html', context)
