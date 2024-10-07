import sqlite3

def check_database():
    conn = sqlite3.connect('quiz.db')
    cursor = conn.cursor()
    
    # Check the number of questions
    cursor.execute('SELECT COUNT(*) FROM questions')
    question_count = cursor.fetchone()[0]
    print(f'Total questions in the database: {question_count}')
    
    # Optionally, check the number of responses
    cursor.execute('SELECT COUNT(*) FROM responses')
    response_count = cursor.fetchone()[0]
    print(f'Total responses recorded: {response_count}')
    
    conn.close()

if __name__ == '__main__':
    check_database()
