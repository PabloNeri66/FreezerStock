import os, datetime

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from outflows.models import Outflow


class Command(BaseCommand):
    """
    Comando Django para gerar e enviar Relatório Diário de Vendas.
    Uso manual: permite informar o dia do relatório (1 a 31).
    Caso o dia seja maior que o dia atual, o comando ajusta mês/ano automaticamente.
    Idealmente usado pelo envio automático diário (via GitHub Actions ou Celery), 
    mas pode ser usado manualmente caso o automático falhe.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--dia',  # opcional, para uso manual
            type=int,
            help='Dia do relatório (1-31). Se não informado, usa o dia atual.'
        )

    def handle(self, *args, **options):
        # Se o dia não for informado, usar o dia atual
        day_input = options.get('dia')
        if day_input:
            if not (1 <= day_input <= 31):
                self.stdout.write(self.style.ERROR("Dia inválido. 1 a 31."))
                return
            daily_report_day = int(day_input)
        else:
            daily_report_day = int(datetime.date.today().day)

        # Ajusta data completa YYYY-MM-DD
        report_date = self.date_fix_daily_report(daily_report_day)

        # Busca dados no banco
        daily_report_query_data = self.query_data_for_daily_report(
            report_date
        )

        # Envia e-mail
        self.model_smtp(daily_report_query_data, report_date)

    def date_fix_daily_report(self, daily_report_day: int) -> str:
        """
        Recebe um dia (1-31) e retorna uma string YYYY-MM-DD.
        - Se o dia informado for maior que o dia atual, assume que é do mês anterior.
        - Ajusta ano automaticamente se passar de dezembro para novembro/ano anterior.
        """
        today = datetime.date.today()
        report_day = daily_report_day

        # assume o mesmo mês e ano inicialmente
        report_date = today.replace(day=report_day)

        # se o dia informado é maior que o dia atual, retrocede um mês
        if report_day > today.day:
            # retroceder um mês, ajustando ano se necessário
            if today.month == 1:
                month = 12
                year = today.year - 1
            else:
                month = today.month - 1
                year = today.year

            # garante que o dia não exceda o último dia do mês
            try:
                report_date = datetime.date(year, month, report_day)
            except ValueError:
                # se dia inválido para o mês, pega último dia do mês
                next_month = datetime.date(year, month + 1, 1) if month < 12 else datetime.date(year + 1, 1, 1)
                report_date = next_month - datetime.timedelta(days=1)

        return report_date.strftime("%Y-%m-%d")

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
                    f'Registro ID: {outflow.id} | Produto: {outflow.geladinho.flavor} | Qtd: {outflow.quantity} | Valor: {outflow.selling_price_outflow} | Data e Hora: {outflow.created_at.strftime("%d/%m/%Y %H:%M:%S")} '
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
