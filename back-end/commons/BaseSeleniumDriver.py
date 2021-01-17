from commons.BaseDriver import BaseDriver
from commons.Log import Log
from models.Chrome import Chrome


class BaseSeleniumDriver(BaseDriver):

    url = ''
    collection_name = 'default'
    tables = None

    def search(self):
        titles = []

        # Inicializando a sessão e pegando as tabelas
        Chrome.get_url(self.url, self.after_load_url)

        """ Pegando o select de seleção de localização """
        localizations = self.get_localizations()

        """ Interagindo sobre as localizações """
        idx = 0
        for localization in localizations:
            idx += 1
            Log.debug('Mudando a localização para {}. {} de {}'.format(localization, idx, len(localizations)))
            """ Selecionando a opção para processar as informações dela """
            self.select_option(localization)
            self.tables = Chrome.get_tables()

            for table in self.tables:
                self.process_table(table, titles, localization)

    def process_table(self, table, titles, localization):
        thead = Chrome.find_element_by_tag_name(table, "thead")
        all_tbody = Chrome.find_elements_by_tag_name(table, "tbody")

        """ Buscando as colunas. Tem sites que utilizam o td no lugar do th """
        ths = Chrome.find_elements_by_tag_name(thead, "th")
        if len(ths) <= 0:
            ths = Chrome.find_elements_by_tag_name(thead, "td")

        for th in ths:
            if th.text not in titles:
                titles.append(th.text)

        for tbody in all_tbody:
            trs_body = Chrome.find_elements_by_tag_name(tbody, "tr")
            for tr in trs_body:
                tds = Chrome.find_elements_by_tag_name(tr, "td")
                key = None

                if len(tds) <= 2:
                    continue

                for index, td in enumerate(tds):
                    if index >= len(titles):
                        continue

                    if 'hidden' in td.attrs:
                        continue

                    text_th = titles[index]

                    # pulando itens que não possuem texto. Ex: botões na tabela
                    if td.text == "" or td.text is None:
                        continue

                    if key is None:
                        key = td.text

                    if key not in self.columns:
                        self.columns[key] = {}

                    """ Se for um valor agrupar em princing, se não só adicionar como uma coluna """
                    if str(td.text).startswith('$'):
                        if 'pricing' not in self.columns[key]:
                            self.columns[key]['pricing'] = {}

                        if localization not in self.columns[key]['pricing']:
                            self.columns[key]['pricing'][localization] = {}

                        self.columns[key]['pricing'][localization][text_th] = td.text
                    else:
                        if text_th not in self.columns[key]:
                            self.columns[key][text_th] = {}

                        value = td.text

                        # Removendo parte dos valores que contém / para maquinas da azure
                        # Algumas máquina vem com um valor de cpu diferente, como por exemplo 2 / 4,
                        # nesses casos vamos considerar apenas o 2
                        if self.collection_name == 'azure':
                            items = str(td.text).split('/')
                            value = items[0]
                            if len(items) > 1 and str(td.text) != 'N/A':
                                Log.debug('Removendo parte do valor de ' + td.text + ' valor agora sera: ' + value)

                        self.columns[key][text_th] = value

    def after_load_url(self):
        pass

    def select_option(self, localization):
        raise NotImplementedError()

    def get_localizations(self):
        raise NotImplementedError()
