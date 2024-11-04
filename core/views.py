# from django.shortcuts import render
# import plotly.express as px
# import pandas as pd

# from core.forms import DateForm
# from core.models import CO2

# def chart(request):
#     start = request.GET.get('start')
#     end = request.GET.get('end')

#     # Obtenha os dados do modelo CO2 e aplique filtros, se houver
#     co2 = CO2.objects.all()
#     if start:
#         co2 = co2.filter(date__gte=start)
#     if end:
#         co2 = co2.filter(date__lte=end)

#     # Converta os dados filtrados em um DataFrame para o Plotly
#     df = pd.DataFrame(list(co2.values('date', 'average')))

#     # Verifique se o DataFrame não está vazio para evitar erros ao plotar
#     if not df.empty:
#         fig = px.line(
#             df,
#             x='date',
#             y='average',
#             title="CO2 PPM",
#             labels={'date': 'Date', 'average': 'CO2 PPM'}
#         )
#         fig.update_layout(
#             title={
#                 'font_size': 24,
#                 'xanchor': 'center',
#                 'x': 0.5
#             }
#         )
#         chart = fig.to_html()
#     else:
#         chart = "<p>No data available for the selected date range.</p>"

#     context = {'chart': chart, 'form': DateForm()}
#     return render(request, 'core/chart.html', context)



from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncHour
from core.models import AccessLog
import plotly.express as px
import plotly.io as pio

def dashboard(request):
    # Total de acessos
    total_accesses = AccessLog.objects.count()

    # Acessos por serviço
    accesses_by_service = (
        AccessLog.objects
        .values('service_name')
        .annotate(total=Count('id'))
    )

    # Acessos por dia
    accesses_by_day = (
        AccessLog.objects
        .annotate(day=TruncDate('timestamp'))
        .values('day')
        .annotate(total=Count('id'))
    )

    # Acessos por hora
    accesses_by_hour = (
        AccessLog.objects
        .annotate(hour=TruncHour('timestamp'))
        .values('hour')
        .annotate(total=Count('id'))
    )

    # Criar gráfico de acessos por serviço
    service_names = [access['service_name'] for access in accesses_by_service]
    service_totals = [access['total'] for access in accesses_by_service]

    fig_service = px.bar(x=service_names, y=service_totals, labels={'x': 'Serviço', 'y': 'Total de Acessos'}, title='Acessos por Serviço')
    chart_service = fig_service.to_html(full_html=False)

    # Criar gráfico de acessos por dia
    days = [access['day'] for access in accesses_by_day]
    day_totals = [access['total'] for access in accesses_by_day]

    fig_day = px.line(x=days, y=day_totals, labels={'x': 'Dia', 'y': 'Total de Acessos'}, title='Acessos por Dia')
    chart_day = fig_day.to_html(full_html=False)

    # Criar gráfico de acessos por hora
    hours = [access['hour'] for access in accesses_by_hour]
    hour_totals = [access['total'] for access in accesses_by_hour]

    fig_hour = px.line(x=hours, y=hour_totals, labels={'x': 'Hora', 'y': 'Total de Acessos'}, title='Acessos por Hora')
    chart_hour = fig_hour.to_html(full_html=False)

    context = {
        'total_accesses': total_accesses,
        'chart_service': chart_service,
        'chart_day': chart_day,
        'chart_hour': chart_hour,
    }
    
    return render(request, 'core/dashboard.html', context)
