from django.shortcuts import render

from .forms import ComplaintForm
from .models import Complaint

# Create your views here.
def home(request):
    return render(request,'complaint/home.html')

def issue_complaint(request):
    if request.method=='POST':
        filled_form=ComplaintForm(request.POST,request.FILES)
        if filled_form.is_valid():
            note="Your complaint about %s has been received. We will look into it!!" %(filled_form.cleaned_data['subject'],)
            new_form=ComplaintForm
            filled_form.save()
            return render(request,'complaint/issue_complaint.html', {'complaintform':new_form,'note':note})
    else:
        form = ComplaintForm()
        return render(request,'complaint/issue_complaint.html', {'complaintform':form})
