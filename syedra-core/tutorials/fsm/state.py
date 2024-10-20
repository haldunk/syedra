from syedra.core.fsm import Machine, State, Event


class MyState(State):

  @staticmethod
  def enter(machine:Machine):
    print(f"{machine.name}: enter")
  
  def __init__(self):
    super().__init__(ingress=MyState.enter)
    

def depart(machine:Machine):
  print(f"{machine.name}: depart")
  
  
class MyMachine(Machine):
  
  machine_name = 'My Machine'

  def arrive(self):
    print(f'{self.name}: arrive')
  
  using_instance_method = State(ingress=arrive)
  using_global_function = State(egress=depart)
  custom_shared_state = MyState()

  always_true = Event(check=lambda machine: True)
  
  transitions = [
    ('using_instance_method', 'always_true', 'using_global_function'),
    ('using_global_function', 'always_true', 'custom_shared_state'),
  ]
  initial = 'using_instance_method'



if __name__ == '__main__':

  my_machine = MyMachine()
  for _ in range(3):
    my_machine.update()
