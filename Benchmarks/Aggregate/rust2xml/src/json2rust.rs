use serde::{Deserialize};
use std::fs;
use std::error::Error;

// Struct to represent a parsed struct
#[derive(Deserialize, Debug)]
struct SerializableStruct {
    name: Vec<String>,    
    fields: Vec<SerializableField>,  // Adjusted to handle fields with types
}

// Struct to represent a field with its type
#[derive(Deserialize, Debug)]
struct SerializableField {
    name: Vec<String>,
    r#type: Vec<String>,
}

// Struct to represent method parameters
#[derive(Deserialize, Debug)]
struct SerializableParameter {
    name: Vec<String>,    
    r#type: Vec<String>,  
}

// Struct to represent methods in an impl block, including their bodies
#[derive(Deserialize, Debug)]
struct SerializableMethod {
    method_name: Vec<String>,  
    parameters: Vec<SerializableParameter>,
    return_type: Vec<String>,  
    body: Vec<Statement>,
}

// Struct to represent impl blocks, which include methods and their logic
#[derive(Deserialize, Debug)]
struct SerializableImpl {
    struct_name: Vec<String>,  
    methods: Vec<SerializableMethod>,
}

// Struct to represent a function (like `main`)
#[derive(Deserialize, Debug)]
struct SerializableFunction {
    functionname: Vec<String>,  
    parameters: Option<Vec<SerializableParameter>>,  
    return_type: Vec<String>,  
    body: Vec<Statement>,
}

// Enum to categorize different types of statements in a function or method body
#[derive(Deserialize, Debug)]
#[serde(tag = "type")]  
enum Statement {
    VariableAssignment { content: Vec<String> },
    Expression { content: Vec<String> },
    Other { content: Vec<String> },  
}

fn generate_rust_code_from_json(json_content: &str) -> Result<String, Box<dyn Error>> {
    let parsed_data: serde_json::Value = serde_json::from_str(json_content)?;

    let mut rust_code = String::new();

    // Extract structs
    if let Some(structs) = parsed_data.get("root").and_then(|root| root.get("structs")) {
        for s in structs.as_array().unwrap() {
            let struct_name = s.get("name").unwrap().as_array().unwrap()[0].as_str().unwrap();
            let fields = s.get("fields").unwrap().as_array().unwrap();

            rust_code.push_str(&format!("#[derive(Debug)]\nstruct {} {{\n", struct_name));

            for field in fields {
                let field_name = field.get("name").unwrap().as_array().unwrap()[0].as_str().unwrap();
                let field_type = field.get("type").unwrap().as_array().unwrap()[0].as_str().unwrap();
                rust_code.push_str(&format!("    {}: {},\n", field_name, field_type));
            }

            rust_code.push_str("}\n\n");
        }
    }

    // Extract impl blocks
    if let Some(impl_blocks) = parsed_data.get("root").and_then(|root| root.get("impl_blocks")) {
        for imp in impl_blocks.as_array().unwrap() {
            let struct_name = imp.get("struct_name").unwrap().as_array().unwrap()[0].as_str().unwrap();
            let methods = imp.get("methods").unwrap().as_array().unwrap();

            rust_code.push_str(&format!("impl {} {{\n", struct_name));

            for method in methods {
                let method_name = method.get("method_name").unwrap().as_array().unwrap()[0].as_str().unwrap();
                
                // Fixing the temporary value issue: bind an empty vec to a variable
                let empty_vec = vec![];
                let parameters = method.get("parameters").and_then(|p| p.as_array()).unwrap_or(&empty_vec);
                let return_type_value = method.get("return_type").unwrap();
                let return_type = if let Some(ret_type) = return_type_value.as_array() {
                    ret_type.get(0).unwrap().as_str().unwrap()
                } else {
                    ""
                };
                let body = method.get("body").unwrap().as_array().unwrap();

                let param_str: Vec<String> = parameters.iter().map(|param| {
                    let name = param.get("name").unwrap().as_array().unwrap()[0].as_str().unwrap();
                    let r#type = param.get("type").unwrap().as_array().unwrap()[0].as_str().unwrap();
                    
                    // Handle "self", "&self", and "&mut self" cases
                    if name.is_empty() && (r#type == "&mut self" || r#type == "&self") {
                        format!("{}", r#type)
                    } else {
                        format!("{}: {}", name, r#type)
                    }
                }).collect();

                if return_type.is_empty() {
                    rust_code.push_str(&format!("    fn {}({}) {{\n", method_name, param_str.join(", ")));
                } else {
                    rust_code.push_str(&format!("    fn {}({}) -> {} {{\n", method_name, param_str.join(", "), return_type));
                }

                for (index, statement) in body.iter().enumerate() {
                    if let Some(content) = statement.get("content") {
                        let is_last = index == body.len() - 1;
                        let content_str = content.as_array().unwrap()[0].as_str().unwrap();
                        
                        if is_last && !return_type.is_empty() {
                            rust_code.push_str(&format!("        {}\n", content_str));
                        } else {
                            rust_code.push_str(&format!("        {};\n", content_str));
                        }
                    }
                }

                rust_code.push_str("    }\n");
            }

            rust_code.push_str("}\n\n");
        }
    }

    // Extract functions (like `main`)
    if let Some(functions) = parsed_data.get("root").and_then(|root| root.get("functions")) {
        for func in functions.as_array().unwrap() {
            let function_name = func.get("functionname").unwrap().as_array().unwrap()[0].as_str().unwrap();
            let return_type_value = func.get("return_type").unwrap();
            let return_type = if let Some(ret_type) = return_type_value.as_array() {
                ret_type.get(0).unwrap().as_str().unwrap()
            } else {
                ""
            };

            // Fixing the temporary value issue here too
            let empty_vec = vec![];
            let parameters = func.get("parameters").and_then(|p| p.as_array()).unwrap_or(&empty_vec);
            let param_str: Vec<String> = parameters.iter().map(|param| {
                let name = param.get("name").unwrap().as_array().unwrap()[0].as_str().unwrap();
                let r#type = param.get("type").unwrap().as_array().unwrap()[0].as_str().unwrap();
                format!("{}: {}", name, r#type)
            }).collect();

            if return_type.is_empty() {
                rust_code.push_str(&format!("fn {}({}) {{\n", function_name, param_str.join(", ")));
            } else {
                rust_code.push_str(&format!("fn {}({}) -> {} {{\n", function_name, param_str.join(", "), return_type));
            }

            let body = func.get("body").unwrap().as_array().unwrap();
            for (index, statement) in body.iter().enumerate() {
                if let Some(content) = statement.get("content") {
                    let is_last = index == body.len() - 1;
                    let content_str = content.as_array().unwrap()[0].as_str().unwrap();
                    
                    if is_last && !return_type.is_empty() {
                        rust_code.push_str(&format!("    {}\n", content_str));
                    } else {
                        rust_code.push_str(&format!("    {};\n", content_str));
                    }
                }
            }

            rust_code.push_str("}\n\n");
        }
    }

    Ok(rust_code)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let input_json_file = "output_b.json";  
    let output_rust_file = "output_b.rs";  

    let json_content = fs::read_to_string(input_json_file)?;

    let rust_code = generate_rust_code_from_json(&json_content)?;

    fs::write(output_rust_file, rust_code)?;

    println!("Generated Rust code saved to {}", output_rust_file);

    Ok(())
}
