from pathlib import Path
from .common import get_website_dir
from flask import Blueprint, flash, jsonify, render_template, \
                  request, send_file, session
import json
import requests
from .kb_graph import graph, n, add_triple, generator_to_list, \
                     isolate_last_part_of_URI, input_new_triple, \
                     string_to_URI, triple_to_text, \
                     text_to_triple, save_graph

views = Blueprint('views', __name__)


def get_subjects(topic, relation, target=None):
    """ Get all the subjects of a relation for the given object. """  
    subs = graph.triples((None, relation, string_to_URI(topic)))
    return [isolate_last_part_of_URI(a[0]).replace("_", " ") for a in subs]

def get_attributes(topic, relation):
    atts = graph.triples((string_to_URI(topic), relation, None))
    return [isolate_last_part_of_URI(a[2]).replace("_", " ") for a in atts]


@views.route('/')
def home():

    methods_t = graph.triples((None, n.is_a, n.method))
    methods = [isolate_last_part_of_URI(m[0]) for m in methods_t]
    methods.sort() 

    apps_t = graph.triples((None, n.is_a, n.application))
    applications = [isolate_last_part_of_URI(a[0]) for a in apps_t]
    applications.sort() 

    return render_template('home.html', methods=methods,
                                        applications=applications)



@views.route('/topic/<string:topic>')
def topic(topic):

    # Title
    title = topic.replace("_", " ").title()
    print("Title:", title)


    # Description
    description = get_attributes(topic, n.description)
    print("Description:", description)

    # What it is - "is a"
    is_a_items = get_attributes(topic, n.is_a)
    print("Is a:", is_a_items)

    # Definition - "definition" 
    definitions = get_attributes(topic, n.definition)
    print("Definitions:", definitions)
    
    # Applications - "can do" - <object>
    # If the topic is a [method], list the applications it can do.
    applications = get_attributes(topic, n.can_do)
    print("Applications:", applications)

    # Methods - "can do" - <subject>
    methods = get_subjects(topic, n.can_do)
    print("Methods:", methods)

    # Advantages - "has advantage"
    advantages = get_attributes(topic, n.has_advantage)
    print("Advantages:", advantages)

    # Disadvantages - "has disadvantage"
    disadvantages = get_attributes(topic, n.has_disadvantage)
    print("Disdvantages:", disadvantages)

    # Examples - "example"
    examples = get_attributes(topic, n.example)
    print("Examples:", examples)


    return render_template("topic.html", 
                           description=description,
                           topic=topic, 
                           title=title,
                           is_a_items=is_a_items,
                           definitions=definitions,
                           applications=applications,
                           methods=methods,
                           advantages=advantages,
                           disadvantages=disadvantages,
                           examples=examples)


@views.route('/examples/<string:example>')
def example_page(example):
    return render_template("/examples/{}.html".format(example))


@views.route('/knowledge-base', methods=['GET', 'POST'])
def knowledge_base():
    """ 
    Knowledge Base page

    - See all the triples in the knowledge base
    - Manually add and remove triples 
    - Save the knowledge base to file "graph.n3"
    """
    # When "Enter" button is pressed:
    if request.method == 'POST':

        # Get user input from subject, predicate, and object fields
        subject = request.form.get("subject")
        predicate = request.form.get("predicate")
        obj = request.form.get("object")

        # Validate input
        if len(subject) == 0 or len(predicate) == 0 or len(obj) == 0:
            flash("Must enter a value in all three fields.", category="error")
        else:

            # Convert to RDF triple format
            s, p, o = input_new_triple(subject, predicate, obj)

            # Check if triple is already in the graph
            if (s, p, o) in graph:
                flash("Triple already exists", category="error")
            else:

                # Add the triple to the graph
                add_triple(s, p, o)
                print("\nJust added:\n", subject, " - ", predicate, " - ", obj,
                      "\nIn RDF format: ", s, p, o)

    # Load all the triples from the graph into a list, convert them into plain text, and sort them
    triples = []
    for s, p, o in graph:
        triples.append((s, p, o))
    triples.sort()
    triples_text = [triple_to_text(t) for t in triples]

    # Pass all the triples to the template to be displayed
    return render_template('knowledge-base.html', triples_text=triples_text)


@views.route('/download/<path:filepath>', methods=['GET', 'POST'])
def download(filepath):
    path = Path(get_website_dir()) / filepath
    return send_file(path, as_attachment=True)


@views.route('/recommender', methods=['GET', 'POST'])
def recommender():
    """ 
    Machine Learning Tool Recommender page

    - Select an application from the drop down menu
    - View the results that match the query ( ? , can do , [selected application] )
    """
    # Get all the applications to be listed in the drop down menu
    application_triples = graph.triples((None, n.is_a, n.application))
    applications = [isolate_last_part_of_URI(a[0]).replace("_", " ") for a in application_triples]
    applications.sort() 

    # Initialize defaults
    default_application_text = "e.g., 'image generation'"  # Placeholder in drop down menu
    selected_application = default_application_text        # Selection in drop down menu
    data = dict()                                          # Holds the results of the query

    # When "Get Recommendation" button is pressed:
    if request.method == 'POST':

        # Get the selected application from the drop down menu
        selected_application = request.form.get("applicationSelect")

        # Get all the methods that can do the selected application
        results = graph.triples((None, n.can_do, string_to_URI(selected_application)))
        relevant_methods = [r[0] for r in results]
        relevant_methods.sort()

        # For each method, get its:
        #  - name,
        #  - description, 
        #  - advantages,
        #  - disadvantages, and
        #  - links
        for method in relevant_methods:
            data[method] = dict()

            data[method]["name"] = isolate_last_part_of_URI(method).replace("_", " ").capitalize()

            data[method]["description"] = isolate_last_part_of_URI(graph.value(method, n.description))

            advantages = graph.triples((method, n.has_advantage, None))
            data[method]["advantages"] = [isolate_last_part_of_URI(a[2]).replace("_", " ") for a in advantages]

            disadvantages = graph.triples((method, n.has_disadvantage, None))
            data[method]["disadvantages"] = [isolate_last_part_of_URI(d[2]).replace("_", " ") for d in disadvantages]

            links = graph.triples((method, n.link, None))
            data[method]["links"] = [isolate_last_part_of_URI(l[2]) for l in links]

    # Pass the applications and the results (if any) to the recommender template to be displayed
    return render_template('recommender.html', default_application_text=default_application_text,
                                               applications=applications,
                                               selected_application=selected_application,
                                               data=data)


