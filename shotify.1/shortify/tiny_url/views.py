from django.shortcuts import render
from tiny_url.forms import UserForm, ShortUrlForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from tiny_url.models import Url
from django.shortcuts import redirect


def register(request):
    registered=False
    if request.method=='POST':
        
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render(request,
            'register.html',
            {'user_form': user_form, 'registered': registered} )
            
def index(request):
    return render(request, 'index.html')
    
    
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/tiny_url/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Shortify account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'login.html', {})
        

"""@login_required
def shorten(request):
    shortened=False
    if request.method=='POST':
        url_form = ShortUrlForm(data=request.POST)
        if url_form.is_valid:
            url=url_form.save(commit=False)
            #url.full_url=
            if 'url' in request.FILES:
                url.full_url=request.FILES('url')
            url.save()
            shortened=True
        else:
            print url_form.errors
            
    else:
        url_form=ShortUrlForm()
        
            
        return render(request, 'shorten.html',{'url':url_form})
            
   """ 
    
    
    
    
    
        
    
    




# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/tiny_url/')
    
    
    
@login_required 
def short(request):
    is_shortened=False
    url_obj = None
    if request.method == 'POST':
        form=ShortUrlForm(request.POST)
        if form.is_valid():
            url_obj = form.save(commit=False)
            url_obj.user = request.user
            url_obj.save()
            is_shortened=True
            #return index(request)
            #print form.cleaned_data.get("full_url")
        else:
            print form.errors
    else:
        form=ShortUrlForm()
    
    return render(request, "shorten.html",{'form':form, 'is_shortened':is_shortened, 'url_obj':url_obj })


def redirect_short_url(request, short):
    full_url=Url.objects.get(short)
    return redirect(full_url, permanent=True)


    
"""def redirect_short_url(request):
    location=full_url
    res=HttpResponse(location, status=302)
    res['Location'] = location
    return res"""