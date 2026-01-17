import datetime, os
from core import settings

import pandas as pd
from celery import shared_task

from .models import Outflow


@shared_task
def csv_outflows_generator():
    outflows = Outflow.objects.values(
        'id',
        'geladinho__flavor',
        'quantity',
        'selling_price_outflow',
        'description',
    )
    df = pd.DataFrame(outflows)

    sheets_dir = os.path.join(settings.MEDIA_ROOT, "sheets")
    os.makedirs(sheets_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"stock_outflows_{timestamp}.csv"
    path = os.path.join(sheets_dir, filename)

    df.to_csv(path, index=False)
    return path
