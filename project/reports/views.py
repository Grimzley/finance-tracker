from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def report_list_view(request):
    pass
