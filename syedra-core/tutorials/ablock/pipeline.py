import asyncio
import random
from syedra.core.block import *


class Link(Block):

  a = InputPort(initial=0.0)
  b = OutputPort(initial=0.0)

  def __init__(self, name, initial=False):
    super().__init__(name=name)
    self.initial = initial
  
  async def update(self):
    if not self.initial:
      self.b = self.a + 1
    print(f"{self.name}: {self.b}")
    await asyncio.sleep(1)

    
async def process(links):
  try:
    while True:
      links[0].b = random.randint(0, 10)
      await AsyncBlock.execute(links[0])
      await asyncio.sleep(1)
      print('-'*20)
  except asyncio.CancelledError:
    print('main is cancelled')
  finally:
    print('main is stopped')

async def printer():
  try:
    while True:
      print("x"*20)
      await asyncio.sleep(random.randint(0, 3))
  except asyncio.CancelledError:
    pass
  finally:
    pass

async def main(links):
  try:
    tasks = [
      asyncio.create_task(process(links)),
      asyncio.create_task(printer())]
    await asyncio.sleep(10)
    asyncio.gather(*tasks, return_exceptions=True)
  except asyncio.CancelledError:
    print('main is cancelled')
  finally:
    print('main is stopped')
  
if __name__ == '__main__':

  links = list()
  for i in range(5):
    links.append(
      Link(name=f"link_{i}", initial=(i==0)))

  for i in range(4):
    links[i]['b'] >> links[i+1]['a']

  asyncio.run(main(links))
