from statistics import Statistics
import asyncio


class LotteryResult:

    @staticmethod
    async def query():
        while 1:
            await Statistics().clean_TV()

            await asyncio.sleep(30)
