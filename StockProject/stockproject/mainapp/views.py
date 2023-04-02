from django.shortcuts import render
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread

from django.db.models import Q
from django.views.generic import TemplateView, ListView


# Create your views here.


def stockList(request):
    if request.method == "POST":
        searched = request.POST['searched']
        
        stocks = tickers_nifty50()
        Stock = stocks.filter(Stock__contains=searched)

        return render(request, 
            'mainapp/searchstocklist.html', 
            {'searched':searched,
            'Stocks':Stock})
    
    else:
        return render(request, 'mainapp/searchstocklist.html',
        {''})




def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})

def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    print(stockpicker)
    data = {}
    avaliable_stocks = tickers_nifty50()
    for i in stockpicker:
        if i in avaliable_stocks:
            pass
        else:
            return HttpResponse('Error')

    n_threads = len(stockpicker)
    thread_list = []
    que = queue.Queue()

    start = time.time()

    # # print(data)
    # for i in stockpicker:
    #     result = get_quote_table(i)
    #     data.update({i: result}) #stocks details

    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args = (que, stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()
    for theread in thread_list:
        theread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
    end = time.time()
    tme_taken = end - start
    
    print(data)
    print(tme_taken)
    # details = get_quote_table('RELIANCE.NS')
    # print(details)
    return render(request, 'mainapp/stocktracker.html', {'data':data})


# class SearchStock(ListView):
#     stock = tickers_nifty50()
#     template_name = "searchstocklist.html"

#     def stockPicker(self):
#         query = self.request.GET.get("q")
#         stock_list = tickers_nifty50().objects.filter(
#             Q(Stock__icontains=query)
#         )
#         return stock_list
#         # stock_picker = tickers_nifty50()
#         # print(stock_picker)
#         # return render(request, 'mainapp/stockpicker.html', {'stockpicker':stock_picker})

# 

# <!-- <!doctype html>
# <html lang="en">
# {% load static %}
# <head> -->
#     <!-- Required meta tags -->
#     <!-- <meta charset="utf-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1"> -->

#     <!-- Bootstrap CSS -->
#     <!-- <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
#         integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
#     <link rel="stylesheet" type="text/css" href="{% static 'mainapp/css/basic.css'%}">
#     <title>{% block title %} {% endblock %}</title>
#     <style>

#     </style>
#     {% block css %}
#     {% endblock %}
# </head>

# <body>
#     <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
#         <div class="container-fluid">
#             <a class="navbar-brand" href="#">StockProject</a>
#             <button class="navbar-toggler" type="button" data-bs-toggle="collapse"
#                 data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false"
#                 aria-label="Toggle navigation">
#                 <span class="navbar-toggler-icon"></span>
#             </button>
#             <div class="collapse navbar-collapse" id="navbarSupportedContent">
#                 <ul class="navbar-nav me-auto mb-2 mb-lg-0">
#                     <li class="nav-item">
#                         <a class="nav-link active" aria-current="page" href="#">Home</a>
#                     </li>
#                     <li class="nav-item">
#                         <a class="nav-link" href="#">Link</a>
#                     </li>
#                     <li class="nav-item dropdown">
#                         <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button"
#                             data-bs-toggle="dropdown" aria-expanded="false">
#                             Dropdown
#                         </a>
#                         <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
#                             <li><a class="dropdown-item" href="#">Action</a></li>
#                             <li><a class="dropdown-item" href="#">Another action</a></li>
#                             <li>
#                                 <hr class="dropdown-divider">
#                             </li>
#                             <li><a class="dropdown-item" href="#">Something else here</a></li>
#                         </ul>
#                     </li>
#                     <li class="nav-item">
#                         <a class="nav-link disabled" href="#" tabindex="-1" aria-disabled="true">Disabled</a>
#                     </li>
#                 </ul>
#                 <form class="d-flex">
#                     <input class="form-control me-2" type="search" name ="q" placeholder="Search" aria-label="Search">
#                     <button class="btn btn-outline-success" type="submit">Search</button>
#                 </form>
#             </div>
#         </div>
#     </nav>
#     {% block body %}
#     {% endblock %} -->
#     <!-- Optional JavaScript; choose one of the two! -->

#     <!-- Option 1: Bootstrap Bundle with Popper -->
#     <!-- <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js"
#         integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM"
#         crossorigin="anonymous"></script> -->

#     <!-- Option 2: Separate Popper and Bootstrap JS -->
#     <!--
#     <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
#     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
#     -->
# <!-- </body>
# <script>

# </script>
# {% block js %}{% endblock %}

# </html> -->