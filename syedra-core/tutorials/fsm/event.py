from syedra.core.fsm import Machine, State, Event



class MyEvent(Event):

  @staticmethod
  def static_method(machine:Machine) -> bool:
    print(f"{machine.name}: static_method")
    return True

  def __init__(self):
    super().__init__(check=MyEvent.static_method)
    

def global_function(machine:Machine) -> bool:
  print(f"{machine.name}: global_function")
  return True


class MyMachine(Machine):

  machine_name = 'My Machine'

  def instance_method(self):
    print(f"{self.name}: instance_method")
    return True
  
  a = State()
  b = State()
  c = State()
  d = State()

  using_global_function = Event(check=global_function)
  using_instance_method = Event(check=instance_method)
  custom_shared_event = MyEvent()

  transitions = [
    ('a', 'using_global_function', 'b'),
    ('b', 'using_instance_method', 'c'),
    ('c', 'custom_shared_event', 'd'),
  ]
  initial = 'a'
  

if __name__ == '__main__':

  my_machine = MyMachine()

  for _ in range(4):
    my_machine.update()
