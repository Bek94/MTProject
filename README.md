# MTProject
# Implantat-Quiz- und Informationssystem

Dieses Projekt bietet eine interaktive Plattform für Quizfragen und Informationsanzeigen über medizinische Implantate. Es kombiniert einen Quizmodus mit einem Mehrinformationsmodus, der es dem Benutzer ermöglicht, durch Sensorberührungen detaillierte Informationen abzurufen.

## Voraussetzungen

- Raspberry Pi 4/5
- LEDs und Sensoren für Herzschrittmacher, Knieprothese, Ellenbogenprothese und Schulterprothese
- Python 3
- Qt Design Studio

## Installation

1. **Klonen des Repositories**:
    ```
    git clone <your-github-repo-link>
    cd implant-quiz-info-app
    ```

2. **Installieren der Abhängigkeiten**:
    ```
    pip install -r requirements.txt
    ```

3. **Verbinden der Sensoren und LEDs**:
    - Herzschrittmacher: GPIO 5 (Sensor), GPIO 17 (LED)
    - Knieprothese: GPIO 6 (Sensor), GPIO 27 (LED)
    - Ellenbogenprothese: GPIO 13 (Sensor), GPIO 22 (LED)
    - Schulterprothese: GPIO 19 (Sensor), GPIO 23 (LED)

4. **Starten der Anwendung**:
    - Führe das Hauptskript aus:
      ```
      sudo python3 main.py <mode> <result> <implant>
      ```

    - Öffne das Qt-Projekt und starte die `implant_interface.qml` Datei.

## Verwendung

- Wähle im UI zwischen dem Quiz- und Informationsmodus.
- Im Quiz-Modus gibt es visuelles Feedback (LEDs) bei richtigen/falschen Antworten.
- Im Mehrinformationsmodus werden durch Sensorberührungen detaillierte Informationen angezeigt.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
