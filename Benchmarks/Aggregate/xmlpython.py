import xml.etree.ElementTree as ET

def parse_variable(var):
    name = var.get('name')
    if 'expression' in var.attrib:
        expression = var.get('expression')
        return f"{name} = {expression}"
    elif 'type' in var.attrib and 'size' in var.attrib:
        size = var.get('size')
        default_value = var.get('defaultValue', '0')
        return f"{name} = [{default_value}] * {size}"
    return ""

def parse_assignment(assignment):
    target = assignment.find('target').text
    value = assignment.find('value').text
    return f"{target} = {value}"

def parse_if(if_element):
    condition = if_element.get('condition')
    assignments = [parse_assignment(a) for a in if_element.findall('assignment')]
    return f"if {condition}:\n    " + "\n    ".join(assignments)

def parse_else(else_element):
    assignments = [parse_assignment(a) for a in else_element.findall('assignment')]
    return "else:\n    " + "\n    ".join(assignments)

def parse_for(for_element):
    start = for_element.get('from')
    end = for_element.get('to')
    for_loop = f"for i in range({start}, {end}):"
    logic = []
    if if_element := for_element.find('if'):
        logic.append(parse_if(if_element))
    if else_element := for_element.find('else'):
        logic.append(parse_else(else_element))
    return f"{for_loop}\n    " + "\n    ".join(logic)

def convert_xml_to_python(xml_str):
    root = ET.fromstring(xml_str)
    
    # Start with function definition
    function_name = root.get('name')
    parameters = root.find('parameters')
    params = ", ".join([param.get('name') for param in parameters.findall('param')])
    
    python_code = [f"def {function_name}({params}):"]
    
    # Parse variables
    variables = root.find('variables')
    for var in variables.findall('var'):
        python_code.append("    " + parse_variable(var))
    
    # Parse logic
    logic = root.find('logic')
    for_loop = logic.find('for')
    python_code.append("    " + parse_for(for_loop))
    
    # Parse return
    return_value = root.find('return').text
    python_code.append(f"    return {return_value}")
    
    return "\n".join(python_code)

# Modified XML string with replaced entities
xml_data = '''
<function name="aggregate">
    <parameters>
        <param name="list" type="i32[]"/>
    </parameters>
    <variables>
        <var name="len" expression="len(list)"/>
        <var name="ret" type="i32[]" size="((len >> 1) + (len & 0b1))" defaultValue="0"/>
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
'''

# Convert XML to Python
python_code = convert_xml_to_python(xml_data)
print(python_code)

