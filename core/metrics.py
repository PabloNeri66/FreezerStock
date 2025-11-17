from geladinhos.models import Geladinho
from django.db.models import Sum, F, Case, When
from outflows.models import Outflow
from django.utils.formats import number_format
from django.utils import timezone
from django.db.models.functions import TruncDate


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


def get_daily_sales_data():
    today = timezone.now().date()
    dates = [today - timezone.timedelta(days=i) for i in range(6, -1, -1)]
    values = list()

    for date in dates:
        sales_total = (
            Outflow.objects
            .filter(created_at__date=date)
            .select_related("geladinho")  # Evita consultas adicionais
            .aggregate(
                total_sales=Sum(
                    Case(
                        When(
                            selling_price_outflow__isnull=False,
                            then=F("selling_price_outflow") * F("quantity")
                        ),
                        default=F("geladinho__selling_price") * F("quantity"),
                    )
                )
            )["total_sales"] or 0
        )
        values.append(float(sales_total))

    return dict(
        dates=[str(d) for d in dates],
        values=values,
    )
