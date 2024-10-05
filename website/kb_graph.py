import os
import pathlib
from rdflib import Graph, Namespace, Literal, URIRef
from .common import get_website_dir


# The "knowledge base"
graph = Graph()

# This string acts as the prefix to all URIs in the knowledge base
namespace_string = "http://JamesButcher_ML_KnowledgeBase.org/"

# You can use n as a shorthand prefix when defining a URI in the code.
#  Instead of writing out "http://JamesButcher_ML_KnowledgeBase.org/regression",
#  you can write n.regression and it will create a URI identical to the above.
n = Namespace(namespace_string)

# When serializing the graph into a file format such as n3, use "mykb" as the prefix
graph.bind("mykb", n)

# For easy removal of poorly-entered triples - see remove_last_triple() method
last_added_triple = None



def get_graph_path(format="n3"):
    return os.path.join(get_website_dir(), "graph.{}".format(format))


def save_graph(save_format="n3"):
    """ Save graph file """
    #graph.serialize(destination="graph.{}".format(save_format), format=save_format)
    graph.serialize(destination=get_graph_path().format(save_format), format=save_format)
    print("Saved graph as graph.{}".format(save_format))


def load_graph(load_format=None):
    """ Load saved graph file """

    # script_dir = os.path.dirname(os.path.abspath(__file__))

    # script_dir = script_dir.replace("\\\\wsl.localhost\\", "\\\\")

    # print("Script dir:", script_dir, "\n")

    # Construct the path to the graph file relative to the script directory
    #graph_file = os.path.join(script_dir, "graph.n3")
    graph_file = get_graph_path()
    print("graph file: ", graph_file, "\n")

    # Load the graph using rdflib
    graph.parse(location=graph_file, format="n3")
    return



    root = pathlib.Path(os.getcwd())
    print("Working directory:", root, "\n")
    filename = pathlib.Path("graph.n3")
    graph.parse(location="./graph.n3")
    return

    # By default, try some common graph file extensions
    if load_format is None:
        load_formats = ["nt", "n3", "turtle", "xml", "pretty-xml"]
        for f in load_formats:
            try:
                #graph.parse("graph.n3", None, format=f)
                #graph.load("graph.{}".format(f), format=f)
                
                
                #print("Working directory:", os.getcwd(), "\n")

                root = pathlib.Path(os.getcwd())
                print("Working directory:", root, "\n")

                #graph_path = "graph.{}".format(f)
                #graph_path = os.getcwd() + "graph.{}".format(f)
                graph_name = "graph.{}".format(f)
                graph_path = root / graph_name
                print("Graph path:", graph_path, "\n")

                graph.load(graph_name, format=f)
                #graph.parse(graph_name)
                print("Loaded file", graph_name)
                return True
            
            # except FileNotFoundError:
            #     pass
            except Exception:
                pass
        print("No graph found.")
        return False
    # If a specific graph file extension is passed as an argument, try that one
    else:
        try:
            graph.load("graph.{}".format(load_format), format=load_format)
            print("Loaded file 'graph.{}'".format(load_format))
            return True
        except FileNotFoundError:
            print("Graph file 'graph.{}' not found.".format(load_format))
            return False



#-----------------------------------------------------------------------------------------------------
# Query functions
#-----------------------------------------------------------------------------------------------------

def get_all_topics():
    topics_set = set()
    for (s, _, _) in graph.triples((None, None, None)):
        topics_set.add(isolate_last_part_of_URI(s))
    topics = list(topics_set)
    topics.sort()
    return topics

# def get_objects(topic, relation, target=None):
#     """ Get all the objects of a relation for the given subject. """  
#     objs = graph.triples((string_to_URI(topic), relation, target))
#     return [isolate_last_part_of_URI(a[2]).replace("_", " ") for a in objs]

# def get_subjects(topic, relation, target=None):
#     """ Get all the subjects of a relation for the given object. """  
#     subs = graph.triples((target, relation, string_to_URI(topic)))
#     return [isolate_last_part_of_URI(a[0]).replace("_", " ") for a in subs]


#-----------------------------------------------------------------------------------------------------
# Conversion Functions
#-----------------------------------------------------------------------------------------------------

def isolate_last_part_of_URI(uri):
    """ Get the substring at the end of the URI after the last '/' """
    if isinstance(uri, Literal):
        return uri
    if uri is None:
        return ""
    return uri[uri.rfind('/')+1 : ]


def string_to_URI(s):
    """ Convert a string to a URIRef

     Example: "Machine Learning" -->  URIRef(http://JamesButcher_ML_KnowledgeBase.org/Machine_Learning)
    """
    if s is None:
        return None
    # If the string is enclosed in quotes, turn it into a Literal
    if (s[0] == '"' and s[-1] == '"') or (s[0] == "'" and s[-1] == "'"):
        s = s.replace('"', '')
        s = s.replace("'", "")
        return Literal(s)
    else:
        uri_string = namespace_string + s.replace(' ', '_')
        return URIRef(uri_string)


