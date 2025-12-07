import os, datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from outflows.models import Outflow


class Command(BaseCommand):
    def handle(self, *args, **options):
        report_date = datetime.date.today()

        # Busca dados no banco
        daily_report_query_data = self.query_data_for_daily_report(
            report_date
        )

        # Envia e-mail
        self.model_smtp(daily_report_query_data, report_date)

    def query_data_for_daily_report(self, report_date):
        daily_values = Outflow.objects.filter(
            created_at__date=report_date
        ).select_related('geladinho')
        daily_report_query_data = dict(
            daily_values=daily_values
        )

        return daily_report_query_data

    def model_smtp(self, daily_report_query_data, report_date):

        # --- Dados do relatório ---
        daily_outflows = daily_report_query_data["daily_values"]

        # --- Assunto ---
        subject = "Relatório Diário de Vendas"

        # --- Corpo do e-mail ---
        body_lines = [
            f"Olá, segue o relatório do dia {report_date}:\n",
            "-------------------------------------",
        ]

        if not daily_outflows:
            body_lines.append("Nenhuma venda registrada neste dia.")
        else:
            for outflow in daily_outflows:
                body_lines.append(
                    f'Registro ID: {outflow.id} | Produto: {outflow.geladinho.flavor} | '
                    f'Qtd: {outflow.quantity} | Valor: {outflow.selling_price_outflow} | '
                    f'Data e Hora: {timezone.localtime(outflow.created_at).strftime("%d/%m/%Y %H:%M:%S")}'
                )


        body_lines.append('-------------------------------------')
        body_lines.append('Relatório automático gerado pelo sistema')

        body = '\n'.join(body_lines)

        to = [os.getenv('EMAILTO')]

        email = EmailMessage(
            subject=subject,
            body=body,
            to=to
        )

        email.send(fail_silently=False)

        self.stdout.write(
            self.style.SUCCESS(f"Relatório enviado para {to[0]} com sucesso!")
        )
