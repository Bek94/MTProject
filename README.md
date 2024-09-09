# MTProject
# Interaktiver Quiz-Test mit Raspberry Pi und Sensoren

Dieses Projekt implementiert einen interaktiven Quiz-Test, bei dem Benutzer über Sensoren eines Ersatzteilmenschen antworten können. Die Rückmeldung erfolgt sowohl über LEDs als auch auf einem Tablet, das die Frage anzeigt.

## Voraussetzungen

1. **Hardware**:
    - Raspberry Pi 4/5
    - 4 LEDs (rot, grün, gelb, weiß)
    - 4 Taster oder Sensoren zur Simulation der physischen Interaktion
    - Verbindungsdrähte und Widerstände
    - Steckbrett

2. **Software**:
    - Raspberry Pi OS (mit installiertem `gpiozero` und `RPi.GPIO`)
    - Python 3
    - Qt Design Studio

## Hardware-Aufbau

Verbinde die LEDs und Taster mit den GPIO-Pins des Raspberry Pi wie folgt:

- Rote LED an GPIO 17
- Grüne LED an GPIO 27
- Gelbe LED an GPIO 22
- Weiße LED an GPIO 23

- Herzschrittmacher-Sensor (Taster) an GPIO 5
- Knieprothese-Sensor (Taster) an GPIO 6
- Cochlea-Implantat-Sensor (Taster) an GPIO 13
- Handprothese-Sensor (Taster) an GPIO 19

## Installation

1. **Clone das Repository**:
    ```
    git clone <your-github-repo-url>
    cd quiz-app
    ```

2. **Installiere benötigte Python-Bibliotheken**:
    ```
    pip install RPi.GPIO
    ```

3. **Führe das Hauptprogramm aus**:
    ```
    sudo python3 main.py
    ```

4. **Starte die GUI (optional)**:
    Öffne das Projekt in Qt Design Studio und führe die QML-Datei aus.

## Verwendung

- Der Benutzer kann entweder durch Drücken eines Sensors auf dem Ersatzteilmenschen oder durch Auswahl auf dem Tablet antworten.
- Bei richtiger Antwort leuchtet die rote LED für 10 Sekunden.
- Bei falscher Antwort blinken alle LEDs für 3 Sekunden.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.
