import json

from aiohttp import web

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
        response_dict['message'] = 'SUCCES'
        topic_name = model.predict(text)
        response_dict['topic_name'] = topic_name
    except Exception:
        response_dict['message'] = 'ERROR'
    response_body = json.dumps(response_dict)
    return web.Response(body=response_body)


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)
