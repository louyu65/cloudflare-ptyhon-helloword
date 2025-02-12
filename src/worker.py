from fastapi import FastAPI, Request
from pydantic import BaseModel
import base64
import json
import random
import string
import time
from hashlib import sha256
import requests
import hmac
from typing import Union

async def on_fetch(request, env):
    import asgi

    return await asgi.fetch(app, request, env)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello, World!"}


@app.get("/env")
async def env(req: Request):
    env = req.scope["env"]
    return {
        "message": "Here is an example of getting an environment variable: "
        + env.MESSAGE
    }
@app.get("/versions")
async def versions(req: Request):
    return {"version": "1.0.0"}


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.post("/items/")
async def create_item(item: Item):
    return item


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/knockdoor")
async def knock_door(item_id: int):
    return knockDoor()


def post_data(session: requests.Session, ssecurity: str, uri: str, data: dict) -> dict:
    data = str(data).replace("'", '"').replace('True', 'true').replace('False', 'false')
    nonce = ''.join(random.sample(string.digits + string.ascii_letters, 16))
    signed_nonce = _generate_signed_nonce(ssecurity, nonce)
    signature = _generate_signature(uri, signed_nonce, nonce, data)
    post_data = {'_nonce': nonce, 'data': data, 'signature': signature}
    ret = session.post(apiURL + uri, data=post_data)
    if ret.status_code != 200:
        raise PostDataError(ret.status_code, f'Failed to post data, {ret.text}')
    ret_data = ret.json()
    return ret_data


def _generate_signed_nonce(secret: str, nonce: str) -> str:
    sha = sha256()
    sha.update(base64.b64decode(secret))
    sha.update(base64.b64decode(nonce))
    return base64.b64encode(sha.digest()).decode()


def _generate_signature(uri: str, signedNonce: str, nonce: str, data: str) -> str:
    sign = '&'.join([uri, signedNonce, nonce, f'data={data}'])
    mac = hmac.new(base64.b64decode(signedNonce), digestmod='sha256')
    mac.update(sign.encode())
    return base64.b64encode(mac.digest()).decode()


class PostDataError(Exception):
    def __init__(self, code: int, message: str):
        self.code = code
        self.message = message
        super().__init__(f'Error code: {code}, message: {message}')


def knockDoor():
    defaultUA = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 Edg/126.0.0.0'
    userId = _userId

    deviceId = _deviceId

    ssecurity = _ssecurity
    serviceToken = _serviceToken
    scence_id = _knock_door_scence
    scence_name = '有人敲门'
    uri = '/appgateway/miot/appsceneservice/AppSceneService/RunScene'
    data = {"scene_id": scence_id, "trigger_key": "user.click"}
    session = requests.Session()
    cookie = f"PassportDeviceId={deviceId};userId={userId};serviceToken={serviceToken};"
    session.headers.update({
        'User-Agent': defaultUA,
        'x-xiaomi-protocal-flag-cli': 'PROTOCAL-HTTP2',
        'Cookie': cookie,
    })
    ret_data = post_data(session, ssecurity, uri, data)
    if ret_data['code'] != 0:
        raise Exception(f'Failed to get data, {data["message"]}')
        reqResult = ret_data['result']
        print(reqResult)
        return "fail"
    else:
        print('执行成功')
        reqResult = ret_data['result']
        print(reqResult)
        return "ok"