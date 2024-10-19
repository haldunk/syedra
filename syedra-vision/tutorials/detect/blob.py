import cv2
from syedra.core.block import Block
from syedra.vision.camera import Camera
from syedra.vision.display import Display, BlobSketch
from syedra.vision.keyboard import Keyboard
from syedra.vision.transform import Convert
from syedra.vision.detect import Mask, Blob



if __name__ == '__main__':

  camera = Camera(index=0)
  converter = Convert(mapping=Convert.Mapping.BGR2HSV)
  mask = Mask(
    lower_color=[108, 50, 50],
    upper_color=[111, 255, 255])
  blob = Blob(min_size=200)
  display_original = Display(name='Original')
  display_converted = Display(name='Converted')
  display_masked = Display(name='Masked')
  sketch_blob = BlobSketch()
  display_blob = Display(name='Blob Sketch')
  keyboard = Keyboard()

  camera['frame'] >> converter['original']
  converter['converted'] >> mask['original']
  mask['selected'] >> blob['image']
  blob['detected'] >> sketch_blob['blob']
  camera['frame'] >> sketch_blob['image']
  
  camera['frame'] >> display_original['image']
  converter['converted'] >> display_converted['image']
  mask['selected'] >> display_masked['image']
  sketch_blob['annotated'] >> display_blob['image']
  display_blob['ready'] >> keyboard['show']

  try:
    Block.execute(camera)
  except Keyboard.QuitCommand:
    pass
