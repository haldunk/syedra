import asyncio
import random
from syedra.core.block import *


class Manual(AsyncBlock):
  block_name = 'Manual'

  value = OutputPort(initial=0.0)


class Printer(Block):
  block_name = 'Display'

  value = InputPort(initial=0.0)

  async def update(self):
    print(self.value)


async def main(manual):
  try:
    while True:
      manual.value = random.randint(0, 10)
      await AsyncBlock.execute(manual)
      await asyncio.sleep(1)
  except asyncio.CancelledError:
    print('main is cancelled')
  finally:
    print('main is stopped')

    
if __name__ == '__main__':

  manual = Manual()
  printer = Printer()

  manual['value'] >> printer['value']

  asyncio.run(main(manual))
