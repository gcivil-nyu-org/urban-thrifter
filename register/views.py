from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import HelpseekerForm

# Create your views here.
def register(request):
    # Check if logged in missing
    return render(request, 'register/index.html')

def helpseeker_register(request):
    # Check if logged in missing
    if request.method == 'POST':
        form = HelpseekerForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            
            # Resource parsing
            resources = form.cleaned_data.get('resource')
            d = {}
            for i in range(0,3):
                if 0 <= i < len(resources):
                    d['resource{0}'.format(i)] = resources[i]
                else:
                    d['resource{0}'.format(i)] = None
            obj.rc_1 = d['resource0']
            obj.rc_2 = d['resource1']
            obj.rc_3 = d['resource2']
            obj.save()
            
            username = form.cleaned_data.get('resource')
            messages.success(request, f'Account created for {username}!')
            # Must redirect to login page (this is a placeholder)
            return redirect('register')
    else:
        form = HelpseekerForm()
    return render(request, 'register/helpseeker_register.html', {'form':form})

def donor_register(request):
    # Check if logged in missing
    return render(request, 'register/donor_register.html')

