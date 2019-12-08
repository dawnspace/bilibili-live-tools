from OnlineHeart import OnlineHeart
from Silver import Silver
from LotteryResult import LotteryResult
from Tasks import Tasks
from connect import connect
from rafflehandler import Rafflehandler
import asyncio
from login import login
from printer import Printer
from statistics import Statistics
from bilibili import bilibili
import threading
import biliconsole
from pkLottery import PKLottery
from guard import Guard

loop = asyncio.get_event_loop()
printer = Printer()
bilibili()
Statistics()
rafflehandler = Rafflehandler()
biliconsole.Biliconsole()

task = OnlineHeart()
task0 = Guard()
task1 = Silver()
task2 = Tasks()
task3 = LotteryResult()
task4 = connect()
task5 = PKLottery()

tasks1 = [
    login().login_new()
]
loop.run_until_complete(asyncio.wait(tasks1))

console_thread = threading.Thread(target=biliconsole.controler)
console_thread.start()

tasks = [
    task.run(),
    task0.run(),
    task1.run(),
    task2.run(),
    biliconsole.Biliconsole().run(),
    task4.create(),
    task3.query(),
    rafflehandler.run(),
    task5.run()
]

loop.run_until_complete(asyncio.wait(tasks, return_when=asyncio.FIRST_EXCEPTION))
loop.close()

console_thread.join()
