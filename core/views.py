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


# CODIGO AJUSTADO anterior a seguir

# from django.shortcuts import render
# from django.db.models import Count
# from django.db.models.functions import TruncDate, TruncHour
# from core.models import AccessLog
# import plotly.express as px
# import folium
# import pandas as pd
# from django.views.generic import TemplateView

# class DashboardMapView(TemplateView):
#     template_name = 'dashboard_map.html'

#     def get_context_data(self, **kwargs):
#         # Contexto do mapa
#         figure = folium.Figure()
        
#         # Coordenadas dos municípios
#         municipios_coordenadas = {
#             'João Pessoa': [-7.11532, -34.861],
#             'Mamanguape': [-6.830279074483519, -35.11999458809625],
#             'Guarabira': [-6.850598322874815, -35.49112792483982],
#             'Pedra Branca': [-7.421690, -38.068900]
#         }

#         # Carregar os dados do CSV
#         data = pd.read_csv('data/locais_de_servicos_do_governo_pb_att.csv')

#         # Extrair os municípios únicos
#         municipios = data['Municipio'].unique()

#         # Filtrar dados com base nos parâmetros da requisição
#         city = self.request.GET.get('city', 'todas')
#         local_type = self.request.GET.get('local_type', 'todos')

#         # Se o município for selecionado, filtra pelos dados correspondentes
#         if city != 'todas':
#             data = data[data['Municipio'] == city]

#         if local_type != 'todos':
#             data = data[data['Categoria'] == local_type]

#         # Se o município estiver no dicionário, centralizar no local correto
#         map_location = municipios_coordenadas.get(city, [-7.11532, -34.861])  # Default: João Pessoa

#         # Criar o mapa centralizado na cidade selecionada
#         map = folium.Map(
#             location=map_location,
#             zoom_start=11,
#             tiles='OpenStreetMap'
#         )

#         # Propriedades dos ícones dos marcadores por categoria
#         marker_properties = {
#             'Trânsito': {'icon': 'car', 'color': 'blue'},
#             'Educação': {'icon': 'graduation-cap', 'color': 'green'},
#             'Segurança': {'icon': 'shield', 'color': 'red'},
#         }

#         # Adicionar os marcadores no mapa
#         for index, row in data.iterrows():
#             folium.Marker(
#                 location=[row['Latitude'], row['Longitude']],
#                 popup=f"{row['Categoria'].capitalize()}: {row['Nome']} - {row['Endereco']}",
#                 tooltip=row['Nome'],  # Mostra o nome ao passar o mouse
#                 icon=folium.Icon(
#                     icon=marker_properties.get(row['Categoria'], {'icon': 'info', 'color': 'gray'})['icon'],
#                     color=marker_properties.get(row['Categoria'], {'icon': 'info', 'color': 'gray'})['color'],
#                     prefix='fa'
#                 )
#             ).add_to(map)

#         # Adicionar o mapa à figura
#         map.add_to(figure)
#         figure.render()

#         # Contexto do dashboard
#         total_accesses = AccessLog.objects.count()

#         accesses_by_service = (
#             AccessLog.objects
#             .values('service_name')
#             .annotate(total=Count('id'))
#         )

#         accesses_by_day = (
#             AccessLog.objects
#             .annotate(day=TruncDate('timestamp'))
#             .values('day')
#             .annotate(total=Count('id'))
#         )

#         accesses_by_hour = (
#             AccessLog.objects
#             .annotate(hour=TruncHour('timestamp'))
#             .values('hour')
#             .annotate(total=Count('id'))
#         )

#         # Criar gráficos
#         service_names = [access['service_name'] for access in accesses_by_service]
#         service_totals = [access['total'] for access in accesses_by_service]
#         fig_service = px.bar(x=service_names, y=service_totals, labels={'x': 'Serviço', 'y': 'Total de Acessos'}, title='Acessos por Serviço')
#         chart_service = fig_service.to_html(full_html=False)

#         days = [access['day'].strftime('%Y-%m-%d') for access in accesses_by_day]
#         day_totals = [access['total'] for access in accesses_by_day]
#         fig_day = px.line(x=days, y=day_totals, labels={'x': 'Dia', 'y': 'Total de Acessos'}, title='Acessos por Dia')
#         chart_day = fig_day.to_html(full_html=False)

#         hours = [access['hour'].strftime('%H:%M') for access in accesses_by_hour]
#         hour_totals = [access['total'] for access in accesses_by_hour]
#         fig_hour = px.line(x=hours, y=hour_totals, labels={'x': 'Hora', 'y': 'Total de Acessos'}, title='Acessos por Hora')
#         chart_hour = fig_hour.to_html(full_html=False)

#         context = {
#             'map': figure,
#             'total_accesses': total_accesses,
#             'chart_service': chart_service,
#             'chart_day': chart_day,
#             'chart_hour': chart_hour,
#             'municipios': municipios,
#             'selected_city': city,
#             'selected_category': local_type,
#             'locais': data.to_dict(orient='records'),  # Transforma o DataFrame em uma lista de dicionários
#         }
#         return context


from django.shortcuts import render
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncHour
from core.models import AccessLog
import plotly.express as px
import folium
import pandas as pd
from django.views.generic import TemplateView
import csv
import os


