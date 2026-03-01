import unittest
from antlr4 import *
from collections import ChainMap
from types import NoneType
from ExpListener import ExpListener
from ExpLexer import ExpLexer
from ExpParser import ExpParser
from XMLVisitor import XMLVisitor
import sys
sys.path.append('../')
from typechecker import TypeName
from typechecker import Nor
from typechecker import QFT

class MyTestCase(unittest.TestCase):
    def test_something(self):
        i_stream = InputStream("X (x,0) ; CU (x,0) (CU (x,1) (X (y,1); X (y,1)))")
        lexer = ExpLexer(i_stream)
        t_stream = CommonTokenStream(lexer)
        parser = ExpParser(t_stream)
        tree = parser.program()
        newmap = ChainMap({'x' : Nor(), 'y' : QFT(10)})
        xml = XMLVisitor(newmap)
        result = tree.accept(xml)
        print(xml.getXML())
        #self.assertEqual(True, False)  # add assertion here
  #walker = ParseTreeWalker()
#y = XMLVisitor.XMLVisitor()

if __name__ == '__main__':
    unittest.main()
