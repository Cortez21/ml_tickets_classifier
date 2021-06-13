import json
import sys

from aiohttp import web

from data_corrector import DataCorrector
from model import Model


routes = web.RouteTableDef()
model = Model()


@routes.post('/predict')
async def handle(request):
    response_dict = dict()
    try:
        body = await request.text()
        body_dict = json.loads(body)
        text = body_dict['message']
        response_dict['status'] = 'SUCCES'
        topic_name = model.predict(DataCorrector(text).parse())
        response_dict['topic_name'] = topic_name
    except Exception:
        print(sys.exc_info())
        response_dict['status'] = 'ERROR'
    response_body = json.dumps(response_dict)
    return web.Response(body=response_body)


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app, port=8000)
