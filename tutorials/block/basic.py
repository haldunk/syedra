import random
from syedra.core.block import Block, InputPort, OutputPort


class Process(Block):
  block_name = 'Process'

  def update(self):
    print("Process: update()")    


class Source(Block):
  block_name = 'Source'

  y = OutputPort(initial=0)

  def update(self):
    self.y = random.randint(0, 10)


class Sink(Block):
  block_name = 'Sink'

  x = InputPort(initial=0)

  def update(self):
    print(f"- x = {self.x}")
       
    
class Function(Block):
  block_name = 'Function'

  x = InputPort(initial=0)
  y = OutputPort(initial=0)

  def update(self):
    self.y = self.x + 1


if __name__ == '__main__':

  print("Process")
  process = Process()
  Block.execute(process)

  print("Sink")
  sink = Sink()
  for x in range(5):
    sink['x'].value = x
    Block.execute(sink)

  print("Source")
  source = Source()
  for _ in range(5):
    Block.execute(source)
    print(f"- y = {source.y}")

  print("Function")
  function = Function()
  for x in range(5):
    function['x'].value = x
    Block.execute(function)
    print(f"- x = {function.x} | y = {function.y}")
