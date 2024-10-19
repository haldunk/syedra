import cv2
from syedra.core.block import Block
from syedra.vision.camera import Camera
from syedra.vision.display import Display
from syedra.vision.keyboard import Keyboard
from syedra.vision.transform import Convert



if __name__ == '__main__':

  camera = Camera(index=0)
  converter = Convert(mapping=Convert.Mapping.BGR2HSV)
  display_original = Display(name='Original')
  display_converted = Display(name='Converted')
  keyboard = Keyboard()

  camera['frame'] >> converter['original']
  camera['frame'] >> display_original['image']
  converter['converted'] >> display_converted['image']
  display_converted['ready'] >> keyboard['show']

  try:
    Block.execute(camera)
  except Keyboard.QuitCommand:
    pass
