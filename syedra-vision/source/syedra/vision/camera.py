from __future__ import annotations
import cv2
from syedra.core.block import Block, OutputPort


__all__ = [
  'Camera',
]


class Camera(Block):

  class HardwareError(Exception):
    def __init__(self, camera:Camera):
      super().__init__(
        f"Camera Hardware Error: {camera}")

      
  frame = OutputPort(initial=None)
  valid = OutputPort(initial=False)

  def __init__(self, index:int, name:str='Camera'):
    super().__init__(name=name)
    self.__index = index
    self.__cap = cv2.VideoCapture(self.__index)
    if not self.__cap.isOpened():
      raise Camera.HardwareError(camera=self)

  def __delete__(self):
    super().__delete__()
    if self.__cap.isOpened():
      self.__cap.release()

  def update(self):
    self.valid, self.frame = self.__cap.read()
    
