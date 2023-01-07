from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
import csv
from collections import Counter
from django.http import HttpResponse, HttpResponseNotFound

@login_required
def index(request):

    return render(request, 'index.html')