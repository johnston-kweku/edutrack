from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .decorators import role_required
from .models import Invitation
from .forms import UserCreationForm, ProfileEditForm
import json
User = get_user_model()
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
        'student_count': Student.objects.count(),
        'class_count': Class.objects.count(),
    }
    return render(request, 'accounts/landing.html', context)


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin():
            return redirect('dashboards:admin_dashboard')
        elif request.user.is_parent():
            return redirect('dashboards:parents_dashboard')
        elif request.user.is_teaching_staff():
            return redirect('academics:teacher_academics_hub')
        
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
        role = data.get('role', '')

        try:
            user_obj = User.objects.get(username=username)
            if not user_obj.is_active:
                return JsonResponse({
                    'success': False,
                    'message': 'Account Deactivated. Please contact admin'
                })
        except User.DoesNotExist:
            pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.role == role:
                if not user.is_active:
                    return JsonResponse({
                        'success': False,
                        'message': 'Account deactivated. Contact admin for support'
                    })
                
                auth_login(request, user)

                if user.is_admin():
                    return JsonResponse({
                        'success': True,
                        'message': 'Login success',
                        'redirect_url': reverse('dashboards:admin_dashboard')
                    })
                
                elif user.is_teaching_staff():
                    return JsonResponse({
                        'success': True,
                        'message': 'Login success',
                        'redirect_url': reverse('academics:teacher_academics_hub')
                    })
                

                elif user.is_parent():
                    return JsonResponse({
                        'success': True,
                        'message': 'Login success',
                        'redirect_url': reverse('dashboards:parents_dashboard')
                    })
            
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid role selected'
                })
            
        else: 
            return JsonResponse({
                'success': False,
                'message': 'Invalid username/password'
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