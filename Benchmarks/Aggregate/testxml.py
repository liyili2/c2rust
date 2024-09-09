import xml.etree.ElementTree as ET
import pytest
import time

# The XML string with escaped special characters for proper XML parsing
xml_string = """
<function name="aggregate">
    <parameters>
        <param name="list" type="i32[]"/>
    </parameters>
    <variables>
        <var name="len" expression="len(list)"/>
        <var name="ret" type="i32[]" size="((len &gt;&gt; 1) + (len &amp; 0b1))" defaultValue="0"/>
    </variables>
    <logic>
        <for from="0" to="len(list)">
            <if condition="i % 2 == 1">
                <assignment>
                    <target>ret[i // 2]</target>
                    <value>ret[i // 2] + list[i]</value>
                </assignment>
            </if>
            <else>
                <assignment>
                    <target>ret[i // 2]</target>
                    <value>list[i]</value>
                </assignment>
            </else>
        </for>
    </logic>
    <return>ret</return>
</function>
"""

def parse_xml(xml_string):
    root = ET.fromstring(xml_string)
    logic = root.find('logic')
    return logic, root.find('return').text

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

def aggregate_from_xml(list):
    logic_element, return_statement = parse_xml(xml_string)
    code_lines = generate_code_from_logic(logic_element)
    code = "\n".join(code_lines)
    code += f"\nreturn {return_statement}"
    
    print("Generated Python Code:\n", code)
    
    local_vars = {'list': list, 'len': len, 'ret': [0] * ((len(list) >> 1) + (len(list) & 0b1)), 'i': None}
    exec(code, {}, local_vars)
    
    return local_vars['ret']

def test_aggregate():
    print("Running....")
    assert aggregate_from_xml([1, 2, 3, 4]) == [3, 7]
    assert aggregate_from_xml([10, 20, 30, 40, 50]) == [30, 70, 50]
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

