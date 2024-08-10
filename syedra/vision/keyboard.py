from __future__ import annotations
from typing import List
import cv2
from system.block import Block


__all__ = [
  'Keyboard',
]


class Keyboard(Block):

  class QuitCommand(Exception):
    def __init__(self):
      super().__init__("Keyboard signal to quit")

  def __init__(self, delay:int=0, input_ports:List[str]=['show']):
    '''
    delay: hold duration in msec. Waits indefinitely if 0
    input_ports: List of names for input port to be created
    '''
    super().__init__(name='Keyboard')
    self.__delay = delay
    for port_name in input_ports:
      self._add_port(port_name, InputPort)

  def update(self):
    try:
      keypress = cv2.waitKey(self.__delay) & 0xFF
    except KeyboardInterrupt:
      keypress = ord('q')
    if keypress == ord('q'):
      cv2.destroyAllWindows()
      raise Keyboard.QuitCommand()
