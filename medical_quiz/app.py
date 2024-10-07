from flask import Flask, render_template, request, jsonify, redirect, url_for
from gpiozero import LED, Button
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

# Initialize Buttons using BCM pin numbering
buttons = {
    'A': Button(13, pull_up=True, bounce_time=0.1),
    'B': Button(19, pull_up=True, bounce_time=0.1),
    'C': Button(26, pull_up=True, bounce_time=0.1),
    'D': Button(21, pull_up=True, bounce_time=0.1)
}

def get_db_connection():
    conn = sqlite3.connect('quiz.db', check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

# Global variable to keep track of selected mode
selected_mode = None
current_question_index = 0
question_list = []

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
    global selected_mode, current_question_index
    if mode in ['information', 'quiz']:
        selected_mode = mode
        current_question_index = 0  # Reset question index when mode changes
        if mode == 'quiz':
            load_questions()
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
    else:
        return jsonify({'error': 'No mode selected or invalid mode for this operation.'}), 400

# New route to get the current question
@app.route('/get_current_question')
def get_current_question():
    global current_question_index, question_list
    if not question_list:
        return jsonify({'message': 'No questions available.'})

    question = question_list[current_question_index]
    return jsonify({'question': dict(question)})

# Load all questions at startup or when entering quiz mode
def load_questions():
    global question_list
    conn = get_db_connection()
    question_list = conn.execute('SELECT * FROM questions').fetchall()
    conn.close()
    if not question_list:
        print("No questions found in the database.")
    else:
        print(f"Loaded {len(question_list)} questions.")

# Function to handle button presses
def handle_button_press(selected_option):
    global current_question_index, question_list
    print(f"Button {selected_option} pressed.")
    if not question_list:
        print("No questions available.")
        return

    question = question_list[current_question_index]
    question_id = question['id']
    print(f"Current question ID: {question_id}")
    # Submit the answer
    submit_answer_via_button(question_id, selected_option)
    # Advance to the next question
    current_question_index = (current_question_index + 1) % len(question_list)
    print(f"Advancing to question index: {current_question_index}")
    # Notify the client to load the next question
    # Since we cannot directly push to the client, the client will refresh periodically

# Function to submit answer without Flask request context
def submit_answer_via_button(question_id, selected_option):
    # Fetch the question from the database
    conn = get_db_connection()
    question = conn.execute('SELECT * FROM questions WHERE id = ?', (question_id,)).fetchone()

    if not question:
        conn.close()
        print('Invalid question ID.')
        return

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
        threading.Thread(target=activate_led, args=(body_part,), daemon=True).start()
        print(f"Correct! The {body_part} LED is blinking for 3 seconds.")
    else:
        threading.Thread(target=blink_all_leds, daemon=True).start()
        print('Incorrect. All LEDs are blinking for 3 seconds.')

# LED control functions
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

# Submit answer from web interface (if still used)
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
        threading.Thread(target=activate_led, args=(body_part,), daemon=True).start()
        message = f"Correct! The {body_part} LED is blinking for 3 seconds."
    else:
        threading.Thread(target=blink_all_leds, daemon=True).start()
        message = 'Incorrect. All LEDs are blinking for 3 seconds.'

    # Advance to the next question
    global current_question_index, question_list
    current_question_index = (current_question_index + 1) % len(question_list)
    print(f"Advancing to question index: {current_question_index}")

    return jsonify({'message': message})

@app.route('/cleanup', methods=['GET'])
def cleanup():
    # gpiozero handles cleanup automatically
    return 'GPIO cleanup done.'

# Set up event handlers for buttons
def create_button_handlers():
    for option, button in buttons.items():
        button.when_pressed = lambda opt=option: handle_button_press(opt)

create_button_handlers()

if __name__ == '__main__':
    load_questions()  # Load questions at startup
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass  # Clean exit
