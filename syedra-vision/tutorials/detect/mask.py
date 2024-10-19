import cv2
from syedra.core.block import Block
from syedra.vision.camera import Camera
from syedra.vision.display import Display
from syedra.vision.keyboard import Keyboard
from syedra.vision.transform import Convert
from syedra.vision.detect import Mask



if __name__ == '__main__':

  camera = Camera(index=0)
  converter = Convert(mapping=Convert.Mapping.BGR2HSV)
  mask = Mask(
    lower_color=[60, 50, 50],
    upper_color=[70, 255, 255])
  display_original = Display(name='Original')
  display_converted = Display(name='Converted')
  display_masked = Display(name='Masked')
  keyboard = Keyboard()

  camera['frame'] >> converter['original']
  converter['converted'] >> mask['original']
  camera['frame'] >> display_original['image']
  converter['converted'] >> display_converted['image']
  mask['selected'] >> display_masked['image']
  display_masked['ready'] >> keyboard['show']

  try:
    Block.execute(camera)
  except Keyboard.QuitCommand:
    pass
