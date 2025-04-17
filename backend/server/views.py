from server import server
from flask import render_template, request, jsonify
from jinja2 import Template
import html

# Webroot
@server.route('/')
def index():
    return render_template('index.html')

# Endpoint for text-entry qti-file generation
@server.route('/text-entry')
def te_data():
    # Open Jinja2 template for text-entry
    with open("server/jinja/text-entry-template.xml.jinja") as tef:
        te_tmpl = Template(tef.read())

    # Define the data for the text-entry QTI file
    te_qti_data = {
            "identifier" : "PVLH1",
            "title" : "PVL Aufgabe 1",
            "response_value" : "zusammenhängender",
            "score" : "zusammenhängender",
            "score_value" : 1,
            "text_pre_gap" : "Ein Baum ist ein ",
            "text_post_gap" : " Graph, der keine Kreise enthält.",
    }

    # Render the QTI file using the template and data
    te_qti_contents = te_tmpl.render(te_qti_data)

    # Escape the QTI contents for HTML display
    escaped_qti_contents = html.escape(te_qti_contents)
    return f"<pre>{escaped_qti_contents}</pre>"

# Endpoint for single-choice qti-file generation
@server.route('/single-choice')
def sc_data():
    # Open Jinja2 template for single-choice
    with open("server/jinja/single-choice-template.xml.jinja") as scf:
        sc_tmpl = Template(scf.read())

    # Define the data for the single-choice QTI file
    sc_qti_data = {
        "identifier": "SC1",
        "title": "Hauptstadtfrage",
        "question": "Was ist die Hauptstadt von Frankreich?",
        "correct_choice": "A",
        "choices": [
            {"identifier": "A", "text": "Paris"},
            {"identifier": "B", "text": "Madrid"},
            {"identifier": "C", "text": "Berlin"},
            {"identifier": "D", "text": "Rom"},
        ]
    }

    # Render the QTI file using the template and data
    sc_qti_contents = sc_tmpl.render(sc_qti_data)
    # Escape the QTI contents for HTML display
    escaped_qti_contents = html.escape(sc_qti_contents)
    return f"<pre>{escaped_qti_contents}</pre>"

# Endpoint for multiple-choice qti-file generation
@server.route('/multiple-choice')
def mc_data():
    # Open Jinja2 template for multiple-choice
    with open("server/jinja/multiple-choice-template.xml.jinja") as mcf:
        mc_tmpl = Template(mcf.read())

    # Define the data for the multiple-choice QTI file
    mc_qti_data = {
        "identifier": "MC1",
        "title": "Programmiersprachen",
        "question": "Welche der folgenden sind Programmiersprachen?",
        "correct_choices": ["A", "C"],
        "max_choices": 4,
        "choices": [
            {"identifier": "A", "text": "Python"},
            {"identifier": "B", "text": "HTML"},
            {"identifier": "C", "text": "Java"},
            {"identifier": "D", "text": "CSS"},
        ]
    }

    # Render the QTI file using the template and data
    mc_qti_contents = mc_tmpl.render(mc_qti_data)
    # Escape the QTI contents for HTML display
    escaped_qti_contents = html.escape(mc_qti_contents)
    return f"<pre>{escaped_qti_contents}</pre>"