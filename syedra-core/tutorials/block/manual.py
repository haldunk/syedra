import random
from syedra.core.block import *


class Manual(Block):

  value = OutputPort(initial=0.0)
  

class Printer(Block):

  value = InputPort(initial=0.0)

  def update(self):
    print(self.value)


if __name__ == '__main__':

  manual = Manual()
  printer = Printer()

  manual['value'] >> printer['value']

  try:
    while True:
      manual.value = random.randint(0, 10)
      Block.execute(manual)
      sleep(1)
  except KeyboardInterrupt:
    pass
    
