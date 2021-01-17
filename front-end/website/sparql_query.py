from owlready2 import *


class SparqlQuery:
    vms = ["alibaba", "aws", "azure", "google"]

    def __init__(self):
        onto_path.append("./website/ontologia")
        default_world.get_ontology("CloudIaaS3.owl").load()

        sync_reasoner()  # reasoner is started and synchronized here
        self.graph = default_world.as_rdflib_graph()

    def search(self):
        iaas_provider = {}

        for provider in SparqlQuery.vms:
            iaas_provider[provider] = []

            query = """
                            PREFIX b:<http://www.semanticweb.org/gilberto/ontologies/2019/4/CloudIaaS#>
                            SELECT DISTINCT ?o
                            WHERE  {{
                            b:{} ?p ?s .
                            ?s rdfs:comment ?o .
                            }} """.format(provider)

            results_list = self.graph.query(query)
            for item in results_list:

                o = str(item['o'].toPython())
                o = re.sub(r'.*#', "", o)

                iaas_provider[provider].append(o)

        return iaas_provider
