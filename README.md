# Greenwashing Detector

Dieses Projekt hat das Ziel, Nachhaltigkeitsversprechen von Unternehmen aus der Automobilbranche systematisch zu analysieren. Dabei werden zwei unterschiedliche Ansätze verfolgt:

1. Vergleich der Nachhaltigkeitsversprechen mit externen Presseartikeln, um Übereinstimmungen oder Widersprüche zu identifizieren.

2. Klassifizierung der Nachhaltigkeitsversprechen, um deren Qualität und Verbindlichkeit zu bewerten.

Die gewonnenen Erkenntnisse werden in einem interaktiven Dashboard visualisiert, das es Anwender:innen ermöglicht, die Daten übersichtlich einzusehen und interaktiv zu analysieren.

Für die Extraktion der Nachhaltigkeitsversprechen wird ein Large Language Model (LLM) eingesetzt. Der semantische Vergleich erfolgt mithilfe eines BERT-Modells. Die Visualisierung des Dashboards wurde mit Streamlit umgesetzt.

# Voraussetzungen und Installation
Um das Projekt lokal auszuführen, empfiehlt es sich, eine virtuelle Umgebung zu erstellen: python -m venv venv
Aktiviere (source venv/bin/activate on WSL/Linux) die virtuelle Umgebung. Unter Windows mit der PowerShell:
.\venv\Scripts\Activate.ps1
oder mit dem Command Prompt:
.\venv\Scripts\activate.bat
Installiere alle Requirements (pip install -r requirements.txt).

# Nutzung des Dashbaords
Das Dashboard kann durch folgenden Befehl gestartet werden: streamlit run greenwashing_dashboard.py
Dadurch wird eine lokale Webanwendung geöffnet, in der die Analyseergebnisse interaktiv erkundet werden können.

# Methodischer Hintergrund
Bei der Entwicklung des Greenwashing-Detektors wurde der CRISP-DM-Prozess (Cross Industry Standard Process for Data Mining) angewendet. Dieser strukturierte Ansatz gewährleistet eine systematische und nachvollziehbare Umsetzung der Datenanalyse von der Problemdefinition bis zur Präsentation der Ergebnisse.