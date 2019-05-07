from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from .forms import UserRegisterForm


# Only admin can add new user.
@permission_required('auth.add_user', raise_exception=True)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'User account: {username} has been created!')
            return redirect('register')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})
