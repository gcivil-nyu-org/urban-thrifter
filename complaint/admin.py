from django.contrib import admin
from .models import Complaint

class ComplaintAdmin(admin.ModelAdmin):
    readonly_fields = ('uploaded_at','subject','message','image')

admin.site.register(Complaint,ComplaintAdmin)
