from email import message
from django.shortcuts import render, redirect
from .models import Stock
import requests;
import json;
from django.contrib import messages
from .forms import StockForm

# Create your views here.


def home(request):

    
    if(request.method == 'POST'):
        ticker = request.POST['ticker']
        
        api_req = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker + "/quote?token=pk_0ba9707bab164631a6a9a920e8320bec");
        try:
            res = json.loads(api_req.content)
        except Exception as e:
            res = "Error"
        return render(request, 'Ticker.html', {'api':res})
    else:
        
        home_stocks = ['aapl', 'msft', 'googl', 'amzn', 'tsla', 'nvda']
        
        stocks = []
        
        for stock in home_stocks:
            api_req = requests.get("https://cloud.iexapis.com/stable/stock/"+ stock + "/quote?token=pk_0ba9707bab164631a6a9a920e8320bec");
            #pk_0ba9707bab164631a6a9a920e8320bec
            try:
                res = json.loads(api_req.content)
            except Exception as e:
                res = "Error"
                
            stocks.append(res)
            
        return render(request, 'Home.html', {'api': stocks})
    
    
def add_stock(request):
    if request.method == 'POST':
        form = StockForm(request.POST or None);
        
        if(form.is_valid()):
            form.save()
            messages.success(request, "Stock is added to portfolio");
    
    return redirect('home')


def portfolio(request):
    
    ticker = Stock.objects.all()
    stocks = []
    
    for tick in ticker:
        print(tick.id)
        api_req = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(tick) + "/quote?token=pk_0ba9707bab164631a6a9a920e8320bec");
        try:
            dict = {}
            res = json.loads(api_req.content)
            dict.update({"id":tick.id, "ticker":res})
            stocks.append(dict)
        except Exception as e:
            res = "Error"
    
    return render(request, 'Portfolio.html', {'stocks': stocks})
    
    
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request , "Stock is removed")
    return redirect("portfolio")