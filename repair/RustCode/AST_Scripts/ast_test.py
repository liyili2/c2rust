import sys
from antlr4 import *
from antlr4.InputStream import InputStream
from antlr4.CommonTokenStream import CommonTokenStream

# Assuming you have generated ANTLR lexer and parser for your language
from XMLExpLexer import XMLExpLexer
from XMLExpParser import XMLExpParser

def main(input_file):


    # Step 1: Read the input file
    input_stream = FileStream(input_file)
 #   input_stream = InputStream(input_file)

    # Step 2: Create a lexer and parser
    lexer = XMLExpLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = XMLExpParser(token_stream)

    # Step 3: Parse the input file to create a parse tree
    cst = parser.program()
    print(cst.toStringTree(recog=parser))



if __name__ == "__main__":
    #input_file = "./xml_test.xml"
    #input_file = "./sumlist.xml"
    input_file = "/home/saitejavinash/Desktop/ProjectC2Rust/c2rust/Benchmarks/Aggregate/rust2xml/src/Aggregate_exp.xml"

    main(input_file)