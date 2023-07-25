from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json, datetime

@login_required(login_url='authentication/login')
def index(request):
    return render(request, 'dashboard/index.html')