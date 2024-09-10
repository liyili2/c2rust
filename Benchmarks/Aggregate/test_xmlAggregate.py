import xml.etree.ElementTree as ET
import pytest
import time


# Function to read XML from a file
def read_xml_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Use the read_xml_from_file function to load the XML
xml_file_path = "aggregate.xml"  # Path to your XML file
xml_string = read_xml_from_file(xml_file_path)


def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    function_name = root.attrib['name']
    parameters = [param.attrib for param in root.find('parameters').findall('param')]
    variables = [var.attrib for var in root.find('variables').findall('var')]
    logic = root.find('logic')
    return_statement = root.find('return').text
    
    return function_name, parameters, variables, logic, return_statement

def generate_code_from_logic(logic_element):
    code_lines = []
    for element in logic_element:
        if element.tag == 'for':
            code_lines.append(f"for i in range({element.attrib['from']}, {element.attrib['to']}):")
            code_lines += ["    " + line for line in generate_code_from_logic(element)]
        elif element.tag == 'if':
            condition = element.attrib['condition']
            code_lines.append(f"if {condition}:")
            code_lines += ["    " + line for line in generate_code_from_logic(element)]
        elif element.tag == 'assignment':
            target = element.find('target').text
            value = element.find('value').text
            code_lines.append(f"{target} = {value}")
        elif element.tag == 'else':
            code_lines.append("else:")
            code_lines += ["    " + line for line in generate_code_from_logic(element)]
    return code_lines

def generate_function_code(function_name, parameters, variables, logic_element, return_statement):
    param_str = ", ".join([param['name'] for param in parameters])
    code = f"def {function_name}({param_str}):\n"
    
    for var in variables:
        if 'size' in var:
            size_expr = var['size'].replace('&gt;&gt;', '>>').replace('&amp;', '&')
            code += f"    {var['name']} = [0] * ({size_expr})\n"
        else:
            code += f"    {var['name']} = {var['expression']}\n"
    
    logic_code = generate_code_from_logic(logic_element)
    code += "\n".join(["    " + line for line in logic_code])
    code += f"\n    return {return_statement}"
    
    return code

def aggregate_from_xml(lst):
    function_name, parameters, variables, logic_element, return_statement = parse_xml(xml_string)
    code = generate_function_code(function_name, parameters, variables, logic_element, return_statement)
    
    print("Generated Python Code:\n", code)
    
    local_vars = {'lst': lst, 'len': len}
    exec(code, {}, local_vars)
    
    return local_vars[function_name](lst)

def test_aggregate_empty():
    assert aggregate_from_xml([]) == []

def test_aggregate_natnum():
    assert aggregate_from_xml([1, 2, 3, 4, 5]) == [3, 7, 5]

def test_aggregate_even_num():
    assert aggregate_from_xml([1, 2, 3, 4]) == [3, 7]

def test_aggregate_single_element():
    assert aggregate_from_xml([5]) == [5]

def test_aggregate_all_same_elements():
    assert aggregate_from_xml([2, 2, 2, 2]) == [4, 4]

def test_aggregate_negative_numbers():
    assert aggregate_from_xml([-1, -2, -3, -4]) == [-3, -7]

def test_aggregate_mixed_pos_neg():
    assert aggregate_from_xml([1, -2, 3, -4]) == [-1, -1]

def test_aggregate_zeroes():
    assert aggregate_from_xml([0, 0, 0, 0]) == [0, 0]

def test_aggregate_large_numbers():
    assert aggregate_from_xml([1000, 2000, 3000, 4000]) == [3000, 7000]

def test_aggregate_mixed_data_types():
    assert aggregate_from_xml([1.5, 2.5, 3.5, 4.5]) == [4.0, 8.0]

def test_aggregate_alternating_pos_neg():
    assert aggregate_from_xml([10, -10, 20, -20, 30]) == [0, 0, 30]

def test_aggregate_max_integers():
    assert aggregate_from_xml([2147483647, 2147483647, 2147483647, 2147483647]) == [4294967294, 4294967294]

def test_aggregate_increasing_sequence():
    assert aggregate_from_xml([1, 2, 3, 4, 5, 6]) == [3, 7, 11]

def test_aggregate_decreasing_sequence():
    assert aggregate_from_xml([6, 5, 4, 3, 2, 1]) == [11, 7, 3]

def test_aggregate_single_pair():
    assert aggregate_from_xml([7, 8]) == [15]

def test_aggregate_large_sequential():
    assert aggregate_from_xml(list(range(1, 101))) == [sum(pair) for pair in zip(range(1, 101, 2), range(2, 102, 2))]

def test_aggregate_floating_point_precision():
    assert aggregate_from_xml([0.1, 0.2, 0.3, 0.4]) == [0.3, 0.7]

def test_aggregate_alternating_large_negatives():
    assert aggregate_from_xml([1000, -100000, 2000, -200000]) == [-99000, -198000]


@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)

if __name__ == "__main__":
    pytest.main(['-v'])

