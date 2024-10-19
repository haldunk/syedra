from syedra.core.block import Block
from syedra.vision.camera import Camera
from syedra.vision.display import Display
from syedra.vision.keyboard import Keyboard
from syedra.vision.transform import Crop



if __name__ == '__main__':

  camera = Camera(index=0)
  crop = Crop(left=100, right=300, top=400, bottom=480)
  display_original = Display(name='Original')
  display_cropped = Display(name='Cropped')
  keyboard = Keyboard()

  camera['frame'] >> crop['original']
  crop['cropped'] >> display_cropped['image']
  camera['frame'] >> display_original['image']
  display_cropped['ready'] >> keyboard['show']

  try:
    Block.execute(camera)
  except Keyboard.QuitCommand:
    pass
