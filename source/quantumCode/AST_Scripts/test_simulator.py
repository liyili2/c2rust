#import pytest

from collections import ChainMap
from simulator import *
from XMLExpLexer import XMLExpLexer

####################
## What is input ###

# st : state
# Both inital program and initial values


# env : environment
# How many qubits are in the array


#######################
## What is expected out

# st : state
# assert that get_state() is equal to the state we expect via oracle


# Write a series of tests HERE
class Test_Simulator(object):

    def test_init(self):
        # //We first turn x array to QFT type, and we apply SR gate to rotate the phase of x for 2 pi i * (1/2^10). It will make sense if 10 < rmax, RQFT is the inverse of QFT.
        str = "<pexp gate = 'QFT' > <id> x </id>  <vexp> 0 </vexp> </pexp> <pexp gate = 'SR' > < vexp> 10 </vexp> <id> x </id> </pexp> <pexp gate = 'RQFT' > <id> x </id>  <vexp> 0 </vexp> </pexp> "
        i_stream = InputStream(str)
        lexer = XMLExpLexer(i_stream)
        t_stream = CommonTokenStream(lexer)
        parser = XMLExpParser(t_stream)
        tree = parser.program()
        print(tree.toStringTree(recog=parser))

        # the following shows an example of using 1 variable state. You can have a 10 variable state
        # see that a variable is a string.
        num = 16 # Number of Qubits
        val = 100 #init value
        valArray = calBin(val,num) #conver value to array
        #val = [False]*num # state for x
        state = dict({"x" : Coq_nval(valArray,0)}) #initial a chainMap having variable "x" to be 0 (list of False)
        environment = dict({"x" : num}) #env has the same variables as state, but here, variable is initiliazed to its qubit num
        y = Simulator(state, environment) # Environment is same, initial state varies by pyTest
        y.visitProgram(tree)
        newState = y.get_state()
        assert(132 == calInt(newState.get('x').getBits(), num))

        # Do assertion check that state is as expected
        # Add function to do state (binary-> int ) conversion  #TODO#
        # int n = calInt(arrayQuBits, sizeArray)
        #assert newState == state

def test_trivial():
    Test_Simulator()
    assert True