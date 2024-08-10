from syedra.core.block import Block



class Process(Block):
  block_name = 'Process'

  def update(self):
    print("Process: update()")    


if __name__ == '__main__':

  process = Process()
  Block.execute(process)

