import os, sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

class Program():
    def __init__(self, items, path=None):
        # super().__init__(path=path)
        self.items = items  # A list of FunctionDef, StructDef, etc.
        self.path = path

    def accept(self, visitor):
        return visitor.visit_Program(self)

    def get_file_extension(file_path):
        """
        :param file_path: The path of file
        :type file_path: str
        :return: file extension
        :rtype: str
        """
        _, file_extension = os.path.splitext(file_path)
        return file_extension

    @classmethod
    def get_engine(cls, file_name):
        pass
    #     _, extension = os.path.splitext(file_name)
    #     if extension == '.rs':
    #         return RustEngine
    #     elif extension in ['.py']:
    #         return AstorEngine
    #     elif extension in ['.xml']:
    #         return XmlEngine
        # raise Exception(f'Unsupported file extension: {extension}')
