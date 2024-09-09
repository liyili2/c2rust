import xml.etree.ElementTree as ET
import pytest
import time

# The XML string with properly escaped special characters
xml_string = """
<function name="aggregate">
    <parameters>
        <param name="lst" type="i32[]"/>
    </parameters>
    <variables>
        <var name="length" expression="len(lst)"/>
        <var name="ret" type="i32[]" size="((length &gt;&gt; 1) + (length &amp; 0b1))" defaultValue="0"/>
    </variables>
    <logic>
        <for from="0" to="len(lst)">
            <if condition="i % 2 == 1">
                <assignment>
                    <target>ret[i // 2]</target>
                    <value>ret[i // 2] + lst[i]</value>
                </assignment>
            </if>
            <else>
                <assignment>
                    <target>ret[i // 2]</target>
                    <value>lst[i]</value>
                </assignment>
            </else>
        </for>
    </logic>
    <return>ret</return>
</function>
"""

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

def test_aggregate():
    print("Running....")
    assert aggregate_from_xml([]) == []
    assert aggregate_from_xml([1, 2, 3, 4,5]) == [3, 7, 5]
    assert aggregate_from_xml([-10, -20, 20-30, 40, 50]) == [30, 70, 50]
    assert aggregate_from_xml([]) == []
    assert aggregate_from_xml([5]) == [5]

@pytest.fixture(scope="session", autouse=True)
def starter(request):
    start_time = time.time()

    def finalizer():
        print("runtime: {}".format(str(time.time() - start_time)))

    request.addfinalizer(finalizer)

if __name__ == "__main__":
    pytest.main(['-v'])

