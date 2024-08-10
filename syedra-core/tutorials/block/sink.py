from syedra.core.block import Block, InputPort


class Sink(Block):
  block_name = 'Sink'

  x = InputPort(initial=0)

  def update(self):
    print(f"- x = {self.x}")
       

if __name__ == '__main__':

  sink = Sink()
  for x in range(5):
    sink['x'].value = x
    Block.execute(sink)
