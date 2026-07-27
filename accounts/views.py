from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .helpers import get_dashboard_url_for_user
import json
from .decorators import role_required
from .models import User
from .models import Invitation




from .forms import UserCreationForm, ProfileEditForm

# Create your views here.

def landing(request):
    if request.user.is_authenticated:
        if request.user.is_admin():
            return redirect('dashboards:admin_dashboard')
        elif request.user.is_parent():
            return redirect('dashboards:parents_dashboard')
        elif request.user.is_teaching_staff():
            return redirect('academics:teacher_academics_hub')
            
    from academics.models import Student, Class
    context = {
        'student_count': Student.objects.filter(status=Student.Status.ENROLLED).count(),
        'class_count': Class.objects.count(),
    }
    return render(request, 'accounts/landing.html', context)





def login_view(request):
    if request.user.is_authenticated:
        return redirect(get_dashboard_url_for_user(request.user))

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)

        username = data.get('username', '')
        password = data.get('password', '')

        # Give deactivated users a specific, honest message rather than
        # a misleading "invalid credentials" — Django's ModelBackend
        # silently refuses to authenticate inactive users either way,
        # so without this check they'd get the generic error below instead.
        user_obj = User.objects.filter(username=username).first()
        if user_obj and not user_obj.is_active:
            return JsonResponse({
                'success': False,
                'message': 'Account deactivated. Please contact admin for support.'
            })

        user = authenticate(request, username=username, password=password)

        if user is None:
            return JsonResponse({
                'success': False,
                'message': 'Invalid username/password'
            })

        auth_login(request, user)
        return JsonResponse({
            'success': True,
            'message': 'Login success',
            'redirect_url': get_dashboard_url_for_user(user)
        })

    return render(request, 'accounts/login.html')




@login_required
@role_required('ADMIN')
def generate_invite_link(request):
    if request.method  == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON data'
            }, status=400)

        role = data.get('role', '')
        if not role:
            return JsonResponse({
                'success': False,
                'message': 'Please provide a valid role'
            })
        
        if role not in User.Roles.values:
            return JsonResponse({'success': False, 'message': 'Invalid role'})  
        

        invitation = Invitation.objects.create(
            role=role,
            created_by=request.user
        )

        invitation_link = request.build_absolute_uri(f'/register/?token={invitation.token}')

        return JsonResponse({
            'success': True,
            'message': 'Invite link generated successfully',
            'invitation_link': invitation_link
        })
    
    return render(request, 'accounts/invite_link.html')


@role_required('ADMIN')
def delete_user(request, username):
    if request.method == 'POST':
        user = get_object_or_404(User, username=username)
        if user.role == 'ADMIN':
            return JsonResponse({
                'success':False,
                'message': 'Cannot delete this type of user'
            })
        
        user.delete()

        return JsonResponse({
            'success': True,
            'message': 'User deleted successfully'
        })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)


def register(request):
    token = request.GET.get('token')
    invitation = get_object_or_404(Invitation, token=token)
    
    if not invitation.is_valid() or not token:
        return redirect('accounts:invalid_invite')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = invitation.role
            user.save()
            invitation.is_used = True
            invitation.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {
        'invitation': invitation,
        'form': form
    })


def invalid_invite(request):
    return render(request, 'accounts/invalid_invite.html')


def logout_view(request):
    logout(request)
    return redirect('accounts:landing')




@login_required
def edit_my_profile(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:edit_my_profile')
    else:
        form = ProfileEditForm(instance=request.user)

    context = {
        'form': form
    }
    return render(request, 'accounts/edit_my_profile.html', context)


@require_POST
@role_required('ADMIN')
def toggle_active_state(request, user_id):

    user = get_object_or_404(User, id=user_id)

    user.is_active = not user.is_active
    user.save()

    message = f'User has been toggled {'active' if user.is_active else 'inactive'}'
    status = 'Active' if user.is_active else 'Inactive'

    return JsonResponse({'is_active': user.is_active, 'message': message, 'status': status})


@login_required
def my_profile(request):
    return render(request, 'accounts/my_profile.html')



@role_required('ADMIN')
@login_required
def user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
    
    context = {
        'profile_user': user,
    }
    
    return render(request, 'accounts/user_profile.html', context)




@login_required
def contact_administration(request):
    """
    Simple read-only admin contact info page for parents.
    No messaging, just displays admin(s) phone/email.
    """
    admins = User.objects.filter(role=User.Roles.ADMIN, is_active=True).order_by('full_name')

    context = {
        'admins': admins,
    }
    return render(request, 'accounts/contact_administration.html', context)