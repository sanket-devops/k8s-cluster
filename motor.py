import tornado
import motor
import urllib


async def get_server_info():
    # replace this with your MongoDB connection string
    conn_str = "mongodb://mongo-admin:" + urllib.parse.quote("mongo-admin-27$-Jun-%2022%") + "@192.168.10.166:32717/?authSource=admin"
    # set a 5-second connection timeout
    client = motor.motor_tornado.MotorClient(conn_str, serverSelectionTimeoutMS=5000)
    try:
        print(await client.server_info())
    except Exception:
        print("Unable to connect to the server.")
tornado.ioloop.IOLoop.current().run_sync(get_server_info)

# mongodb://operr3:1BWOLaJOBwjDQ@192.168.10.166:32717/?authSource=admin
