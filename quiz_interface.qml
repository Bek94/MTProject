import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "Quiz zu medizinischen Implantaten"

    Column {
        spacing: 10
        padding: 20

        Text {
            text: "Welches Implantat hilft, bei einem Defizit die Sinussignale des Herzens zu überbrücken?"
            font.pointSize: 18
        }

        RadioButton {
            id: optionA
            text: "A. Herzschrittmacher"
        }
        RadioButton {
            id: optionB
            text: "B. Knieprothese"
        }
        RadioButton {
            id: optionC
            text: "C. Cochlea-Implantat"
        }
        RadioButton {
            id: optionD
            text: "D. Handprothese"
        }

        Button {
            text: "Absenden"
            onClicked: {
                if (optionA.checked) {
                    console.log("Richtig, die richtige Antwort ist Herzschrittmacher.")
                } else if (optionB.checked || optionC.checked || optionD.checked) {
                    console.log("Falsch, die richtige Antwort ist Herzschrittmacher.")
                }
            }
        }
    }
}
