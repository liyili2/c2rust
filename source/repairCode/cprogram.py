import random
from pyggi.tree import TreeProgram
from .cresult import CResult
import xml.etree.ElementTree as ET
import re
import os


class CProgram(TreeProgram):
    """
    A Program 
    """

    def __init__(self, project_path):
        """
        :param number_of_variables: Number of decision variables of the problem.
        :param prg: Program object from pyggi
        """
        super(TreeProgram, self).__init__(project_path)
        self.path = project_path
        self.operators = []

        # Determine if project_path is a directory
        if os.path.isdir(project_path):
            # Find an XML file in the directory
            xml_files = [f for f in os.listdir(project_path) if f.endswith('.xml')]
            if not xml_files:
                raise FileNotFoundError("No XML file found in the provided directory.")
            # Use the first XML file found
            xml_file_path = os.path.join(project_path, xml_files[0])
        else:
            # Use the provided file path directly
            xml_file_path = project_path

        # Read and parse the XML content
        with open(xml_file_path, 'r') as file:
            self.xml_content = file.read()
        self.tree = ET.ElementTree(ET.fromstring(self.xml_content))

    def get_xml_string(self):
        """
        Returns the entire XML content as a string.
        """
        return ET.tostring(self.tree.getroot(), encoding='unicode', method='xml')

    def __str__(self):
        return self.get_xml_string()

    def compute_fitness(self, result, return_code=0, stdout=0, stderr=0, elapsed_time=0):
        """
        Given a program, compute the fitness by parsing the pyTest output
        """
        # print('start computing fitness')
        # print("stdout",stdout)
        m = re.findall("runtime: ([0-9.]+)", stdout)

        # m = re.findall("runtime: (\d+\.\d+)s", stdout)
        print(f'Runtime: {m}')
        if len(m) > 0:
            runtime = m[0]
            failed_list = re.findall("([0-9]+) failed", stdout)
            if len(failed_list) > 0:
                failed = int(failed_list[0])
            else:
                failed = 0
            passed_list = re.findall("([0-9]+) passed", stdout)
            if len(passed_list) > 0:
                passed = int(passed_list[0])
            else:
                passed = 0
            total_tests = failed + passed

            result.fitness = failed
            # result.fitness = passed / total_tests if total_tests > 0 else 0
            # print(f'Fitness: {result.fitness}')
        else:
            result.status = 'PARSE_ERROR'
            result.fitness = 1000000  # Large Value
        # Print Fitness
        print(f'Status: {result.status}')
        print(f'Fitness: {result.fitness}')
        return result

    def stopping_criterion(self, iters, fitness):
        return fitness <= self.BEST

    def name(self) -> str:
        return "CProgram"

    def app_target(self, target_file=None, method="random"):
        '''
        Similar to random target but tuned for app insertation

        '''
        if target_file is None:
            target_file = target_file or random.choice(self.target_files)
        assert target_file in self.target_files

        # Matches all occurences of ./let[1]/match[1]/pair[1-9](one or more occurence of app[1-9], if[1-9], or pexp[1-9]) then nothing after
        # Example: Matches: ./let[1]/match[1]/pair[1]/pexp[1] and ./let[1]/match[1]/pair[2]/app[1]/vexp[1]
        # Does not match: ./let[1]/match[1]/vexp[1] or ./let[1]/match[1]/pair[2]/app[1]/vexp[1]/let[1] 
        valid_path_regex = re.compile(r'\./let\[1\]/match\[1\]/pair\[\d+\](/(pexp|if|app)\[\d+\])+$')
        valid_indices = [i for i, point in enumerate(self.modification_points[target_file]) if
                         valid_path_regex.match(point)]
        assert method in ['random', 'weighted']

        if method == 'random' or target_file not in self.modification_weights:
            return (target_file, random.choice(valid_indices))

    # jMetal required functions

    def evaluate_solution(self, patch, test_command):
        '''
        Apply the edit list to the program and run the test command (pyTest)
        '''
        self.apply(patch)
        # print(patch, "\n")
        # return_code is the return code of the program execution
        tout = 10
        rcode, stdout, stderr, elapsed = self.exec_cmd(test_command, timeout=tout)
        result = CResult('SUCCESS', None)
        self.compute_fitness(result, rcode, stdout, stderr, elapsed)
        # print("=== STDOUT ===")
        # print(stdout)
        # print("=== STDERR ===")
        # print(stderr)
        return result
