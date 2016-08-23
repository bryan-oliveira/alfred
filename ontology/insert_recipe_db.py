from rdflib import Namespace
from rdflib import Graph


g = Graph()
result = g.parse("alfred-ontology.owl")

namespace = Namespace("http://www.alfred-ai.com/recipe-ontology.owl#")

ingredient = namespace + 'ingredient'

print "Graph has %s statements." % len(g)

print namespace+"ingredient"

# for s, p, o in g:
#    print s, p, o

# for s, p, o in g.triples((None, None, namespace+"ingredient")):
#    print "%s is an ingredient" % s

query = """
    SELECT ?a ?b WHERE { ns:pepper ?a ?b . }
    """

print query

q = g.query(query, initNs={'ns': namespace})

for row in q:
    print row
