from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from .forms import UserRegisterForm


# Only admin can add new user.
@permission_required("auth.add_user", raise_exception=True)
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get group_name from the form and apply the user to it.
            group_name = form.cleaned_data.get("group")
            group = Group.objects.get(name=group_name)
            user.groups.add(group)

            # Display message.
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"User account: {username} has been created!"
            )

            return redirect("register")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})
