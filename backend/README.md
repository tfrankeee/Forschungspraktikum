# QTI Generator Webserver
Ziel ist es mittels der Python Libray Jinja automatisiert qti3.0-konforme XML-Dateien zu erzeugen.  
Dies soll mittels einer Webanwendung bedienbar sein, basierend auf HTMX gehosted in Flask.

## Installation

1. Python3 installieren  
    Windows: `winget install -e --id Python.Python.3.9`  
    Linux: `sudo apt install python3` (Debian based) | `sudo dnf install python3` (Fedora)  
2. Mit Python venv virtuelles Environment erstellen  
    `python3 -m venv env`  
3. Virtuelles Environment aktivieren  
    Windows: `.env\Scripts\activate`  
    Linux: `source env/bin/activate`  
4. Mittels Python Package Manager (pip, pip3 oder pipx) flask und gunicorn installieren, falls nicht vorhanden.  
    pip3 install flask gunicorn html jinja2

## Dateistruktur

root  
├── htmx/  
├── README.md  
├── run.py  
└── server/  
    ├── \__init__.py  
    ├── jinja/  
    │   ├── multiple-choice-template.xml.jinja  
    │   └── text-entry-template.xml.jinja  
    ├── templates  
    │   └── index.html  
    └── views.py  

## Funktionsweise
run.py -> ist root des Systems und wird zum start des Servers ausgeführt. run.py importiert zusätzlich die im Server definierten Module (Python Skripte).  

server/init.py -> initialisiert die Module beim start des Systems  

server/views.py -> regelt die Funktionsweise des Flask-Webservers, definierte Endpunkte und Aktionen beim Aufruf der Endpunkte  

server/jinja -> jinja Vorlagen für qti-Datei Erzeugung  

server/templates/index.html -> templates enthalt die reinen HTML/HTMX Dateien. Die index.html ist die Webroot bzw. Homepage. Via Skript in der index.html wird HTMX geladen
und ausgeführt.  

## Ausführen

1. jinja-Template Dateien (*.xml.jinja) im Ordner server/jinja/  
2. (Optional) Variablen in dem Python-Skript (server/views.py) ändern.  
3. Mittels Python ausführen (python3 run.py)  
4. Website unter http://127.0.0.1:5000 öffnen.  

## TODO

- Model-Context-Protocol (MCP) integrieren.  
    - [Ressourcen](https://modelcontextprotocol.io/docs/concepts/resources) definieren (Holles Vorlesungsskript als PDF -> file:///home/user/documents/report.pdf)  
    - [Tools](https://modelcontextprotocol.io/docs/concepts/tools) definieren (text-entry erzeugen oder mutliple-choice erzeugen)  

## Ausblick

- Zwischenspeicherung bereits erstellter Aufgaben in Datenbank (sqlite DB)
- Formular auf Website für manuelles erstellen von Aufgaben


## Ressourcen

[Jinja2-Doku](https://jinja.palletsprojects.com/en/stable/)  
[Flask Webserver](https://flask.palletsprojects.com/en/stable/)  
[HTMX für Websiteinhalt](https://htmx.org/)  
[AI Integration](https://modelcontextprotocol.io/introduction)  
[AI Hosting](https://ollama.com/)  
[Deployment Poetry](https://python-poetry.org/)  

## Alternativprodukte

- [Obsidian Quiz-generator](https://github.com/ECuiDev/obsidian-quiz-generator)  
- [Google NotebookLM](https://notebooklm.google/)  
- [Open NotebookLM](https://huggingface.co/spaces/gabrielchua/open-notebooklm)  
- [dende.ai](https://dende.ai/)  
- [Saner.AI](http://Saner.ai)
