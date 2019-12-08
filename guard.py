import asyncio
import aiohttp
import struct
import json

from bilibili import bilibili
from printer import Printer

class Guard:

    SERVER = 'ws://websftp.cecs.pdx.edu:8999'    # Portland State University server

    def __init__(self):
        self.guard_history = []
        self.queue = asyncio.Queue()
        self.session = aiohttp.ClientSession()

    async def run(self):
        try:
            consumers = [ self.consume() for _ in range(100) ]
            consumers.append(self.produce())
        except Exception as exc:
            raise exc

        done, pending = await asyncio.wait(consumers, return_when=asyncio.FIRST_EXCEPTION)
        for finished in done:
            if finished.exception():
                raise finished.exception()

    async def produce(self):
        cls = self.__class__
        while True:
            try:
                async with self.session.ws_connect(cls.SERVER) as ws:
                    Printer().printer(f'成功连接服务器@{cls.SERVER}', 'Info', 'green')
                    while not ws.closed:
                        data = await ws.receive_bytes()
                        
                        position = 0
                        while position < len(data):
                            total_len, header_len, _, cmd, _ = struct.unpack('!IHHII', data[:16])
                            start = position + header_len
                            end = position + total_len
                            await self.queue.put(data[start:end])
                            position += total_len

                        if ws.exception():
                            raise ws.exception()
            except (OSError, ConnectionRefusedError) as exc:
                Printer().printer(
                        f'舰长服务器@{cls.SERVER}连接失败, 30s后重试...', 'Error', 'red')
                await asyncio.sleep(30)
            except Exception as exc:
                Printer().printer(
                        f'舰长服务器@{cls.SERVER}发生错误: {exc}, 30s后重试', 'Error', 'red')
                await asyncio.sleep(30)


    async def consume(self):
        while True:
            data = await self.queue.get()
            await self.on_message(data)

    async def on_message(self, data):
        json_str = data.decode('utf-8')
        payload = json.loads(json_str)
        
        if (payload['type'] == 'guard'):
            OriginRoomId = payload['roomid']
            GuardId = payload['id']
            r = await bilibili().get_gift_of_captain(OriginRoomId, GuardId)
        
            resp = await r.json(content_type=None)
            if resp['code'] == 0:
                data = resp['data']
                award = f'获取到房间 {OriginRoomId} 编号 {GuardId} 的上船亲密度: '
                award += data.get('award_text', '')
                Printer().printer(f'{award}', "Lottery", "cyan")
            elif resp['code'] == 400 and resp['msg'] == "你已经领取过啦":
                Printer().printer(
                        f"房间 {OriginRoomId} 编号 {GuardId} 的上船亲密度已领过",
                        "Info", "green")
            elif resp['code'] == -403 and resp['msg'] == "访问被拒绝":
                Printer().printer(f"获取房间 {OriginRoomId} 编号 {GuardId} 的上船亲密度: {resp['message']}",
                        "Lottery", "cyan")
                print(resp)
            else:
                Printer().printer(
                        f"房间 {OriginRoomId} 编号 {GuardId}  的上船亲密度领取出错: {resp}",
                        "Error", "red")
                await asyncio.sleep(0.2)
