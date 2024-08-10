import random
from time import sleep
from syedra.core.block import *



class Periodic(Block):
  block_name = 'Periodic'

  trigger = InputPort()
  y = OutputPort()

  def update(self):
    self.y = random.randint(0, 10)
    print(f"y = {self.y}")
    sleep(1)


if __name__ == '__main__':

  periodic = Periodic()

  periodic['y'] >> periodic['trigger']

  try:
    Block.execute(periodic)
  except KeyboardInterrupt:
    pass
