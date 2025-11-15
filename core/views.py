from django.shortcuts import render
from . import metrics


def home(request):
    geladinho_metrics = metrics.get_geladinho_metrics()
    sales_metrics = metrics.get_sales_metrics()

    context = {
        'geladinho_metrics': geladinho_metrics,
        'sales_metrics': sales_metrics,
    }

    return render(request, 'home.html', context)
