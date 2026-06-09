from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash


@require_POST
@login_required
def update_personal(request):
    user = request.user
    user.first_name     = request.POST.get('first_name', '').strip()
    user.last_name      = request.POST.get('last_name', '').strip()
    user.email          = request.POST.get('email', '').strip()
    user.phone          = request.POST.get('phone', '').strip()
    user.bio            = request.POST.get('bio', '').strip()

    dob = request.POST.get('date_of_birth', '').strip()
    if dob:
        user.date_of_birth = dob

    user.save()
    messages.success(request, 'Personal details updated successfully.')
    return redirect('/profile/')


@require_POST
@login_required
def update_security(request):
    user             = request.user
    current_password = request.POST.get('current_password', '')
    new_password     = request.POST.get('new_password', '')
    confirm_password = request.POST.get('confirm_password', '')

    if not user.check_password(current_password):
        messages.error(request, 'Current password is incorrect.')
        return redirect('/profile/')

    if not new_password:
        messages.error(request, 'New password cannot be empty.')
        return redirect('/profile/')

    if new_password != confirm_password:
        messages.error(request, 'New passwords do not match.')
        return redirect('/profile/')

    if len(new_password) < 8:
        messages.error(request, 'Password must be at least 8 characters.')
        return redirect('/profile/')

    user.set_password(new_password)
    user.save()
    update_session_auth_hash(request, user)
    messages.success(request, 'Password updated successfully.')
    return redirect('/profile/')


@require_POST
@login_required
def update_address(request):
    user          = request.user
    user.address  = request.POST.get('street_address', '').strip()
    user.city     = request.POST.get('city', '').strip()
    user.state    = request.POST.get('state', '').strip()
    user.zip_code = request.POST.get('zip_code', '').strip()
    user.country  = request.POST.get('country', '').strip()

    user.save()
    messages.success(request, 'Delivery address updated successfully.')
    return redirect('/profile/')
