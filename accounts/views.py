from django.shortcuts import render, redirect
from .forms import ChangePasswordForm


def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            # form.save()
            return redirect('success')
    else:
        form = ChangePasswordForm()
    return render(request, 'accounts/password_change.html', {'form': form})
