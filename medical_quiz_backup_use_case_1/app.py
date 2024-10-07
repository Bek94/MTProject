from flask import Flask, render_template, request, jsonify, redirect, url_for
from gpiozero import LED
import time
import threading
import sqlite3

app = Flask(__name__)

# Initialize LEDs using BCM pin numbering
leds = {
    'Heart': LED(18),
    'Ear': LED(27),
    'Hip': LED(22),
    'Shoulder': LED(8),
    'Elbow': LED(9),
    'Knee': LED(11),
    'Foot': LED(23),
    'Arm': LED(6)
}

def get_db_connection():
    conn = sqlite3.connect('quiz.db')
    conn.row_factory = sqlite3.Row
    return conn
    
# Global variable to keep track of selected mode
selected_mode = None

# Global dictionary containing information about each body part
body_part_info = {
    'Heart': {
        'description': 'The heart is a muscular organ responsible for pumping blood through the blood vessels by repeated, rhythmic contractions.',
        'implants': [
            'Pacemaker',
            'Artificial Heart Valve',
            'Coronary Stent',
            'Aortic Stent Graft',
            'Blalock-Taussig Shunt',
            'Mitral Valve Prosthesis'
        ],
        'qr_code_url': 'static/qr_codes/heart_qr.png'
    },
    'Ear': {
        'description': 'The ear is the organ of hearing and balance in humans and other vertebrates.',
        'implants': [
            'Cochlear Implant',
            'Tympanic Membrane Graft'
        ],
        'qr_code_url': 'static/qr_codes/ear_qr.png'
    },
    'Hip': {
        'description': 'The hip joint is a ball and socket joint that allows for a wide range of motion in the lower extremity.',
        'implants': [
            'Hip Prosthesis',
            'Acetabular Cup'
        ],
        'qr_code_url': 'static/qr_codes/hip_qr.png'
    },
    'Shoulder': {
        'description': 'The shoulder is a complex joint that connects the upper arm to the torso, allowing for a wide range of motion.',
        'implants': [
            'Shoulder Prosthesis',
            'Shoulder Plate',
            'Rotator Cuff Patch',
            'Humeral Head Prosthesis',
            'Clavicle Plate'
        ],
        'qr_code_url': 'static/qr_codes/shoulder_qr.png'
    },
    'Elbow': {
        'description': 'The elbow is the joint connecting the forearm to the upper arm, allowing for bending and rotation.',
        'implants': [
            'Elbow Prosthesis',
            'Elbow Plate'
        ],
        'qr_code_url': 'static/qr_codes/elbow_qr.png'
    },
    'Knee': {
        'description': 'The knee is a hinge joint that connects the thigh with the leg, essential for walking and running.',
        'implants': [
            'Knee Prosthesis',
            'Knee Ligament Graft',
            'Polyethylene Insert',
            'Total Knee Arthroplasty Implant'
        ],
        'qr_code_url': 'static/qr_codes/knee_qr.png'
    },
    'Foot': {
        'description': 'The foot is a complex structure of bones and joints which provides support and mobility.',
        'implants': [
            'Ankle Prosthesis',
            'Foot Orthosis',
            'Ankle Arthrodesis Plate',
            'Foot Orthotic Implant',
            'Great Toe Implant'
        ],
        'qr_code_url': 'static/qr_codes/foot_qr.png'
    },
    'Arm': {
        'description': 'The arm extends from the shoulder to the hand and allows for manipulation and interaction with the environment.',
        'implants': [
            'Arm Prosthesis',
            'Hand Prosthesis',
            'Intramedullary Rod',
            'Spinal Cord Stimulator'
        ],
        'qr_code_url': 'static/qr_codes/arm_qr.png'
    }
}

# Route for mode selection
@app.route('/')
def mode_selection():
    return render_template('mode_selection.html')

# Route to set the selected mode and render the main page
@app.route('/set_mode/<mode>')
def set_mode(mode):
    global selected_mode
    if mode in ['information', 'quiz']:
        selected_mode = mode
        return redirect(url_for('main_page'))
    else:
        return "Invalid mode selected.", 400

# Main page displaying the skeleton and content
@app.route('/main')
def main_page():
    return render_template('main.html', mode=selected_mode)

# API endpoint to get information or quiz content for a body part
@app.route('/get_content/<body_part>')
def get_content(body_part):
    global selected_mode
    if selected_mode == 'information':
        # Fetch information about the body part
        info = body_part_info.get(body_part)
        if not info:
            return jsonify({'error': 'Information not available for this body part.'}), 404
        return jsonify({'type': 'information', 'content': render_template('information_content.html', body_part=body_part, info=info)})
    elif selected_mode == 'quiz':
        # Fetch quiz questions related to the body part
        conn = get_db_connection()
        questions = conn.execute('SELECT * FROM questions WHERE body_part = ?', (body_part,)).fetchall()
        conn.close()
        if not questions:
            return jsonify({'error': 'No quiz questions available for this body part.'}), 404
        return jsonify({'type': 'quiz', 'content': render_template('quiz_content.html', questions=questions)})
    else:
        return jsonify({'error': 'No mode selected.'}), 400    

# LED control part
def activate_led(body_part):
    led = leds.get(body_part)
    if led:
        for _ in range(6):  # Blink for 6 cycles (0.5 seconds each) for a total of 3 seconds
            led.on()
            time.sleep(0.25)
            led.off()
            time.sleep(0.25)

def blink_all_leds():
    for _ in range(6):  # 6 cycles for 3 seconds total
        for led in leds.values():
            led.on()
        time.sleep(0.25)
        for led in leds.values():
            led.off()
        time.sleep(0.25)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    question_id = data.get('question_id')
    selected_option = data.get('selected_option')

    # Fetch the question from the database
    conn = get_db_connection()
    question = conn.execute('SELECT * FROM questions WHERE id = ?', (question_id,)).fetchone()

    if not question:
        conn.close()
        return jsonify({'message': 'Invalid question ID.'}), 400

    correct_answer = question['correct_answer']
    body_part = question['body_part']

    is_correct = int(selected_option == correct_answer)

    # Store the response in the database
    conn.execute('''
        INSERT INTO responses (question_id, selected_option, is_correct)
        VALUES (?, ?, ?)
    ''', (question_id, selected_option, is_correct))
    conn.commit()
    conn.close()

    # Activate LEDs
    if is_correct:
        threading.Thread(target=activate_led, args=(body_part,)).start()
        message = f"Correct! The {body_part} LED is lit for 3 seconds."
    else:
        threading.Thread(target=blink_all_leds).start()
        message = 'Incorrect. All LEDs are blinking for 3 seconds.'

    return jsonify({'message': message})


@app.route('/cleanup', methods=['GET'])
def cleanup():
    # gpiozero handles cleanup automatically
    return 'GPIO cleanup done.'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass  # Clean exit

