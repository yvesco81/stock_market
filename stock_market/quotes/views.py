from django.shortcuts import redirect, render
from django.contrib import messages
from .forms import StockForm
from .models import Stock
import requests
import json


def get_ticker_infos(ticker):
    api_key = "csr9cqpr01qhtrfn15b0csr9cqpr01qhtrfn15bg"
    url_quote = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={api_key}"
    url_profile2 = f"https://finnhub.io/api/v1/stock/profile2?symbol={ticker}&token={api_key}"
    
    try:
        api_request = requests.get(url_profile2)
        data_profile = api_request.json()
        
        api_request = requests.get(url_quote)
        data_quote = api_request.json()
        
        if not data_profile or not data_quote:
            raise ValueError(f"Error Ticker '{ticker}' does not exist or has no data.")
            
        data = {**data_profile, **data_quote}
    except Exception as e:
        data = {'error': str(e)}
          
    return data


def home(request):
    
    if request.method == "POST":
        ticker = request.POST['ticker']
        
        context = {'data': get_ticker_infos(ticker)} 
        
        
    else:
        context = {'ticker':"Enter a ticker Symbol Above..."} 
        
    return render(request,'home.html',context)


def about(request):
    url = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=IBM&apikey=8XV14PUJF2X9ZCIT'
    r = requests.get(url)
    data = r.json()
    
    context = {} 
    return render(request,'about.html',context)


def add_stock(request):
    if request.method == "POST":
        form = StockForm(request.POST)
        
        if form.is_valid():
            ticker = form.cleaned_data['ticker']
            ticker_infos = get_ticker_infos(ticker)
            if 'error' in ticker_infos:
                messages.error(request, ticker_infos['error'])
            else:
                form.save()
                messages.success(request, f"{ticker} Has Been Added")
            return redirect('add_stock')
    else:    
        tickers = Stock.objects.all()
        output = []
        for ticker in tickers:
            output.append( get_ticker_infos(ticker))

        context = {'output': output} 
        return render(request,'add_stock.html',context)


def delete(request,stock_id):
    ticker = Stock.objects.get(pk=stock_id)
    ticker.delete()
    messages.success(request, f"{ticker} Has Been Deleted")
    return redirect('delete_stock')


def delete_stock(request):
    tickers = Stock.objects.all()
    
    context = {'tickers':tickers} 
    return render(request,'delete_stock.html',context)