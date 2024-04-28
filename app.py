from flask import Flask, request, render_template

from predict_model import *
from feed_back_model import *

app = Flask(__name__)

courses = {
    'курс 1': 'Основы тестирования',
    'курс 2': 'Процесс тестирования мобильных приложений',
    '1': 'Основы тестирования',
    '2': 'Процесс тестирования мобильных приложений'
}

lectures = {
    '1-1': 'Введение в тестирование',
    '1-2': 'Чек-листы',
    '1-3': 'Тест-кейсы',
    '1-4': 'Техники тест-дизайна',
    '1-5': 'Функциональная и нефункциональное тестирование',
    '1-6': 'Этапы подготовки к тестированию мобильных приложений',
    '1-7': 'Тест по всему курсу',
    '2-1': 'Этапы подготовки к тестированию мобильных приложений',
    '2-2': 'Основные инструменты тестирования: эмуляторы, симуляторы и мобильные фермы',
    '2-3': 'Открытые и закрытые тесты в сторах. Гайды мобильных сторов',
    '2-4': 'Функциональное тестирование',
    '2-5': 'Нефункциональное тестирование',
    '2-6': 'Проблемы и сложности при тестировании мобильных приложений',
    '2-7': 'Тест по всему курсу'
}

user_courses = {
    'counter': 0,
    'questions': [],
    'correct_ans': [],
    'incorrect_ans': []
}


def select_and_drop_random_row(df):
    if len(df) <= 5:
        random_row = df.head(1)
    else:
        random_row = df.sample()
    index_to_drop = random_row.index[0]
    df = df.drop(index_to_drop)

    return random_row, df


def create_df(lecture):
    data = pd.read_csv('train_full.csv')
    if lecture == '1-7':
        data = data[data['Lesson'].str.startswith('1')]
    elif lecture == '2-7':
        data = data[data['Lesson'].str.startswith('2')]
    else:
        data = data[data['Lesson'] == lecture]

    data = data.Question.unique()
    df = pd.DataFrame(data={'Question': data})

    return df


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    parts = user_message.split('-')
    response = ''
    feedback = ''

    if 5 >= user_courses['counter'] >= 2:
        row, user_courses['df'] = select_and_drop_random_row(user_courses['df'])
        question = row['Question'].iloc[0]
        response = get_response(user_message, user_courses['questions'][-1])

        if response == 'Вы ошиблись! ':
            response += 'Попробуйте ответить на следующий вопрос. \n \n'
            user_courses['incorrect_ans'].append(user_message)
        else:
            user_courses['correct_ans'].append(user_message)
            response += 'Перейдем к следующему вопросу. \n \n'

        user_courses['questions'].append(question)
        response += question

    elif user_courses['counter'] == 6:
        response = get_response(user_message, user_courses['questions'][-1]) + '\n Спасибо, что воспользовались нашим ботом, для проверки знаний.'

        if len(user_courses['incorrect_ans']) > 0:
            feedback = get_feedback(user_courses['incorrect_ans'][-1])
        else:
            feedback = get_feedback(user_courses['correct_ans'][-1])

    elif user_courses['counter'] == 1:
        course, lecture = parts
        if user_message not in ('1-7', '2-7'):
            response = f"Выбран курс: {courses[course]}, лекция: {lectures[user_message]}. \n \n Давайте начнем обсуждение!"
        else:
            response = f"Выбран курс: {courses[course]}. \n \n Давайте начнем обсуждение!"

        user_courses['df'] = create_df(user_message)
        row, user_courses['df'] = select_and_drop_random_row(user_courses['df'])
        question = row['Question'].iloc[0]
        response += '\n \nПервый вопрос: ' + question

        user_courses['questions'].append(question)
        user_courses['курс'] = course
        user_courses['лекция'] = lectures[user_message]
        user_courses['key'] = user_message

    elif user_courses['counter'] == 0:
        response = 'Вы выбрали курс: ' + courses[user_message] + '. \n \nТеперь выберите лекцию:'
        user_courses['курс'] = courses[user_message]

    else:
        response = '\n \nСпасибо, что воспользовались нашим ботом, для проверки знаний.'

    user_courses['counter'] += 1

    if feedback != '':
        return response + '\t' + feedback + '\t' + user_courses['key']

    return response


if __name__ == '__main__':
    app.run(debug=True)