def triple_to_text(triple):
    """ Convert a triple into three plain-language strings separated by dashes """
    # If the 3rd part of the triple (the object) is a Literal, enclose it in quotes
    obj = triple[2]
    if isinstance(obj, Literal):
        obj = '"' + obj + '"'
    else:
        obj = isolate_last_part_of_URI(obj).replace('_', ' ')

    return isolate_last_part_of_URI(triple[0]).replace('_', ' ') + ' ---- ' + \
           isolate_last_part_of_URI(triple[1]).replace('_', ' ') + ' ---- ' + \
           obj


def text_to_triple(triple_text):
    """ Convert a plain-text triple into a regular triple with URIs (or a Literal) """
    elements = triple_text.split(' ---- ')
    s = string_to_URI(elements[0])
    p = string_to_URI(elements[1])
    o = string_to_URI(elements[2])
    triple = (s, p, o)
    return triple


# def text_to_triple(s_text, p_text, o_text):
#     """ Convert a plain-text triple into a regular triple with URIs (or a Literal) """
#     s = string_to_URI(s_text)
#     p = string_to_URI(p_text)
#     o = string_to_URI(o_text)
#     triple = (s, p, o)
#     return triple


#-----------------------------------------------------------------------------------------------------
# Adding and Removing Triples
#-----------------------------------------------------------------------------------------------------

def input_new_triple(subject, predicate, obj):
    """ Process raw string triple input into RDF format and return """
    # Validate input
    if subject is None or predicate is None or obj is None or \
        len(subject) == 0 or len(predicate) == 0 or len(obj) == 0:
        print("\nERROR - missing an input\n")

    # Process subject and convert to URI
    subject = subject.strip().lower().replace(' ', '_')
    subject = string_to_URI(subject)

    # Process predicate and convert to URI
    predicate = predicate.strip().lower().replace(' ', '_')
    predicate = string_to_URI(predicate)

    # Process object - Make the object a Literal if enclosed in quotes or is
    # a link, otherwise make it a URI
    if (obj[0] == '"' and obj[-1] == '"') or (obj[0] == "'" and obj[-1] == "'") or "/" in obj:
        obj = obj.strip("\"'")
        obj = Literal(obj)
    else:
        obj = string_to_URI(obj)

    return subject, predicate, obj


def add_triple(subject, predicate, obj):
    """ Add a (subject, predicate, obj) triple to the graph """
    new_triple = (subject, predicate, obj)
    if new_triple not in graph:
        graph.add(new_triple)
        print("\nAdded triple: ", triple_to_text(new_triple))
    else:
        print("\nTriple already exists!")


def remove_triple(triple):
    if triple in graph:
        graph.remove(triple)
        print("\nRemoved triple: ", triple_to_text(triple))
    else:
        print("\nCan't remove triple, not found:", triple_to_text(triple))


def remove_last_triple():
    """ Remove the most recently added triple during this session """
    if last_added_triple:
        graph.remove(last_added_triple)
    print("\nRemoved last triple: ", triple_to_text(last_added_triple))


#-----------------------------------------------------------------------------------------------------
# Queries and Other Output Functions
#-----------------------------------------------------------------------------------------------------

def take_query():
    """ Take a non-SPARQL rdflib pattern matching "query" input and output the results """

    q = input("\nEnter a query as three words separated by spaces. Use keyword 'what' in place of the variables you want to query.\n" +
              " Example:   'what can_do classification'   -->   gets all the things that can do classification\n\n")
    if q == "e": return
    input_values = q.split(" ")
    # Reprompt user for correct input if not three strings separated by spaces
    while len(input_values) != 3:
        print("You must enter exactly three strings separated by spaces. Use underscores if necessary. Try again or enter 'e' to end query.")
        q = input(" -- : ")
        if q == "e": return
        input_values = q.split(" ")
        print()

    # Change any 'what' keywords to None. None acts as the wildcard for rdflib triple pattern matching
    s, p, o = input_values
    if s.lower() == "what": s = None
    if p.lower() == "what": p = None
    if o.lower() == "what": o = None

    # Run the pattern matching "query" and print the results
    results = graph.triples((string_to_URI(s), string_to_URI(p), string_to_URI(o)))
    print("\nResults:\n")
    for r in results:
        print(triple_to_text(r))
    print()


def print_graph():
    """ Print the contents of the entire graph in both serialized format and plain-language format """
    print("\n--- Graph Contents: ---\n")
    print(" - In n3 format:\n")
    print(graph.serialize(format="n3").decode("utf-8"))

    print(" - In plain text format:\n")
    triples = []
    # Sort the triples by subject
    for s, p, o in graph:
        triples.append((s, p, o))
        triples.sort()
    for triple in triples:
        print(triple_to_text(triple))
    print()


def generator_to_list(generator, exclude_literals=False):
    """ Convert a graph generator object such as g.subjects() to a list with distinct text elements """
    item_list = []
    for i in generator:
        # If exclude_literals is set to True, skip over any Literals and add only URIs
        if exclude_literals and isinstance(i, Literal):
            continue
        if i not in item_list:
            item_list.append(i)
    item_text_list = [isolate_last_part_of_URI(i).replace('_', ' ') for i in item_list]
    item_text_list.sort()
    return item_text_list
