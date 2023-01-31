from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from modules.ssh import ssh_conn

app = FastAPI()
incomes = [
    {'description': 'salary', 'amount': 5000}
]

@app.get('/incomes')
async def get_incomes():
    return jsonable_encoder(incomes)

@app.post('/ssh')
async def ssh_connection(request: Request):
    reqData = await request.json()
    return await ssh_conn(reqData["host"], reqData["username"], reqData["password"], reqData["commandsArr"])

@app.get("/")
async def get_server():
    # sys.exit()
    return "FastAPI Server Is Running..."