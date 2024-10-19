# AI-Knowledge-Base

### A web app for managing and accessing my personally-curated collection of machine learning knowledge, encoded as an RDF knowledge graph
Version 2.1
October 2024
by James Butcher
jmsbutcher1576@gmail.com

Access the site here: <a href="https://aikb-bfe2tw67tq-ue.a.run.app/" target="_blank" rel="noopener">AI Knowledge Base</a>

[https://aikb-bfe2tw67tq-ue.a.run.app/](https://aikb-bfe2tw67tq-ue.a.run.app/)

## Overview:

Artificial Intelligence Knowledge Base

- A web app designed to easily manage and access a knowledge base
- The knowledge base is intended for my collection of machine learning knowledge, but can be used for any other domain as well.

5 pages:
- Home page: Introduction and instructions on how to use
- Knowledge base: Add and remove RDF triples
- Recommender: Select an application and get info on ML methods that can do it
- Custom Query: Make simple queries on the knowledge base
- Ask Chatbot: Chat with a RAG (Retrieval-Augmented Generation) service running on AWS that uses the knowledge base material as context.

Thanks to Tech with Tim for this YouTube video to help get the basics of the original website working:

- <i>Python Website Full Tutorial - Flask, Authentication, Databases & More by Tech With Tim</i> Feb 1, 2021 https://www.youtube.com/watch?v=dam0GPOAvVI&list=PLwGZ7X2gMChQbGLrYP57YW2S_lrknkw1_&index=57

I deployed the app to the web using Google Cloud Run.

My introduction to the subject of ontology, knowledge graphs, and RDF came from the online course I took
for my MCS - Masters of Computer Science degree from ASU on Coursera, taken in Spring A 2021:
- CSE 579 - Knowledge Representation and Reasoning, created by Dr. Joohyung Lee


## Introduction:

<p>Welcome to my carefully-curated base of AI and machine learning knowledge!</p>
<p>Here I plan to keep all kinds of information about machine learning methods and how they compare. There are so many out there 
   that it is easy to get lost. After studying the topic for over three years I am still overwhelmed by the immensity of the field.
   Hopefully this project will serve as a helpful reference for me as I learn and grow in experience working with machine learning.</p>
<p>The framework is an RDF graph, a semantic web technology consisting of many interconnected "things" called <i>resources</i>.
   These resources can be <b>concepts</b> such as <i>linear regression</i> or <b>properties</b> such as <i>has advantage</i> or 
   <b>literals</b> such as <i>"very simple."</i></p>
<p>These connections are represented as <b>triples</b> consisting of a <b>subject</b>, a <b>predicate</b>, and an <b>object</b>.</p>

<img src="https://github.com/jmsbutcher/machine-learning-knowledge-base/blob/master/website/static/triples_diagram1.png" class="img-fluid" alt="triples diagram">

<p>The above diagram depicts two triples: (classification, is a, application) and (decision tree, can do, application). Note that 
    the resource called "classification" appears twice. In an RDF graph, these two instances of "classification" refer to the same thing. 
    Thus, a list of triples together builds a sort of "web" of knowledge. This is the backbone of the knowledge graph structure.
    Below is a small example of what such a knowledge graph looks like:
</p>

<img src="https://github.com/jmsbutcher/machine-learning-knowledge-base/blob/master/website/static/simple_graph1.png" class="img-fluid" alt="simple graph">

<p>This framework is extremely flexible. You can use any concept or property you wish to express relationships in any domain of knowledge.
    For example, the above diagram can be extended by adding triples representing subclass relationships. One of these could be:
    (logistic regression, subclass of, supervised learning).
</p>
<p>Or, as I found very useful, triples representing the strengths and weaknesses of various machine learning methods. For example:
    (decision tree, has advantage, "creates good explanations"), and (decision tree, has disadvantage, "only easily interpretable when short").
    This comes in handy when comparing different methods to use for a given application.
</p>

<br />

## Add/Remove Triples from Knowledge Base

<p>The <a href="https://aikb-bfe2tw67tq-ue.a.run.app/knowledge-base" target="_blank">Knowledge Base</a> page lists all the triples currently in the knowledge base.</p>
<p><b>To add a triple:</b> Enter a subject, a predicate, and an object in the corresponding input fields and click enter.
Be sure to use consistent spelling when entering multiple triples containing the same thing. Some inputs are case-sensitive.</p>
<p><b>To delete a triple:</b> Simply scroll down to the triple you want to delete and click the 'X' on the right.
<p>Be sure to click "Save" if you want to save your changes to the graph file.</p>

<img src="https://github.com/jmsbutcher/machine-learning-knowledge-base/blob/master/images/knowledgebase_page1.PNG">

<br />

## Recommender Tool

<p>The <a href="https://aikb-bfe2tw67tq-ue.a.run.app/recommender" target="_blank">Recommender</a> page lets you select the application you are interested in and then generates a neat list of relevant
    machine learning methods and information about each one, including their advantages and disadvantages. 
</p>
<p>It does this by querying the knowledge base for all subjects that meet the criteria: [subject] --> can do --> [selected application],
    and then gathers all other information on that subject.
</p>

<img src="https://github.com/jmsbutcher/machine-learning-knowledge-base/blob/master/images/recommender_page1.PNG">

<br />

## Custom Queries

<p>The <a href="https://aikb-bfe2tw67tq-ue.a.run.app/query" target="_blank">Custom Query</a> page lets you examine the knowledge base in more detail.</p>
<p>Select the subject, predicate, or object you are interested in while leaving the other fields with the default '?'
    selection acting as a wildcard, and the program will fetch all the triples that meet the criteria.
</p>

<img src="https://github.com/jmsbutcher/machine-learning-knowledge-base/blob/master/images/query_page1.PNG">

<p>For example, if you wanted to see all of the different applications in the knowledge base, you would
    select '?' for the subject, "is a" for the predicate, and "application" for the object. Similarly, if 
    you wanted to see all of the things k-means clustering can do, you would select "k-means clustering" for 
    the subject, "can do" for the predicate, and '?' for the object.
</p>

<img src="https://github.com/jmsbutcher/machine-learning-knowledge-base/blob/master/images/query_page2.PNG">

<br />
<br />

<hr>

<p>&copy; <i>James Butcher 2024 - jmsbutcher1567@gmail.com</i></p>

](https://www.linkedin.com/in/james-butcher-275a2080/)
