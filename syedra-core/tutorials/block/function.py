import random
from syedra.core.block import *


class Generator(Block):
  block_name = 'Generator'

  y = OutputPort()

  def update(self):
    self.y = random.randint(0, 10)


class Function(Block):
  block_name = 'Function'

  x = InputPort()
  y = OutputPort()

  def update(self):
    self.y = self.x ** 2


class Printer(Block):
  block_name = 'Printer'

  x = InputPort()
  y = InputPort()

  def update(self):
    print(f"x = {self.x} | y = {self.y}")


if __name__ == '__main__':

  generator = Generator()
  function = Function()
  printer = Printer()

  generator['y'] >> function['x']
  generator['y'] >> printer['x']
  function['y'] >> printer['y']

  Block.execute(generator)
