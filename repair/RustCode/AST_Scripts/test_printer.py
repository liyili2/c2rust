#import pytest

from collections import ChainMap

from antlr4 import InputStream, CommonTokenStream

from RustCode.AST_Scripts.XMLExpParser import XMLExpParser
from RustCode.AST_Scripts.XMLPrinter import XMLPrinter
#from simulator import *
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
        #
        str = " <STMT type = Block> <STMT type = Let> <ID> some_number </ID> <VEXP> 7 </VEXP> </STMT> <STMT type = Let> add_number <VEXP OP = Plus> <ID> some_number </ID> <VEXP> 3 </VEXP> </VEXP> </STMT> </STMT> "

        i_stream = InputStream(str)
        lexer = XMLExpLexer(i_stream)
        t_stream = CommonTokenStream(lexer)
        parser = XMLExpParser(t_stream)
        tree = parser.program()
        # for xml printer:
        newprint = XMLPrinter()
        stringa = newprint.visitProgram(tree)

        print(stringa) # for xml printer: XMLVisitor newprint = XMLVisitor()

        # test things out to figure out why nothing is being printed


        # assert()

        # Do assertion check that state is as expected
        # Add function to do state (binary-> int ) conversion  #TODO#
        # int n = calInt(arrayQuBits, sizeArray)
        #assert newState == state

def test_trivial():
    print("Happy")
    # Now, I need to create the object (Test_Simulator()), and call its function.
    tester = Test_Simulator().test_init()
    # assert True

test_trivial()