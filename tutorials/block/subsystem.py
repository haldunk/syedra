import random
from syedra.core.block import *



class Generator(Block):
  block_name = 'Generator'

  y = OutputPort()
  
  def update(self):
    self.y = random.randint(0, 10)


class Printer(Block):
  block_name = 'Printer'

  x = InputPort()

  def update(self):
    print(f"x = {self.x}")


class Container(Block):
  block_name = 'Container'

  y = ProxyPort()

  def __init__(self):
    super().__init__()
    self.generator = Generator(superblock=self)
    self.printer = Printer()
    self.generator['y'] >> self.printer['x']
    self.generator['y'] >> self['y']


if __name__ == '__main__':

  container = Container()

  Block.execute(container)
