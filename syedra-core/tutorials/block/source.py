import random
from syedra.core.block import Block, OutputPort



class Source(Block):
  block_name = 'Source'

  y = OutputPort(initial=0)

  def update(self):
    self.y = random.randint(0, 10)


if __name__ == '__main__':

  source = Source()
  for _ in range(5):
    Block.execute(source)
    print(f"- y = {source.y}")
