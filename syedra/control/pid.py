from syedra.system.block import Block, InputPort, OutputPort
from time import time


__all__ = [
  'PID',
]


class PID(Block):

  reading = InputPort()
  command = OutputPort(initial=None)
  error = OutputPort(initial=None)
  d_error = OutputPort(initial=None)
  i_error = OutputPort(initial=None)

  def __init__(self,
               p_gain:float=0.0,
               d_gain:float=0.0,
               i_gain:float=0.0,
               name:str='PID'):
    super().__init__(name=name)
    self.set_gains(p_gain, d_gain, i_gain)
    self.reset()

  def _get_error(self) -> float:
    '''Child class will define this method to implement how
    error is computed from the instantenous reading value.'''
    raise NotImplementedError
    
  def update(self):
    self.error = self._get_error()
    time_now = time()
    if (self.error is not None and
        self.__error_prev is not None and
        self.__time_prev is not None):
      time_delta = time_now - self.__time_prev
      self.d_error = (self.error - self.__error_prev) / time_delta
      self.i_error = (self.i_error or 0.0) + self.error * time_delta
      self.command = -1 * (
        self.__p_gain * self.error +
        self.__d_gain * self.d_error +
        self.__i_gain * self.i_error)
    else:
      self.d_error = None
      self.i_error = None
      self.command = None
    self.__time_prev = time_now
    self.__error_prev = self.error

  def set_gains(self,
                p_gain:float=None,
                d_gain:float=None,
                i_gain:float=None):
    self.__p_gain =  getattr(self, '__p_gain', p_gain or 0.0)
    self.__d_gain =  getattr(self, '__d_gain', d_gain or 0.0)
    self.__i_gain =  getattr(self, '__i_gain', i_gain or 0.0)
    
  def reset(self):
    self.__error_prev = None
    self.__time_prev = None
    self.error = None
    self.d_error = None
    self.i_error = None
    self.command = None