class DashboardMapView(TemplateView):
    template_name = 'dashboard_map.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Carregar dados do CSV
        data, municipios = self.carregar_dados('data/locais_de_servicos_atualizado_full.csv')

        # Coordenadas dos municípios
        municipios_coordenadas = self.carregar_municipios('data/cidades.csv')

        # Filtros baseados em parâmetros da requisição
        city = self.request.GET.get('city', 'todas')
        local_type = self.request.GET.get('local_type', 'todos')

        # Validar filtros
        city, local_type = self.validar_filtros(city, local_type, municipios, data)

        # Filtrar dados com base nos filtros aplicados
        data_filtrada = self.filtrar_dados(data, city, local_type)

        # Criar o mapa
        map_figure = self.criar_mapa(data_filtrada, city, municipios_coordenadas)

        # Obter gráficos e dados de dashboard
        context.update(self.obter_dados_dashboard())
        context['chart_service'], context['chart_day'], context['chart_hour'] = self.criar_graficos()

        # Adicionar outros contextos
        context.update({
            'map': map_figure,
            'municipios': municipios,
            'selected_city': city,
            'selected_category': local_type,
            'locais': data_filtrada.to_dict(orient='records'),
        })

        return context

    # ---------------------- Funções auxiliares ----------------------

    def carregar_municipios(self, caminho_csv):
        """
        Carrega municípios e suas coordenadas de um arquivo CSV.
        """
        municipios = {}
        if not os.path.exists(caminho_csv):
            raise FileNotFoundError(f"O arquivo {caminho_csv} não foi encontrado.")

        try:
            with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                colunas_esperadas = {'Cidade', 'latitude', 'longitude'}
                if not colunas_esperadas.issubset(leitor.fieldnames):
                    raise ValueError(f"O arquivo deve conter as colunas: {', '.join(colunas_esperadas)}")

                for linha in leitor:
                    try:
                        nome = linha['Cidade'].strip()
                        latitude = float(linha['latitude'])
                        longitude = float(linha['longitude'])
                        municipios[nome] = [latitude, longitude]
                    except (ValueError, KeyError) as e:
                        print(f"Erro ao processar a linha {linha}: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar municípios: {e}")

        return municipios

    def carregar_dados(self, caminho_csv):
        """
        Carrega os dados principais do CSV de localidades.
        """
        if not os.path.exists(caminho_csv):
            raise FileNotFoundError(f"O arquivo {caminho_csv} não foi encontrado.")
        data = pd.read_csv(caminho_csv)
        municipios = data['Municipio'].unique()
        return data, municipios

    def validar_filtros(self, city, local_type, municipios, data):
        """
        Valida os filtros de cidade e categoria.
        """
        if city not in list(municipios) + ['todas']:
            city = 'todas'
        if local_type not in list(data['Categoria'].unique()) + ['todos']:
            local_type = 'todos'
        return city, local_type

    def filtrar_dados(self, data, city, local_type):
        """
        Filtra os dados com base nos parâmetros fornecidos.
        """
        if city != 'todas':
            data = data[data['Municipio'] == city]
        if local_type != 'todos':
            data = data[data['Categoria'] == local_type]
        return data

    def criar_mapa(self, data, city, municipios_coordenadas):
        """
        Cria o mapa com marcadores.
        """
        map_location = municipios_coordenadas.get(city, [-7.11532, -34.861])  # Default: João Pessoa
        map = folium.Map(location=map_location, zoom_start=11, tiles='OpenStreetMap')

        marker_properties = {
            'Trânsito': {'icon': 'car', 'color': 'blue'},
            'Educação': {'icon': 'graduation-cap', 'color': 'green'},
            'Segurança': {'icon': 'shield', 'color': 'red'},
        }

        for index, row in data.iterrows():
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=f"{row['Categoria'].capitalize()}: {row['Nome']} - {row['Endereco']}",
                tooltip=row['Nome'],
                icon=folium.Icon(
                    icon=marker_properties.get(row['Categoria'], {'icon': 'info', 'color': 'gray'})['icon'],
                    color=marker_properties.get(row['Categoria'], {'icon': 'info', 'color': 'gray'})['color'],
                    prefix='fa'
                )
            ).add_to(map)

        figure = folium.Figure()
        map.add_to(figure)
        figure.render()
        return figure

    def obter_dados_dashboard(self):
        """
        Obtém os dados do dashboard, incluindo contagem total de acessos.
        """
        total_accesses = AccessLog.objects.count()

        accesses_by_service = (
            AccessLog.objects
            .values('service_name')
            .annotate(total=Count('id'))
        )

        return {
            'total_accesses': total_accesses,
            'accesses_by_service': accesses_by_service,
        }

    def criar_graficos(self):
        """
        Cria os gráficos de serviços, acessos por dia e acessos por hora.
        """
        accesses_by_day = (
            AccessLog.objects
            .annotate(day=TruncDate('timestamp'))
            .values('day')
            .annotate(total=Count('id'))
        )

        accesses_by_hour = (
            AccessLog.objects
            .annotate(hour=TruncHour('timestamp'))
            .values('hour')
            .annotate(total=Count('id'))
        )

        service_names = [access['service_name'] for access in self.obter_dados_dashboard()['accesses_by_service']]
        service_totals = [access['total'] for access in self.obter_dados_dashboard()['accesses_by_service']]
        fig_service = px.bar(x=service_names, y=service_totals, labels={'x': 'Serviço', 'y': 'Total de Acessos'}, title='Acessos por Serviço')
        fig_service.update_layout(template='plotly_white')

        days = [access['day'].strftime('%Y-%m-%d') for access in accesses_by_day]
        day_totals = [access['total'] for access in accesses_by_day]
        fig_day = px.line(x=days, y=day_totals, labels={'x': 'Dia', 'y': 'Total de Acessos'}, title='Acessos por Dia')

        hours = [access['hour'].strftime('%H:%M') for access in accesses_by_hour]
        hour_totals = [access['total'] for access in accesses_by_hour]
        fig_hour = px.line(x=hours, y=hour_totals, labels={'x': 'Hora', 'y': 'Total de Acessos'}, title='Acessos por Hora')

        return fig_service.to_html(full_html=False), fig_day.to_html(full_html=False), fig_hour.to_html(full_html=False)

