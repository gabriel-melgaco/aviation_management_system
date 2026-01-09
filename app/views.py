from django.shortcuts import render
from . import metrics
from datetime import datetime
import json
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    date_str = request.GET.get('date')

    if date_str:
        date = datetime.strptime(date_str, "%Y-%m").date()
    else:
        date = None

    context = {
        'inventory_metrics': metrics.get_inventory_metrics(),
        'order_metrics': metrics.get_order_metrics(),
        'inflow_outflow_metrics': metrics.get_inflow_outflow_metrics(date),
        'daily_inflows_data': json.dumps(metrics.get_chart_daily_inflows_data()),
        'daily_outflows_data': json.dumps(metrics.get_chart_daily_outflows_data()),
        'order_status_data': json.dumps(metrics.get_chart_order_status_data()),
    }
    return render(request, 'home.html', context) 