@views.route('/query', methods=['GET', 'POST'])
def query():
    """
    Custom Queries page

    - Choose any combination of subject, predicate, or object from the dropdown menu
    - Select '?' to act as a wildcard value
    - View all the triples that satisfy the query
    """
    # Gather all the unique subjects, predicates, and objects to be listed in their corresponding drop down menus
    subjects = generator_to_list(graph.subjects())
    predicates = generator_to_list(graph.predicates())
    objects = generator_to_list(graph.objects(), exclude_literals=True)

    # By default, set selection fields to the wildcard value
    wildcard_text = '?'
    selected_subject = wildcard_text
    selected_predicate = wildcard_text
    selected_obj = wildcard_text

    results_text = []

    # When "Submit" button is pressed:
    if request.method == 'POST':

        # Get the values from the drop down menus
        selected_subject = request.form.get('subjectSelect')
        selected_predicate = request.form.get('predicateSelect')
        selected_obj = request.form.get('objectSelect')

        # Convert the input into the necessary format, setting wildcards to None
        q_text = [selected_subject, selected_predicate, selected_obj]
        q = [None, None, None]
        for i in range(3):
            # For each of the three values (subject, predicate, object), if the selected
            #  value is not the wildcard value, convert it into a URI and replace the
            #  None placeholder in query q
            if q_text[i] != wildcard_text:
                q[i] = string_to_URI(q_text[i])

        # Query the knowledge base and convert the results to plain text in a sorted list
        results = graph.triples(tuple(q))
        results_text = [triple_to_text(t) for t in results]
        results_text.sort()

    # Pass all the values and results (if any) to the query template to be displayed
    return render_template('query.html', selected_subject=selected_subject,
                                         selected_predicate=selected_predicate,
                                         selected_obj=selected_obj,
                                         subjects=subjects, 
                                         predicates=predicates,
                                         objects=objects,
                                         results_text=results_text,
                                         wildcard_text=wildcard_text)


@views.route('/query-rag', methods=['GET', 'POST'])
def query_rag():
    """
    Query Knowledge Base Chatbot

    - Ask a natual-language question about the knowledge base to a chatbot

    Uses a RAG AI service running on AWS bedrock.
    """
    ROOT_URL = "https://mhkyeven3e3yrdzqa36g443c4q0xyqkm.lambda-url.us-east-1.on.aws/"
    answer = "-"
    if (session.get("last_query_id") is not None):
        print("Last question ID: [", session["last_query_id"], "]")
    else:
        session["last_query_id"] = ""
        print("Set last query ID to empty.")

    # When "Enter" button is pressed:
    if request.method == 'POST':

        # Get the question asked by the user
        question = request.form.get('question')

        #------------------------------------------------------------------------------
        # Send submit query POST request to route "/docs/submit_query"
        SUBMIT_QUERY_URL = ROOT_URL + "submit_query/"
        query_contents = {
            "query_text": question
        }

        response = requests.post(SUBMIT_QUERY_URL, json = query_contents)
        query_id = response.json()["query_id"]
        session["last_query_id"] = query_id

        #------------------------------------------------------------------------------
        # Wait to receive answer via GET request to route "/docs/get_query"
        import time
        GET_QUERY_URL = ROOT_URL + "get_query/"
        is_complete = False
        timeout_in_s = 120
        time_in_s = 0

        while not is_complete or time_in_s > timeout_in_s:
            # Wait for answer
            time.sleep(3)
            time_in_s += 3
            print("Waiting for answer...", time_in_s)

            query_contents = {
                "query_id": query_id
            }

            response = requests.get(GET_QUERY_URL, params = query_contents)

            is_complete = response.json()["is_complete"]
            if (is_complete):
                answer = response.json()["answer_text"]
            elif (time_in_s > timeout_in_s):
                print("Timeout.")
                

    elif session["last_query_id"] != "":
        GET_QUERY_URL = ROOT_URL + "get_query/"
        query_contents = {
            "query_id": session["last_query_id"]
        }
        response = requests.get(GET_QUERY_URL, params = query_contents)
        is_complete = response.json()["is_complete"]
        if (is_complete):
            answer = response.json()["answer_text"]


    # Pass all the values and results (if any) to the query template to be displayed
    return render_template('query-rag.html', answer=answer)


@views.route('/delete-triple', methods=['POST'])
def delete_triple():
    """ Delete the triple whose 'X' was clicked from the graph """
    triple = json.loads(request.data)
    triple_text = triple['triple']
    original_triple = text_to_triple(triple_text)
    graph.remove(original_triple)
    return jsonify({})


@views.route('/save-graph', methods=['GET', 'POST'])
def save():
    """ Save the graph """
    print("Saving...")
    save_graph()
    print("Saved.")
    return jsonify({})
