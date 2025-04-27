from __future__ import annotations
import asyncio
from functools import reduce
from typing import Type, List
from enum import Enum
from functools import reduce



__all__ = [
  'Block',
  'Port',
  'InputPort',
  'OutputPort',
  'ProxyPort',
]


class Port:
  '''Port is a descriptor employed to get and set block
  port node instances.'''

  class NotSetupError(Exception):
    def __init__(self, port:Port):
      super().__init__("Port has not been setup")

  class DoesNotExist(Exception):
    def __init__(self, block:Block, name:str):
      super().__init__(
        f"Port {name} does not exist in Block {block}")

  class ImmutableError(Exception):
    def __init__(self, block:Block, port:Port):
      super().__init__(
        f"Port {port} on Block {block} is immutable")

  class CannotInitializeError(Exception):
    def __init__(self, port:Port):
      super().__init__(
        f"Port {port} cannot be initialized")

  class ConflictError(Exception):
    def __init__(self, block:Block):
      super().__init__(
        f"Port name conflict in Block {block}")
      
      
  class Kind(Enum):
    INPUT = 'I'
    OUTPUT = 'O'
    PROXY = 'P'
  
  def __init__(self, kind:Kind, initial=None, internal=False):
    self._kind = kind
    self._name = None
    if initial is not None and self._kind == Port.Kind.PROXY:
      raise Port.CannotInitializeError(port=self)
    self._initial = initial
    self._internal = internal

  @property
  def is_input(self):
    return self._kind == Port.Kind.INPUT

  @property
  def is_output(self):
    return self._kind == Port.Kind.OUTPUT

  @property
  def is_internal(self):
    return self._internal

  @property
  def initial(self):
    return self._initial

  def __get__(self, block:Block, owner):
    return block._latches[self._name]._node.value

  def __set__(self, block:Block, value):
    if self.is_output:
      block._latches[self._name]._node.value = value
    else:
      raise Port.ImmutableError(block=block, port=self)
  
  def __str__(self):
    if self._name:
      return self._name
    else:
      raise Port.NotSetupError(self)
  

class InputPort(Port):
  '''Input kind Port'''

  def __init__(self, initial=None, internal=False):
    super().__init__(
      kind=Port.Kind.INPUT, initial=initial, internal=internal)


class OutputPort(Port):
  '''Output kind Port'''

  def __init__(self, initial=None):
    super().__init__(kind=Port.Kind.OUTPUT, initial=initial)
    

class ProxyPort(Port):
  '''Proxy kind Port'''

  def __init__(self, initial=None):
    super().__init__(kind=Port.Kind.PROXY, initial=initial)
    
    
class BlockMeta(type):

  def __new__(cls, name, bases, attrs):
    ports = dict()
    parents = [b for b in bases if isinstance(b, BlockMeta)]
    for parent in parents:
      ports.update(parent._ports)
    for name,port in attrs.items():
      if isinstance(port, Port):
        port._name = name
        ports[name] = port
    attrs['_ports'] = ports
    return super().__new__(cls, name, bases, attrs)
  
  
class Block(metaclass=BlockMeta):

  class Terminated(Exception):
    def __init__(self):
      super().__init__("Block system execution terminated")
  
  __collection = set()

  block_name = None
  
  def __init__(self, name:str=None, superblock:Block=None):
    self.__name = name or self.block_name
    assert self.__name, \
      'A non emptry string name must be assigned'
    self.__superblock = superblock
    self.__init_latches()
    self._token = False
    Block.__collection.add(self)
    self.__execution_cohord = [self]
    if superblock:
      superblock.__execution_cohord.append(self)
    try:
      asyncio.get_running_loop()
      self.__loop = asyncio.get_event_loop()
      self.__lock = asyncio.Lock()
    except RuntimeError:
      self.__loop = None
      self.__lock = None

  @property
  def execution_cohord(self):
    return self.__execution_cohord
      
  def __init_latches(self):
    self._latches = {
      name: Latch(block=self, port=port)
      for name,port in self._ports.items()}
    self._inputs = [
      latch for latch in self.latches()
      if latch.is_input]
    self._outputs = [
      latch for latch in self.latches()
      if latch.is_output]

  def _add_port(self, port_name, port_cls, **kwargs):
    '''This method is used when block ports need to be
    created dynamically'''
    if hasattr(self, port_name):
      raise Port.ConflictError(block=self)
    port = port_cls(**kwargs)
    port._name = port_name
    setattr(self, port_name, port)
    self._ports[port_name] = port
    self.__init_latches()
      
  @property
  def name(self) -> str:
    return self.__name

  def __str__(self):
    return self.name

  def __getitem__(self, name:str) -> Node:
    '''Returns the Node instance that the named port of the
    block is attached to.'''
    try:
      return self._latches[name]._node
    except KeyError:
      raise Port.DoesNotExist(
        block=self, name=name)

  def __call__(self, name:str) -> Latch:
    '''Returns the Latch instance for the named port of the
    block.'''
    try:
      return self._latches[name]
    except KeyError:
      raise Port.DoesNotExist(
        block=self, name=name)

  def update(self):
    '''Block process specification'''
    pass

  async def async_update(self):
    '''Asynchronous update process coroutine'''
    assert self.__loop, 'Block is not in an asynchronous loop'
    async with self.__lock:
      await self.__loop.run_in_executor(None, self.update)
    
  @staticmethod
  def all():
    return Block.__collection

  def latches(self):
    return self._latches.values()

  @property
  def inputs(self):
    return self._inputs

  @property
  def outputs(self):
    return self._outputs

  @staticmethod
  def clear_input_latch_tokens(*blocks:List[Block]):
    for block in blocks:
      for latch in block.inputs:
        latch.token = False

  @staticmethod
  def set_output_latch_tokens(*blocks:List[Block]):
    for block in blocks:
      for latch in block.outputs:
        latch.token = True

  @staticmethod
  def get_execution_ready_blocks() -> List[Block]:
    blocks = list()
    for block in Block.all():
      input_tokens = [inp.token for inp in block.inputs]
      if (block.inputs and all(input_tokens)):
        blocks.append(block)
    return blocks
      
  @staticmethod
  def execute(*start:List[Block]):
    assert start, \
      'At least one block must be specified as start block'
    assert all([isinstance(b, Block) for b in start]), \
      'Input must be a list of Block instances'
    blocks = reduce(
      lambda a,b: a+b, [b.execution_cohord for b in start], [])
    try:
      while blocks:
        Block.clear_input_latch_tokens(*blocks)
        for block in blocks:
          block.update()
        Block.set_output_latch_tokens(*blocks)
        ready_blocks = Block.get_execution_ready_blocks()
        blocks = reduce(
          lambda a,b: a+b,
          [b.execution_cohord for b in ready_blocks], [])
    except Block.Terminated:
      pass
    finally:
      Block.clear_input_latch_tokens(*Block.all())
      
  @staticmethod
  async def async_execute(*start:List[Block]):
    assert start, \
      'At least one block must be specified as start block'
    assert all([isinstance(b, Block) for b in start]), \
      'Input must be a list of Block instances'
    blocks = reduce(
      lambda a,b: a+b, [b.execution_cohord for b in start], [])
    try:
      while blocks:
        Block.clear_input_latch_tokens(*blocks)
        for block in blocks:
          await block.async_update()
        Block.set_output_latch_tokens(*blocks)
        ready_blocks = Block.get_execution_ready_blocks()
        blocks = reduce(
          lambda a,b: a+b,
          [b.execution_cohord for b in ready_blocks], [])
    except Block.Terminated:
      pass
    finally:
      Block.clear_input_latch_tokens(*Block.all())

      
