from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import SummarizedArticle


def index(request):

    return HttpResponse("Hello, world. You're at the summarized_news index.")
