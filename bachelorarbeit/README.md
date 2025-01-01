##### Bachelorarbeit - Erstellung einer UI mit automatischer Satzvervollständigung für Reviewprozesse

## PROJECT OVERVIEW
Die vorliegende Arbeit hat einen Online-Service zur automatischen Satzvervollständigung für Reviewprozesse entwickelt und evaluiert.
Zwei Hauptansätze wurden implementiert: ein datenbankbasierter
Ansatz und ein Machine-Learning-Ansatz, der auf fortschrittlichen Large Language Models
(LLMs) basiert.
Die datenbankbasierte Umsetzung bietet eine schnelle Reaktion und einen minimalen
Ressourcenverbrauch, eignet sich jedoch am besten für Anwendungen, bei denen vordefinierte
Inhalte ausreichen. Der Machine-Learning-Ansatz bietet eine höhere Varianz und Leistung,
geht jedoch mit höherem Ressourcenbedarf einher, insbesondere bei leistungsstarken Modellen.

## REQUIREMENTS
    Minimum Python version: 3.9, recommended 3.10
    Ubuntu 22.04

    3B Model MiniOrca - 4GB RAM (https://gpt4all.io/models/gguf/orca-mini-3b-gguf2-q4_0.gguf)
    7B Model Mistral - 8GB RAM (https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf)
    
## INSTALLATION
Python:
1. Create python environment (python Version=3.10)
2. Activate python environment 
3. Install all needed packages: pip install -r requirements.txt

Local model:
1. Download a model from https://gpt4all.io/index.html to \app\model (Default: 3B-MiniOrca)
2. If needed, change constants in config.py

## HOW TO USE
1. Execute run.py and open http://127.0.0.1:5000/home on a browser.


## CREDITS
- Jannis Cui: Bachelor Thesis Author, Projekt Lead
- Daniel Schiffner: Betreuer, viel Hilfestellung
- Professor Hendrik Drachsler: Ermöglichte die Durchführung der Bachelorarbeit