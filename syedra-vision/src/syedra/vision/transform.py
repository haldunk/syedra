from __future__ import annotations
from enum import Enum
import cv2
from syedra.core.block import Block, InputPort, OutputPort


__all__ = [
  'Crop',
  'Convert',
]


class Crop(Block):

  original = InputPort()
  cropped = OutputPort(initial=None)

  def __init__(self, 
               left:int=None, top:int=None,
               right:int=None, bottom:int=None,
               name:str='Crop'):
    super().__init__(name=name)
    self.set_crop_range(left, top, right, bottom)

  def set_crop_range(self, left:int=None, top:int=None,
                     right:int=None, bottom:int=None):
    self.__left = left
    self.__top = top
    self.__right = right
    self.__bottom = bottom

  def update(self):
    if self.original is not None:
      height, width, _ = self.original.shape
      x1 = self.__left or 0
      y1 = self.__top or 0
      x2 = self.__right or width
      y2 = self.__bottom or height
      self.cropped = self.original[y1:y2, x1:x2]
    else:
      self.cropped = None


class Convert(Block):

  original = InputPort()
  converted = OutputPort(initial=None)

  class Mapping(Enum):
    BGR2HSV = cv2.COLOR_BGR2HSV
  
  def __init__(self,
               mapping:Mapping=Mapping.BGR2HSV,
               name:str='Converter'):
    super().__init__(name=name)
    self.__mapping = mapping

  def update(self):
    if self.original is not None:
      self.converted = cv2.cvtColor(
        self.original, self.__mapping.value)
    else:
      self.converted = None
