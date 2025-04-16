from antlr4 import *
from RustListener import RustListener
from RustLexer import RustLexer
from RustParser import RustParser

def main():
  base_adderss = "../../../c2safeRust_examples/"
  file_name = "aggregate.rs"
  #giveMeInput = input("(x,0)\n")
  file_path = base_adderss + file_name
  # i_stream = InputStream("fn main() {let a: i32 = 1;}")
  i_stream = FileStream(fileName=file_path)
  lexer = RustLexer(i_stream)
  t_stream = CommonTokenStream(lexer)
  parser = RustParser(t_stream)
  tree = parser.program()

  with open(file_name+".txt", "w", encoding='utf-8') as f:
    f.write("Here's the parsing result:\n")
    f.write(tree.toStringTree(recog=parser))
  # print("here's the parsing result: ", tree.toStringTree(recog=parser))
  #walker = ParseTreeWalker()
  # y = simulator(state, environment) # Environment is same, initial state varies by pyTest
  # y.visitProgram(tree)
  # state = y.get_state()

  # Do assertion check that state is as expected
  # Add function to do state (binary-> int ) conversion  #TODO#
  # int n = calInt(arrayQuBits, sizeArray)
  # Then ASSERT 

#y = XMLVisitor.XMLVisitor()

if __name__ == "__main__":
    main()