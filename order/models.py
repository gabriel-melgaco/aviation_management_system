from django.db import models
from django.contrib.auth.models import User
from aircraft.models import Aircraft
from inventory.models import Inventory
from item.models import Item


class Order(models.Model):
    ORDER_TYPE_CHOICES = [
        ("RMS", "RMS"),
        ("FSM", "FSM"),
        ("REQ", "REQ"),
    ]

    STATUS_CHOICES = [
        ("NOT", "Não enviado"),
        ("OPEN", "Aberto - Não Atendido"),
        ("OPEN2", "Aberto - Atendido Parcialmente"),
        ("CLOSE", "Finalizado - Atendido"),
        ("CLOSE2", "Finalizado - Não Atendido"),
        ("CANCEL", "Cancelado"),
    ]

    REQUESTER_CHOICES =[
        ("1BAVEX", "1º BAvEx"),
        ("BMS", "B Mnt Sup Av Ex"),

    ]

    order_number = models.IntegerField("Número do Pedido")
    order_year = models.IntegerField("Ano do Pedido", null=True, blank=True)
    order_date = models.DateField("Data do Pedido", null=True, blank=True)
    requester = models.CharField("Solicitante", choices=REQUESTER_CHOICES, max_length=500, null=True, blank=True)
    order_type = models.CharField("Tipo de Pedido", choices=ORDER_TYPE_CHOICES, max_length=500, null=True, blank=True)
    status = models.CharField("Status", choices=STATUS_CHOICES, max_length=500, null=True, blank=True)
    notes = models.TextField("Observações", blank=True, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders_created"
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders_updated"
    )

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Pedido {self.order_number}"
    



class OrderItem(models.Model):
    SERVICE_TYPE_CHOICES = [
        ("RUSH", "RUSH"),
        ("PROG", "PROG"),
        ("AOG", "AOG"),
    ]

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    inventory_item = models.ForeignKey(
        Inventory, on_delete=models.PROTECT, null=True, blank=True, related_name="order_items"
    )
    item_item = models.ForeignKey(
        Item, on_delete=models.PROTECT, null=True, blank=True, related_name="order_fms_items"
    )
    aircraft = models.ForeignKey(
        Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items"
    )
    aircraft_destination = models.ForeignKey(
        Aircraft, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items_aircraft_destination"
    )
    operator = models.CharField("Operador Pedido", max_length=500, null=True, blank=True)
    service_type = models.CharField("Tipo de Atendimento", choices=SERVICE_TYPE_CHOICES ,max_length=500, null=True, blank=True)
    quantity = models.PositiveIntegerField("Quantidade", default=1)
    quantity_supplied = models.PositiveIntegerField("Quantidade Fornecida", null=True, blank=True)
    dpe = models.CharField(max_length=500, null=True, blank=True)
    eglog = models.CharField(max_length=500, null=True, blank=True)
    log = models.BooleanField("Log Card", default=False)
    sn_attended = models.CharField(max_length=500, null=True, blank=True)
    expiration_date_attended = models.DateField("Data de Validade do Atendimento", null=True, blank=True)
    nf_answer = models.CharField("Nota Fiscal de Atendimento", max_length=500, null=True, blank=True)
    attended_date = models.DateField("Data de Atendimento", null=True, blank=True)
    collected = models.BooleanField("Coletado", default=False)
    gmm = models.CharField(max_length=500, null=True, blank=True)
    bms = models.CharField(max_length=500, null=True, blank=True)
    hb_destination = models.CharField("Destino HB", max_length=500, null=True, blank=True)
    contract_old = models.BooleanField("Contrato Anterior (013)?", default=False)
    reason = models.TextField("Motivo", null=True, blank=True)
    troubleshooting = models.TextField("Ação de Troubleshooting", null=True, blank=True)
    failure_description = models.TextField("Descrição da Falha", null=True, blank=True)
    observation = models.TextField("Observação do Item", null=True, blank=True)
    notes = models.TextField("Anotações sobre o Item", null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items_created"
    )
    tsn_item = models.DecimalField("TSN do Item", null=True, blank=True, max_digits=10, decimal_places=2)
    tso_item = models.DecimalField("TSO do Item", null=True, blank=True, max_digits=10, decimal_places=2)
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="order_items_updated"
    )

    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.item_item or self.inventory_item} ({self.quantity})"
