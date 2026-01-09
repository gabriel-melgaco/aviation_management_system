from django.contrib import admin
from .models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "order_date",
        "requester",
        "order_type",
        "status",
        "notes",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "order_number",
        "requester",
        "order_type",
        "status",
        "notes",
    )

    list_filter = (
        "order_type",
        "status",
        "order_date",
        "created_at",
    )

    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "service_type",
        "inventory_item",
        "operator",
        "item_item",
        "aircraft",
        "aircraft_destination",
        "quantity",
        "nf_answer",
        "attended_date",
        "collected",
        "gmm",
        "bms",
        "observation",
        "tsn_item",
        "tso_item",
        "hb_destination",
        "contract_old",
        "created_by",
        "updated_by",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "inventory_item__name",
        "aircraft_destination",
        "item_item__name",
        "order__service_type",       
        "inventory_item__tsn_item",  
        "inventory_item__tso_item",  
        "reason",
        "troubleshooting",
        "observation",
        "failure_description",
        "gmm",
        "operator",
        "bms",
        "hb_destination",
        "nf_answer",
    )

    list_filter = (
        "collected",
        "attended_date",
        "service_type",
        "tsn_item",
        "tso_item",
        "created_at",
        "updated_at",
        "aircraft",
        "order",
        "contract_old",
    )

    ordering = ("-created_at",)
