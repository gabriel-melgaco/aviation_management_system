from inventory.models import Inventory
from order.models import Order
from outflow.models import Outflow
from inflow.models import Inflow
from order.models import Order
from datetime import date
from datetime import timedelta
from django.db.models import F, Sum
from django.utils import timezone




def get_inventory_metrics():
    total_itens = Inventory.objects.all().count()

    itens_expirated = Inventory.objects.filter(expiration_date__lt=date.today()).count()


    itens_minimum = Inventory.objects.filter(quantity__lte=F('minimum_quantity')).count()


    inventory_metrics = {
        'total_itens': total_itens,
        'itens_expirated': itens_expirated,
        'itens_minimum': itens_minimum,
    }

    return inventory_metrics


def get_order_metrics():
    total_orders = Order.objects.all().count()

    open_orders = Order.objects.filter(status__in=['OPEN', 'OPEN2']).count()

    order_metrics = {
        'total_orders': total_orders,
        'open_orders': open_orders,
    }
    
    return order_metrics


def get_inflow_outflow_metrics(date):

    if date:
        year = date.year
        month = date.month
        total_outflows = sum(outflow.quantity for outflow in Outflow.objects.filter(created_at__year=year,created_at__month=month))
        total_inflows = sum(inflow.quantity for inflow in Inflow.objects.filter(created_at__year=year,created_at__month=month))
    else:
        total_outflows = sum(outflow.quantity for outflow in Outflow.objects.all())
        total_inflows = sum(inflow.quantity for inflow in Inflow.objects.all())

    inflow_outflow_metrics = {
        'total_outflows': total_outflows,
        'total_inflows': total_inflows,
    }

    return inflow_outflow_metrics


def get_chart_daily_inflows_data():
    today = timezone.localdate()
    dates = [(today - timedelta(days=i)).strftime('%d/%m') for i in range(6, -1, -1)]
    values = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        total_items = sum(inflow.quantity for inflow in Inflow.objects.filter(created_at__date=day))
        values.append(total_items)

    return {
        "dates": dates,
        "values": values,
    }

def get_chart_daily_outflows_data():
    today = timezone.localdate()
    dates = [(today - timedelta(days=i)).strftime('%d/%m') for i in range(6, -1, -1)]
    values = []

    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        total_items = sum(outflow.quantity for outflow in Outflow.objects.filter(created_at__date=day))
        values.append(total_items)

    return {
        "dates": dates,
        "values": values,
    }

def get_chart_order_status_data():
    keys = [choice[0] for choice in Order.STATUS_CHOICES]
    labels = [choice[1] for choice in Order.STATUS_CHOICES]

    values = []

    for k in keys:
        value = Order.objects.filter(status=k).count()
        values.append(value)

    return {
        "labels":labels,
        "keys": keys,
        "values": values,
    }