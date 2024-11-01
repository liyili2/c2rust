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
    visibility: Vec<String>,
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
    visibility: Vec<String>,
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

    // Updated helper function to process statements recursively with conditional/loop handling
    fn process_statements(statements: &Vec<serde_json::Value>, rust_code: &mut String, indent: usize) {
        let indentation = " ".repeat(indent);
        for statement in statements {
            if let Some(content) = statement.get("content") {
                let content_str = content.as_array().unwrap()[0].as_str().unwrap();
                rust_code.push_str(&format!("{}{};\n", indentation, content_str));
            }
            
            // Check for nested `body` within `statement` for loops and conditionals
            if let Some(nested_body) = statement.get("body") {
                rust_code.push_str(&format!("{}{{\n", indentation));  // Start nested block
                process_statements(nested_body.as_array().unwrap(), rust_code, indent + 4);  // Recursive call for nested statements
                rust_code.push_str(&format!("{}}}\n", indentation));  // End nested block
            }
        }
    }

    // Process functions (like `aggregate`, `printall`, `main`)
    if let Some(functions) = parsed_data.get("root").and_then(|root| root.get("functions")) {
        for func in functions.as_array().unwrap() {
            // Extract visibility
            let visibility = func.get("visibility").unwrap().as_array().unwrap()[0].as_str().unwrap();
            
            let function_name = func.get("functionname").unwrap().as_array().unwrap()[0].as_str().unwrap();
            let return_type_value = func.get("return_type").unwrap();
            let return_type = if let Some(ret_type) = return_type_value.as_array() {
                ret_type.get(0).unwrap().as_str().unwrap()
            } else {
                ""
            };

            let empty_vec = vec![];
            let parameters = func.get("parameters").and_then(|p| p.as_array()).unwrap_or(&empty_vec);
            let param_str: Vec<String> = parameters.iter().map(|param| {
                let name = param.get("name").unwrap().as_array().unwrap()[0].as_str().unwrap();
                let r#type = param.get("type").unwrap().as_array().unwrap()[0].as_str().unwrap();
                format!("{}: {}", name, r#type)
            }).collect();

            // Insert visibility (e.g., "pub") if available, otherwise default to private (no keyword)
            let visibility_str = if visibility == "pub" { "pub " } else { "" };

            if return_type.is_empty() {
                rust_code.push_str(&format!("{}fn {}({}) {{\n", visibility_str, function_name, param_str.join(", ")));
            } else {
                rust_code.push_str(&format!("{}fn {}({}) -> {} {{\n", visibility_str, function_name, param_str.join(", "), return_type));
            }

            let body = func.get("body").unwrap().as_array().unwrap();
            process_statements(body, &mut rust_code, 4);  // Process body with indentation

            rust_code.push_str("}\n\n");
        }
    }

    Ok(rust_code)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let input_json_file = "src/output_b.json";  
    let output_rust_file = "src/output_b.rs";  

    let json_content = fs::read_to_string(input_json_file)?;

    let rust_code = generate_rust_code_from_json(&json_content)?;

    fs::write(output_rust_file, rust_code)?;

    println!("Generated Rust code saved to {}", output_rust_file);

    Ok(())
}
