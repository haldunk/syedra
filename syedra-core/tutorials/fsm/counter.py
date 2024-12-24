from time import sleep
from syedra.core.fsm import Machine, State, Event



class Counter(Machine):
  
  machine_name = 'Counter'
  value = 0

  def add(self):
    self.value += 1
    print(self.value)

  def subtract(self):
    self.value -= 1
    print(self.value)
  
  increment = State(during=add)
  decrement = State(during=subtract)

  upper_limit = Event(check=lambda m: m.value==10)
  lower_limit = Event(check=lambda m: m.value==-10)

  transitions = [
    ('increment', 'upper_limit', 'decrement'),
    ('decrement', 'lower_limit', 'increment'),
  ]
  initial = 'increment'


if __name__ == '__main__':

  counter = Counter()

  try:
    while True:
      counter.update()
      sleep(1)
  except KeyboardInterrupt:
    pass
