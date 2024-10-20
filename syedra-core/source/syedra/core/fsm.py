from __future__ import annotations
from typing import Callable, List, Tuple


__all__ = [
  'Machine',
  'State',
  'Event',
]


class State:

  def __init__(self,
               ingress:Callable[[Machine], None]=None,
               during:Callable[[Machine], None]=None,
               egress:Callable[[Machine], None]=None):
    self._name = None
    self._machine = None
    self.__ingress = ingress
    self.__during = during
    self.__egress = egress

  def __str__(self):
    return self._name
    
  def ingress(self):
    if callable(self.__ingress):
      self.__ingress(self._machine)

  def during(self):
    if callable(self.__during):
      self.__during(self._machine)

  def egress(self):
    if callable(self.__egress):
      self.__egress(self._machine)
  

class Event:

  def __init__(self, check:Callable[[Machine], bool]=None):
    self._name = None
    self._machine = None
    self.__check = check

  def __str__(self):
    return self._name
  
  def check(self) -> bool:
    if callable(self.__check):
      return self.__check(self._machine)
    else:
      return False

  @property
  def is_occured(self) -> bool:
    return self.check()

  
class MachineMeta(type):

  def __new__(cls, name, bases, attrs):
    states = dict()
    events = dict()
    for name,attr in attrs.items():
      if isinstance(attr, State):
        attr._name = name
        states[name] = attr
      if isinstance(attr, Event):
        attr._name = name
        events[name] = attr
    attrs['_states'] = states
    attrs['_events'] = events
    return super().__new__(cls, name, bases, attrs)


class Machine(metaclass=MachineMeta):

  machine_name:str = None
  transitions:List[Tuple[str, str, str]] = []
  initial:str = None

  class ImproperConfiguration(Exception):

    def __init__(self, message):
      super().__init__(f"Improper configuration: {message}")

      
  def __init__(self, name:str=None):
    self.__name = name or self.machine_name
    if self.__name is None:
      raise Machine.ImproperConfiguration(
        "A non empty string name must be assigned")
    for state in self._states.values():
      state._machine = self
    for event in self._events.values():
      event._machine = self
    self._setup()
      
  @property
  def name(self) -> str:
    return self.__name

  def __str__(self):
    return self.name

  def get_initial(self):
    if self.initial in self._states:
      return self.initial
    elif self.initial is None:
      raise Machine.ImproperConfiguration(
        "initial property and/or get_initial() must be specified")
    else:
      raise Machine.ImproperConfiguration(
        f"Specified initial state ({self.initial}) is not a machine state")
      
  def _setup(self):
    self.__transitions = dict()
    for transition in self.transitions:
      source = self._states[transition[0]]
      event = self._events[transition[1]]
      target = self._states[transition[2]]
      if source in self.__transitions:
        self.__transitions[source][event] = target
      else:
        self.__transitions[source] = {event: target}
    self.__initial = self._states[self.get_initial()]
    self.__current = None
      
  def print(self):
    print("-> {}".format(self.__initial))
    for source,transitions in self.__transitions.items():
      for event,target in transitions.items():
        print("({})-|{}|->({})".format(
          source, event, target))

  def update(self):
    if self.__current is None:
      self.__current = self.__initial
      self.__current.ingress()
    else:
      transitions = self.__transitions[self.__current]
      for event,target in transitions.items():
        if event.is_occured:
          self.__current.egress()
          self.__current = target
          self.__current.ingress()
          break
    self.__current.during()
        

