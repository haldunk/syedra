# Syedra: A Systems Design Framework

**syedra** framework is a tool kit to implement control and data
processing systems. It is named after the ancient city of
[Syedra](https://syedra.org) located in Alanya, Turkey whose city
plan of concentric circles climbing up a hill top resembles a
heirachy of abstraction layers.

Refer to [index.org](index.org) for hyperlinked detailed
documentation.
  
## Instalation

The package can be installed from pypi by running the following
command:

    pip install syedra

Alternatively, you can install directly from the github repository
using the following command:

    pip install git+https://github.com/haldunk/syedra

To install a specific tagged version or a branch use the following
syntax:

    pip install git+https://github.com/haldunk/syedra@<tag|branch>

## Folders

The project folder consists of the following subfolders:

- [syedra](syedra/) : syedra package sources
- [tutorials](tutorials/) : scripts referred in the tutorials
- [tests](tests/) : unit test files

### Tutorials

Tutorials folder contains a collection of scripts demonstrating the
use of the package. Each script is a stand alone executable.

The scripts should be executed from the top project folder and from
within the development virtual environment and/or a setup where the
syedra package is installed.

    source venv/bin/activate

For instance, the ``tutorial/block/basic.py`` example can be executed
as follows:

    python -m tutorials.block.basic
  
        
## Modules

The following are the modules in the syedra package.
  
### core {#core}

There fundamental building blocks of the framework are collected in
the [core](#core) module.

#### Block

*Block* is a process container primitive with a well specified
input/output interface for data flow. To import Block and associated
classes use the following import.

    from syedra.core.block import Block, InputPort, OutputPort

The [basic.py](tutorials/block/basic.py) demonstrates the basic Block
class definitions. In its most basic form a block may only define a
process in its update() method without any input or output Port.

    class Process(Block):
      block_name = 'Process'

      def update(self):
        print("Process: update()")

Execution of a Block (or a network of Blocks) is initiated by the
Block.execute() method which takes a list of Block instances as the
starting blocks.

The execution may be started from a single Block instance.

    process = Process()
    Block.execute(process)

Or, multiple Block instances.

    process1 = Process()
    process2 = Process()
    Block.execute(process1, process2)

However, the real value of the Block architecture arises from its
ability to describe complex processing pipelines. Intra-Block
connection definitions require Ports. There are two fundamental Port
types: InputPort and OutputPort. The names imply the enforced
direction of the data flow from the Block's perspective.

One can define a Block that only has OutputPorts. These are *source*
blocks.

    class Source(Block):
      block_name = 'Source'

      y = OutputPort(initial=0)

      def update(self):
        self.y = random.randint(0, 10)
  
Similarly, a Block may have only InputPorts. These are *sink* blocks.

    class Sink(Block):
      block_name = 'Sink'

      x = InputPort(initial=0)

      def update(self):
        print(f"- x = {self.x}")

The Block execution is scheduled based on a *token passing
mechanism*. When a block is executed a token is passed to the
InputPort(s) that are connected to the OutputPort of the executed
Block. If all InputPort(s) of a Block instance has a token this Block
instance is marked as *ready to execute* and executed in the next
execution cycle. When there is no Block instance ready for execution
the execution concludes.
  
