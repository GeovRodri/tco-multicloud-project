import os
import requests
from django.shortcuts import render
from django.views.generic import FormView
from website.forms import PesquisaForm
from website.sparql_query import SparqlQuery
from website.tco.tco_calculator import CalculadoraTco


class Pesquisa(FormView):
    template_name = 'index.html'
    form_class = PesquisaForm

    def form_valid(self, form):
        data = form.data
        sparql_query = SparqlQuery()
        ontology = sparql_query.search()

        request_body = {
            "select": ontology,
            "labels": ['cpu', 'hd', 'pricing', 'ram'],
            "filters": [],
            "limit": 10# data['limit']
        }

        if data['cpu'] is not None and data['cpu'] != '':
            request_body['filters'].append(
                # {"field": "cpu", "comparator": data['cpu_filter'], "value": int(data['cpu'])}
                {"field": "cpu", "comparator": '>=', "value": int(data['cpu'])}
            )

        # if data['hd'] is not None and data['hd'] != '':
        #     request_body['filters'].append(
        #         {"field": "hd", "comparator": data['hd_filter'], "value": int(data['hd'])}
        #     )

        if data['ram'] is not None and data['ram'] != '':
            request_body['filters'].append(
                # {"field": "ram", "comparator": data['ram_filter'], "value": int(data['ram'])}
                {"field": "ram", "comparator": '>=', "value": int(data['ram'])}
            )

        request = requests.post(f'http://{os.environ["BACKEND_HOST"]}:8080/', json=request_body)
        machines = request.json()

        ''' Adicionar o item que corresponde a maquina fisica '''
        calculadora_tco = CalculadoraTco()
        machines.append(calculadora_tco.calcular(data['ram'], data['hd'], data['cpu']))

        return render(self.request, 'listagem.html', {'machines': machines})
