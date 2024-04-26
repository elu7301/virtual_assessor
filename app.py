from flask import Flask, request, render_template

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
    '2-1': 'Этапы подготовки к тестированию мобильных приложений',
    '2-2': 'Основные инструменты тестирования: эмуляторы, симуляторы и мобильные фермы',
    '2-3': 'Открытые и закрытые тесты в сторах. Гайды мобильных сторов',
    '2-4': 'Функциональное тестирование',
    '2-5': 'Нефункциональное тестирование',
    '2-6': 'Проблемы и сложности при тестировании мобильных приложений'
}

user_courses = {}


def get_response(message):
    return 'Тестовый ответ'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['user_message']
    parts = user_message.split('-')

    if len(user_courses) >= 2:
        response = get_response(user_message)
        print(user_courses)

    elif len(parts) == 2:
        course, lecture = parts
        response = f"Выбран курс: {courses[course]}, лекция: {lectures[user_message]}. Давайте начнем обсуждение!"
        user_courses['лекция'] = lectures[user_message]

    elif len(parts) == 1:
        response = "Вы выбрали курс: " + courses[user_message] + ". Теперь выберите лекцию:"
        user_courses['курс'] = courses[user_message]

    return response


if __name__ == '__main__':
    app.run(debug=True)
