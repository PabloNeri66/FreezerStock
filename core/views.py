from django.shortcuts import render
from . import metrics
import json


def home(request):
    geladinho_metrics = metrics.get_geladinho_metrics()
    sales_metrics = metrics.get_sales_metrics()
    daily_sales_data = metrics.get_daily_sales_data()

    context = {
        'geladinho_metrics': geladinho_metrics,
        'sales_metrics': sales_metrics,
        'daily_sales_data': json.dumps(daily_sales_data),
    }

    return render(request, 'home.html', context)
