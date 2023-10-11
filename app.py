from flask import Flask, request, jsonify
import requests

from model import db, Question

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@db:5432/quiz_questions"
db.init_app(app)


def create_questions_table():
    with app.app_context():
        db.create_all()


def get_unique_question():
    create_questions_table()
    while True:
        response = requests.get('https://jservice.io/api/random?count=1')
        question_data = response.json()[0]
        question_text = question_data['question']
        answer_text = question_data['answer']

        question = Question.query.filter_by(question_text=question_text).first()
        if not question:
            question = Question(question_text=question_text, answer_text=answer_text)
            db.session.add(question)
            db.session.commit()
        return {
            'id': question.id,
            'question_text': question.question_text,
            'answer_text': question.answer_text,
            'created_at': question.created_at
        }


@app.route('/questions', methods=['POST'])
def get_questions():
    data = request.get_json()
    questions_num = data.get('questions_num')

    questions = []
    for _ in range(questions_num):
        question = get_unique_question()
        if question:
            questions.append(question)

    return jsonify(questions)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
