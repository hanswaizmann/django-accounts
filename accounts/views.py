from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import SignUpForm, UserProfileSignUpForm, UserProfileEditForm

from accounts.forms import PasswordChangeCustomForm
# from django.conf import settings
from django.contrib.auth import get_user_model

from django.views import generic
from django.contrib.auth import views as auth_views

from webpages.models import WebPage

# @login_required
def userbackend(request):
    webpage = WebPage.objects.filter(alias='userbackend')[0]
    if request.user.is_authenticated:
        user_profile_form = UserProfileEditForm(instance=request.user.userprofile)
        if request.method == 'POST':
            user_profile_form = UserProfileEditForm(request.POST, instance=request.user.userprofile)

            if user_profile_form.is_valid():
                userProfileObj = user_profile_form.save(commit=False)
                userProfileObj.save()
        else:
            print('form not valid!!!')
        c = { 
                'webpage': webpage,
                'forms': [user_profile_form]
            }
        return render(request, 'userbackend.html', c)

    else:
        raise Http404

def userprofile(request, pk, slug):
    webpage = WebPage.objects.filter(alias='userprofile')[0]
    try:
        userprofile = UserProfile.objects.get(id=pk)
        if slug != userprofile.slug():
            raise Http404
        votes = userprofile.votes.order_by('-created_at').select_related()[:10]
    except userprofile.DoesNotExist:
        raise Http404


    meta_title = userprofile.user.get_name() + ' - ' + userprofile.desc 
    meta_desc = meta_title
    meta_title = Truncator(meta_title).chars(80)


    t = Template(webpage.meta_title)
    webpage.meta_title = t.render(Context({'userprofile': userprofile}))
    t = Template(webpage.meta_desc)
    webpage.meta_desc = t.render(Context({'userprofile': userprofile}))

    c = {
        'userprofile': userprofile, 
        'votes': votes,
        'webpage': webpage
    }

    if (userprofile.online == 0):
        raise Http404

    return render(request, 'userprofile.html', c)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        userprofile_form = UserProfileSignUpForm(request.POST)
        if form.is_valid() and userprofile_form.is_valid():
            user = form.save()
            userprofile_form = UserProfileSignUpForm(request.POST, instance=user.userprofile)
            userprofile = userprofile_form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = SignUpForm()
        userprofile_form = UserProfileSignUpForm(request.POST)

    return render(request, 'signup.html', {'forms': [form, userprofile_form]})

class PasswordChangeView(auth_views.PasswordChangeView):
    form_class = PasswordChangeCustomForm
    model = get_user_model()
    template_name = 'password_change.html'
