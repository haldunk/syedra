from typing import Tuple
import cv2
from syedra.core.block import Block, InputPort, OutputPort


__all__ = [
  'Display',
  'Sketch',
  'BlobSketch',
]


class Display(Block):

  image = InputPort(initial=None)
  ready = OutputPort(initial=False)

  def __init__(self, name:str='Display'):
    super().__init__(name=name)
  
  def update(self):
    if self.image is not None:
      cv2.imshow(self.name, self.image)
      self.ready = True
    else:
      self.ready = False


class Sketch(Block):

  image = InputPort(initial=None)
  annotated = OutputPort(initial=None)

  def put_text_center(self, text:str):
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    font_color = (0, 0, 255)
    (text_width, text_height), baseline = cv2.getTextSize(
      text, font, font_scale, font_thickness)
    text_x = (self.annotated.shape[1] - text_width) // 2
    text_y = (self.annotated.shape[0] + text_height) // 2
    cv2.putText(
      self.annotated, text, (text_x, text_y),
      font, font_scale, font_color, font_thickness)
  
  def update(self):
    self.annotated = self.image


class BlobSketch(Sketch):

  blob = InputPort(initial=None)

  def __init__(self,
               radius:int=10,
               color:Tuple[int,int,int]=(0,255,0),
               thickness:int=2,
               name:str='Blob Sketch'):
    super().__init__(name=name)
    self.__radius = radius
    self.__color = color
    self.__thickness = thickness
  
  def update(self):
    super().update()
    if self.blob is None:
      self.put_text_center(text='No Line Detected')
    else:
      self.put_marks()

  def put_marks(self):
    center = [int(self.blob['cx']), int(self.blob['cy'])]
    cv2.circle(
      self.annotated, center,
      self.__radius, self.__color, self.__thickness)
