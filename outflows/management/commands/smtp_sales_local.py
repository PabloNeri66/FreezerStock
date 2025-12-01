import datetime, os

from django.core.management.base import BaseCommand
from django.core.mail import EmailMessage
from outflows.models import Outflow


class Command(BaseCommand):
    """
Management command Django para gerar e enviar o Relatório Diário de Vendas por e-mail.

Este comando permite gerar um relatório das vendas de um dia específico,
passado como argumento ao chamar o comando, e envia o relatório por e-mail
para o endereço configurado na variável de ambiente EMAILTO.

O usuário deve fornecer o dia do relatório (número de 1 a 31) como argumento.
Caso o dia informado seja maior que o dia atual do mês, o comando ajusta o mês
automaticamente para o mês anterior. Isso permite gerar relatórios de até 30 dias
retroativos. Por exemplo, se hoje é 1 de dezembro e o usuário informa dia 2,
o comando irá gerar o relatório para 2 de novembro.

Classes e métodos:

Command(BaseCommand):
    add_arguments(parser):
        Adiciona o argumento obrigatório 'Dia do Relatório', que deve ser
        um número representando o dia do mês para o qual deseja-se gerar o relatório.

    handle(*args, **options):
        Ponto de entrada do comando. Recebe o dia do relatório, ajusta a data
        considerando o mês/ano correto, busca os dados das vendas e envia o e-mail.

    date_fix_daily_report(daily_report) -> str:
        Ajusta o dia do relatório passado pelo usuário para a data completa
        no formato YYYY-MM-DD. Trata casos em que o dia informado é maior
        que o dia atual, ajustando o mês e ano corretamente.

    search_data_for_daily_report(date_fixed) -> dict:
        Consulta no banco de dados todas as vendas (Outflow) do dia especificado.
        Utiliza select_related('geladinho') para evitar queries N+1 ao acessar
        informações do produto (Geladinho) relacionado.

    model_smtp(daily_report_data, date_fixed):
        Constrói e envia o e-mail com o relatório diário.
        - daily_report_data: dicionário contendo os registros de vendas do dia.
        - date_fixed: data completa do relatório (YYYY-MM-DD) para exibir no corpo do e-mail.
        Formata a data/hora de cada venda para leitura mais amigável (dd/mm/yyyy HH:MM:SS).
"""

    def add_arguments(self, parser):
        parser.add_argument(
            'Dia do Relatório',
            type=str,
            help='''
            para gerar o relatório de hoje -> XX
            por exemplo: hoje dia 1/12/25, digite 1.
            ''',
        )

    # Onde ocorre a parada mesmo
    def handle(self, *args, **options):
        daily_report = options['Dia do Relatório']

        date_fixed = self.date_fix_daily_report(daily_report)  # recebe retorno

        daily_report_data = self.search_data_for_daily_report(date_fixed)

        self.model_smtp(daily_report_data, date_fixed)

    def date_fix_daily_report(self, daily_report):
        today = datetime.date.today()
        date = str(today)

        daily_report_list = list(daily_report)
        date_list = list(date)

        current_day = int(date_list[-2] + date_list[-1])

        report_day = int(daily_report)

        if report_day > current_day:
            month = int(date_list[5] + date_list[6])
            month -= 1
            if month == 0:
                month = 12
                year = int("".join(date_list[0:4])) - 1
                year_str = f"{year:04d}"
                date_list[0:4] = list(year_str)

            month_str = f"{month:02d}"
            date_list[5] = month_str[0]
            date_list[6] = month_str[1]

        date_list[-2] = daily_report_list[0]
        date_list[-1] = daily_report_list[1]

        # transformar de volta:
        date_fixed = "".join(date_list)

        return date_fixed

    def search_data_for_daily_report(self, date_fixed):
        daily_values = Outflow.objects.filter(
            created_at__date=date_fixed
        ).select_related('geladinho')
        daily_report_data = dict(
            daily_values=daily_values
        )

        return daily_report_data

    def model_smtp(self, daily_report_data, date_fixed):

        # --- Dados do relatório ---
        daily_outflows = daily_report_data["daily_values"]

        # --- Assunto ---
        subject = "Relatório Diário de Vendas"

        # --- Corpo do e-mail ---
        body_lines = [
            f"Olá, segue o relatório do dia {date_fixed}:\n",
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
