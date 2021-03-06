import json
import sys

from aiohttp import web

from data_corrector import DataCorrector
from model import Model
from langdetect import detect, LangDetectException

routes = web.RouteTableDef()
models = {
    'ru': Model('ru'),
    'en': Model('en')
}


@routes.post('/predict')
async def predict(request):
    response_dict = dict()
    try:
        body = await request.text()
        body_dict = json.loads(body)
        text = body_dict['message']
        response_dict['status'] = 'SUCCES'
        lang = detect_language(text)
        topic_name = models.get(lang).predict(DataCorrector(text).parse())
        response_dict['language'] = lang
        response_dict['topic_name'] = topic_name
    except Exception:
        print(sys.exc_info())
        response_dict['status'] = 'ERROR'
    response_body = json.dumps(response_dict)
    return web.Response(
        body=response_body,
        content_type='application/json'
    )


def detect_language(text):
    try:
        if detect(text) in ['sl', 'uk', 'et', 'bg', 'ru', 'ca', 'pt', 'cs', 'it', 'es', 'so', 'cy', 'ro', 'mk']:
            return 'ru'
        else:
            return 'en'
    except LangDetectException:
        return 'en'


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8000)
