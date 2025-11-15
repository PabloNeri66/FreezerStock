from geladinhos.models import Geladinho
from django.db.models import Sum
from outflows.models import Outflow
from django.utils.formats import number_format


def get_geladinho_metrics():
    geladinhos = Geladinho.objects.all()
    total_cost_price = sum(geladinho.cost_price * geladinho.quantity for geladinho in geladinhos)
    total_selling_price = sum(geladinho.selling_price * geladinho.quantity for geladinho in geladinhos)
    total_quantity = sum(geladinho.quantity for geladinho in geladinhos)
    total_profit = total_selling_price - total_cost_price

    return dict(
        total_cost_price=number_format(
            total_cost_price, decimal_pos=2, force_grouping=True
        ),
        total_selling_price=number_format(
            total_selling_price, decimal_pos=2, force_grouping=True
        ),
        total_profit=number_format(
            total_profit, decimal_pos=2, force_grouping=True
        ),
        total_quantity=total_quantity,
    )


def get_sales_metrics() -> dict:
    outflows = Outflow.objects.all().select_related(
        'geladinho'
    ).only(
        "quantity",
        "selling_price_outflow",
        "geladinho__selling_price",
        "geladinho__cost_price"
    )
    total_sales = Outflow.objects.count()

    total_geladinhos_sold = Outflow.objects.aggregate(
        total_geladinhos_sold=Sum("quantity")
    )["total_geladinhos_sold"] or 0

    total_sales_value = sum(
        outflow.quantity * (
            outflow.selling_price_outflow if outflow.selling_price_outflow else outflow.geladinho.selling_price
        )
        for outflow in outflows
    ) or 0

    total_sales_cost = sum(
        outflow.quantity * outflow.geladinho.cost_price for outflow in outflows
    ) or 0

    total_sales_profit = total_sales_value - total_sales_cost

    return dict(
        total_sales=total_sales,
        total_geladinhos_sold=total_geladinhos_sold,
        total_sales_profit=total_sales_profit,
        total_sales_value=total_sales_value,
    )