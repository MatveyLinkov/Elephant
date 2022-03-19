from flask import Flask, request
import logging
import json


app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

session_storage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info(f'Request: {request.json}')
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {'end_session': False}
    }
    handle_dialog(request.json, response)
    logging.info(f'Response: {response}')
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        session_storage[user_id] = {
            'suggests': ['Не хочу', 'Не буду', 'Отстань!']
        }
        res['response']['text'] = 'Привет! Купи слона!'
        res['response']['buttons'] = get_suggests(user_id)
        return
    if req['request']['original_utterance'].lower() in ['куплю', 'покупаю', 'да', 'ок', 'хорошо',
                                                        'согласен', 'давай', 'купить', 'ладно']:
        res['response']['text'] = 'Слона можно найти на Яндекс.Маркете!'
        res['response']['end_session'] = True
        return
    res['response']['text'] = f"Все говорят {req['request']['original_utterance']}, а ты купи слона"
    res['response']['buttons'] = get_suggests(user_id)


def get_suggests(user_id):
    session = session_storage[user_id]
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests'][:2]
    ]
    session['suggests'] = session['suggests'][1:]
    session_storage[user_id] = session
    if len(suggests) <= 1:
        suggests.append({
            'title': 'Ладно',
            'url': 'https://market.yandex.ru/search?text=слон',
            'hide': True
        })
    return suggests


if __name__ == '__main__':
    app.run()
