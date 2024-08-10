from typing import List
import cv2
from system.block import Block, InputPort, OutputPort


__all__ = [
  'Mask',
  'Blob',
]


class Mask(Block):

  original = InputPort()
  selected = OutputPort(initial=None)

  def __init__(self,
               lower_color:List[int],
               upper_color:List[int],
               name:str='Mask'):
    super().__init__(name=name)
    self.set_color_range(lower_color, upper_color)

  def set_color_range(self, lower_color, upper_color):
    self.__lower = np.array(lower_color)
    self.__upper = np.array(upper_color)

  def update(self):
    if self.original is not None:
      self.selected = cv2.inRange(
        self.original, self.__lower, self.__upper)
    else:
      self.selected = None


class Blob(Block):

  image = InputPort(initial=None)
  detected = OutputPort(initial=None)
  
  def __init__(self,
               min_size:int=200,
               name:str='Blob Detector'):
    super().__init__(name=name)
    self.set_min_size(min_size)

  def set_min_size(self, min_size:int):
    self.__min_size = min_size

  def update(self):
    if self.image is None:
      self.blob = None
      return
    contours, _ = cv2.findContours(
      self.image, cv2.RETR_EXTERNAL,
      cv2.CHAIN_APPROX_SIMPLE)
    areas = [cv2.contourArea(c) for c in contours]
    if areas and max(areas) >= self.__min_size:
      largest_blob = sorted(
        [c for c,a in zip(contours, areas) if a >= self.__min_size],
        key=lambda c: cv2.contourArea(c), reverse=True)[0]
      centroid, axes, angle = cv2.fitEllipse(largest_blob)
      self.detected = {
        'cx': centroid[0],
        'cy': centroid[1],
        'minor': axes[0],
        'major': axes[1],
        'angle': angle,
      }
    else:
      self.detected = None


