import sys
from cluster.common import terminal
# own stuff
from mypackage import mypackedmodule
import mymodule

def greet():
    print(f"Hello, from demo input file!")
greet()
mypackedmodule.greet()
mymodule.greet()
prompt_response = terminal.prompt_for_confirm("Do you like herbivores?", ['y','n','c'])
if prompt_response == 'y':
    __response__ = "Your dinosaur is Diplodocus"
elif prompt_response == 'n':
    __response__ = "Your dinosaur is Rex"

print('Your dinosaur has been stored in __response__ so it can be accessed from the executive.')
sys.exit()
