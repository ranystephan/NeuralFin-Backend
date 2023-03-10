from django.shortcuts import render

import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view

import os
import environ
env = environ.Env()
environ.Env.read_env()




def get_stock_data(request, ticker):
    
    api_key = env('ALPHA_VANTAGE_API_KEY')
    url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)



@api_view(['GET'])
def stock_data_api(request, ticker):
    data = get_stock_data(request, ticker)
    return JsonResponse(data)