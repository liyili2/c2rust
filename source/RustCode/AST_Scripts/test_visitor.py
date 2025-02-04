from ProgramVisitor import *
from XMLProgrammer import *
#from XMLProgrammer import Range_exp
from ProgramTransformer import *
from antlr4 import FileStream, CommonTokenStream
from XMLExpLexer import XMLExpLexer
from XMLExpParser import XMLExpParser
from XMLPrinter import XMLPrinter

def main(input_file):
    # Read the input file
    input_stream = FileStream(input_file)

    # Create a lexer and parser
    lexer = XMLExpLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    # Parse the input file to create a parse tree
    parser = XMLExpParser(token_stream)
    tree = parser.program()
#    print(tree, type(tree))
    
#    range = Range_exp(3, 4)
#    print(f"Let's check the range_exp type,{range}, {type(range)}")

    # Create an instance of the ProgramTransformer
    transformer = ProgramTransformer()

    program = transformer.visitProgram(tree)

    visitor = ProgramVisitor()
#    printer = XMLPrinter()
    
    # Visit the XMLProgrammer object
#    ast = printer.visit(program)
    ast = visitor.visit(program)
    print('ast', ast)
    
if __name__ == "__main__":
    input_file = "./xml_test.xml"
    main(input_file)
