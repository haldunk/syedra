from time import time, sleep
import numpy as np
from syedra.core.block import Block, InputPort, OutputPort
from syedra.control.pid import PID



class Sensor(Block):
  block_name = 'Sensor'

  reading = OutputPort(initial=0.0)

  def __init__(self, frequency:float=5.0):
    super().__init__()
    self.__f = frequency
  
  def update(self):
    self.reading = np.sin(2*np.pi*self.__f*time())


class Controller(PID):

  def __init__(self,
               set_point:float=0.0,
               p_gain:float=0.0,
               d_gain:float=0.0,
               i_gain:float=0.0):
    super().__init__(
      name='Controller',
      p_gain=p_gain, d_gain=d_gain, i_gain=i_gain)
    self.__set_point = set_point
  
  def _get_error(self):
    return self.__set_point - self.reading


class Printer(Block):
  block_name = 'Printer'

  error = InputPort()
  command = InputPort()

  def update(self):
    if self.error is not None and self.command is not None:
      print(f"err: {self.error:>5.2f} | cmd: {self.command:>5.2f}")


if __name__ == '__main__':

  sensor = Sensor(frequency=5.0)
  controller = Controller(
    set_point=0.0, p_gain=1.0, d_gain=1.0)
  printer = Printer()

  sensor['reading'] >> controller['reading']
  controller['error'] >> printer['error']
  controller['command'] >> printer['command']

  for _ in range(10):
    Block.execute(sensor)
    sleep(0.1)