class Latch:
  '''Latch is a particular instance of a port in a block
  instance.'''

  class NotNodeMemberError(Exception):
    def __init__(self, node:Node, latch:Latch):
      super().__init__(
        f"Latch {latch} is not a member of Node {node}")

  def __init__(self, block:Block, port:Port):
    self._block = block
    self._port = port
    self._node = Node(latch=self)
    self._token = False

  def __str__(self):
    return "{}:{}".format(self._block, self._port)
  
  @property
  def initial(self):
    return self._port.initial

  @property
  def is_output(self):
    return self._port.is_output

  @property
  def is_input(self):
    return self._port.is_input
  
  @property
  def token(self):
    return self._token

  @token.setter
  def token(self, state:bool):
    if self.is_input:
      self._token = state
    else:
      connected_input_latches = filter(
        lambda l: l.is_input, self._node._latches)
      for latch in connected_input_latches:
        latch.token = state
        
  def detach(self):
    return self._node != self

        
class Node:
  '''Node object is the value storage entity for a set of
  _connected_ Latch instances(s). Nodees can also be
  considered as the nodes in the data pipeline graph. Its
  value content is set and get through the use of the
  associated Port descriptor. For any Node there can be at
  most one OUTPUT kind associated port.

  '''

  __collection = set()

  class MergeError(Exception):
    def __init__(self, node1:Node, node2:Node):
      super().__init__(
        f"{node1} and {node2} are both driven "
        "cannot be merged")

  class UnconsumedToken(Exception):
    def __init__(self, node:Node):
      super().__init__(
        f"Attempting to set value before token is passed")
      
  def __init__(self, latch:Latch, initial=None):
    self._latches = set([latch])
    self._value = initial or latch.initial
    self._name = str(latch)
    self.__is_driven = latch._port.is_output
    self.__is_internal = latch._port.is_internal
    Node.__collection.add(self)

  def __str__(self):
    return self._name
    
  @property
  def value(self):
    return self._value

  @value.setter
  def value(self, v):
    self._value = v

  def __update_name(self):
    self._name = '|'.join([str(l) for l in self._latches])
  
  def __merge(self, node:Node):
    if self.__is_driven and node.__is_driven:
      raise Node.MergeError(node1=self, node2=node)
    else:
      self._latches |= node._latches
      self.__is_driven |= node.__is_driven
      if node.__is_driven:
        self.value = node.value
      for latch in node._latches:
        latch._node = self
      Node.__collection.remove(node)
      self.__update_name()
      return self

  def __remove(self, latch:Latch):
    if latch in self._latches:
      self._latches.remove(latch)
      latch._node = Node(
        latch=latch, initial=self.value)
      if len(self._latches):
        self.__update_name()
        self.__is_driven = not latch.is_output
        return self
      else:
        Node.__collection.remove(self)
        return None
    else:
      raise Latch.NotNodeMemberError(
        node=self, latch=latch)
    
  def __rshift__(self, node:Node):
    return self.__merge(node)

  def __lshift__(self, node:Node):
    return self.__merge(node)

  def __ne__(self, latch:Latch):
    return self.__remove(latch=latch)


