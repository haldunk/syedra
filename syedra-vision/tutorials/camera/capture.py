from syedra.core.block import Block
from syedra.vision.camera import Camera
from syedra.vision.display import Display
from syedra.vision.keyboard import Keyboard



if __name__ == '__main__':

  camera = Camera(index=0)
  display = Display()
  keyboard = Keyboard()

  camera['frame'] >> display['image']
  display['ready'] >> keyboard['show']
  
  try:
    Block.execute(camera)
  except Keyboard.QuitCommand:
    pass
