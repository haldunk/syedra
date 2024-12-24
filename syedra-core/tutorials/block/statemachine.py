import time
from random import randint
from syedra.core.block import Block, InputPort, OutputPort
from syedra.core.fsm import Machine, State, Event



class Indicator(Machine):

  indicate = State(
    ingress=lambda m: print('ingress'),
    during=lambda m: print(f'during: {m.block.gauge}'),
    egress=lambda m: print('egress'),
  )
  exceeds = Event(check=lambda m: m.block.gauge > 5)

  transitions = [
    ('indicate', 'exceeds', 'indicate'),
  ]
  initial = 'indicate'

  def __init__(self, block:Block):
    super().__init__(name=block.name)
    self.block = block

  
class BlockMachine(Block):
  block_name = 'BlockMachine'

  gauge = InputPort(initial=0)

  def __init__(self):
    super().__init__()
    self.machine = Indicator(block=self)
  
  def update(self):
    self.machine.update()

    
class RandomSource(Block):
  block_name = 'Random Source'
  
  value = OutputPort(initial=0)

  def update(self):
    self.value = randint(0, 10)
    print(f"source: {self.value}")
    

if __name__ == '__main__':

  random_source = RandomSource()
  block_machine = BlockMachine()

  random_source['value'] >> block_machine['gauge']
  
  try:
    while True:
      Block.execute(random_source)
      time.sleep(1.0)
  except KeyboardInterrupt:
    pass
