import asyncio

class test_class():
    def __init__(self):
        self.num = 1
    async def math(self):
        return self.num + 1

async def math():
    return 1 + 1

async def myPrint(name):
    test = test_class()
    out = await test.math()
    return out

if __name__ == "__main__":
    test = test_class()
    out = asyncio.run(test.math())
    print(out)