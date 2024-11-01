use serde::{Serialize, Deserialize};
use std::fs;
use syn::{File, Item, Stmt, FnArg, PatType, Type};
use xml2json_rs::XmlBuilder;

// Struct to represent a parsed struct field with type
#[derive(Serialize, Deserialize, Debug)]
struct SerializableField {
    name: String,
    r#type: String,
}

// Struct to represent a parsed struct
#[derive(Serialize, Deserialize, Debug)]
struct SerializableStruct {
    name: String,
    fields: Vec<SerializableField>,
}

// Struct to represent method parameters
#[derive(Serialize, Deserialize, Debug)]
struct SerializableParameter {
    name: String,
    r#type: String, // using r#type since type is a reserved keyword in Rust
}

// Struct to represent methods in an impl block, including their bodies
#[derive(Serialize, Deserialize, Debug)]
struct SerializableMethod {
    visibility: String, 
    method_name: String,
    parameters: Vec<SerializableParameter>,
    return_type: String,
    body: Vec<Statement>,
}

// Struct to represent impl blocks, which include methods and their logic
#[derive(Serialize, Deserialize, Debug)]
struct SerializableImpl {
    struct_name: String,
    methods: Vec<SerializableMethod>,
}

// Struct to represent a function (like `main`)
#[derive(Serialize, Deserialize, Debug)]
struct SerializableFunction {
    visibility: String, 
    functionname: String,
    parameters: Vec<SerializableParameter>,
    return_type: String,
    body: Vec<Statement>,
}

// Enum to categorize different types of statements in a function or method body
#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "type", content = "content")]
enum Statement {
    VariableAssignment(String),
    Expression(String),
    Other(String),
}

// Updated function to extract full type information, including generics and references
// Updated function to extract full type information, including generics and references
fn extract_type(ty: &Type) -> String {
    match ty {
        // Handle Path types (e.g., Vec<T>, i32)
        Type::Path(type_path) => {
            let segments: Vec<String> = type_path.path.segments.iter()
                .map(|seg| {
                    let args_str = match &seg.arguments {
                        syn::PathArguments::AngleBracketed(angle_bracketed) => {
                            let arg_types: Vec<String> = angle_bracketed.args.iter()
                                .filter_map(|arg| match arg {
                                    syn::GenericArgument::Type(ty) => Some(extract_type(ty)),
                                    _ => None,
                                })
                                .collect();
                            if !arg_types.is_empty() {
                                format!("<{}>", arg_types.join(", "))
                            } else {
                                String::new()
                            }
                        }
                        _ => String::new(),
                    };
                    format!("{}{}", seg.ident, args_str)
                })
                .collect();
            segments.join("::")
        }
        // Handle Reference types (e.g., &mut [T], &T)
        Type::Reference(type_reference) => {
            let mutability = if type_reference.mutability.is_some() { "mut " } else { "" };
            let elem_type = extract_type(&type_reference.elem);
            format!("&{}{}", mutability, elem_type)
        }
        // Handle slices (e.g., &[T])
        Type::Slice(slice) => {
            let elem_type = extract_type(&slice.elem);
            format!("[{}]", elem_type)
        }
        _ => "Unknown".to_string(),
    }
}

// Function to parse struct definitions including field types
fn parse_struct(item: &Item) -> Option<SerializableStruct> {
    if let Item::Struct(item_struct) = item {
        let struct_name = item_struct.ident.to_string();
        let fields: Vec<SerializableField> = match &item_struct.fields {
            syn::Fields::Named(fields_named) => fields_named.named.iter()
                .map(|field| {
                    let field_name = field.ident.as_ref().unwrap().to_string();
                    let field_type = extract_type(&field.ty);
                    SerializableField {
                        name: field_name,
                        r#type: field_type,
                    }
                })
                .collect(),
            _ => vec![],
        };
        Some(SerializableStruct {
            name: struct_name,
            fields,
        })
    } else {
        None
    }
}

// Function to classify and parse statements in the function or method body
fn classify_statement(stmt: &Stmt) -> Statement {
    match stmt {
        Stmt::Local(local) => {
            let stmt_str = quote::quote!(#local).to_string();
            Statement::VariableAssignment(stmt_str)
        }
        Stmt::Expr(expr) | Stmt::Semi(expr, _) => {
            let stmt_str = quote::quote!(#expr).to_string();
            Statement::Expression(stmt_str)
        }
        _ => {
            let stmt_str = quote::quote!(#stmt).to_string();
            Statement::Other(stmt_str)
        }
    }
}

// Function to extract parameters from a function signature, including `self`, `&self`, or `&mut self`
fn extract_parameters(inputs: &syn::punctuated::Punctuated<FnArg, syn::token::Comma>) -> Vec<SerializableParameter> {
    inputs.iter().filter_map(|arg| {
        match arg {
            // Check if the argument is a receiver like `&self` or `&mut self`
            FnArg::Receiver(receiver) => {
                let param_name = "".to_string();
                let param_type = if receiver.reference.is_some() {
                    if receiver.mutability.is_some() {
                        "&mut self".to_string()  // `&mut self`
                    } else {
                        "&self".to_string()  // `&self`
                    }
                } else {
                    "self".to_string()  // `self`
                };
                Some(SerializableParameter {
                    name: param_name,
                    r#type: param_type,
                })
            },
            // If the argument is a regular typed parameter
            FnArg::Typed(PatType { pat, ty, .. }) => {
                let param_name = quote::quote!(#pat).to_string();
                let param_type = extract_type(&ty);
                Some(SerializableParameter {
                    name: param_name,
                    r#type: param_type,
                })
            },
        }
    }).collect()
}

// Function to extract return type from a function signature
fn extract_return_type(output: &syn::ReturnType) -> String {
    match output {
        syn::ReturnType::Type(_, ty) => extract_type(&ty),
        syn::ReturnType::Default => "".to_string(),
    }
}

fn extract_visibility(visibility: &syn::Visibility) -> String {
    match visibility {
        syn::Visibility::Public(_) => "pub".to_string(),
        syn::Visibility::Crate(_) => "crate".to_string(),
        syn::Visibility::Restricted(_) => "restricted".to_string(),
        syn::Visibility::Inherited => "private".to_string(),
    }
}


// Function to parse methods inside an impl block, including the method body
fn parse_impl_block(item: &Item) -> Option<SerializableImpl> {
    if let Item::Impl(item_impl) = item {
        let struct_name = match &*item_impl.self_ty {
            syn::Type::Path(type_path) => type_path.path.segments.last()?.ident.to_string(),
            _ => return None,
        };

        let methods: Vec<SerializableMethod> = item_impl.items.iter().filter_map(|impl_item| {
            if let syn::ImplItem::Method(method) = impl_item {
                let body_statements: Vec<Statement> = method.block.stmts.iter()
                    .map(classify_statement)
                    .collect();
                let parameters = extract_parameters(&method.sig.inputs);
                let return_type = extract_return_type(&method.sig.output);
                let visibility = extract_visibility(&method.vis);

                Some(SerializableMethod {
                    visibility,
                    method_name: method.sig.ident.to_string(),
                    parameters,
                    return_type,
                    body: body_statements,
                })
            } else {
                None
            }
        }).collect();

        Some(SerializableImpl {
            struct_name,
            methods,
        })
    } else {
        None
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let input_file_path = "src/aggregate.rs"; 
    let output_json_file_path = "src/output.json";  
    let output_xml = "src/output.xml";

    let rust_code = fs::read_to_string(input_file_path)?;

    let syntax_tree: File = syn::parse_file(&rust_code)?;

    let mut structs = vec![];
    let mut impl_blocks = vec![];
    let mut functions = vec![];

    for item in syntax_tree.items.iter() {
        if let Some(parsed_struct) = parse_struct(item) {
            structs.push(parsed_struct);
        }

        if let Some(parsed_impl) = parse_impl_block(item) {
            impl_blocks.push(parsed_impl);
        }

        if let Item::Fn(func) = item {
            let body_statements: Vec<Statement> = func.block.stmts.iter()
                .map(classify_statement)
                .collect();
            let parameters = extract_parameters(&func.sig.inputs);
            let return_type = extract_return_type(&func.sig.output);
            let visibility = extract_visibility(&func.vis);

            functions.push(SerializableFunction {
                visibility,
                functionname: func.sig.ident.to_string(),
                parameters,
                return_type,
                body: body_statements,
            });
        }
    }

    // Prepare the full output containing structs, impl blocks, and functions
    let output = serde_json::json!({
        "structs": structs,
        "impl_blocks": impl_blocks,
        "functions": functions,
    });

    // Write the output to a JSON file
    let json_output = serde_json::to_string_pretty(&output)?;
    fs::write(output_json_file_path, &json_output)?;

    println!("Parsed code has been saved to {}", output_json_file_path);

    // Initialize the XML builder
    let mut xml_builder = XmlBuilder::default();

    // Convert the JSON content to XML directly from the variable
    let xml_content = xml_builder.build_from_json_string(&json_output)?;

    // Write the XML content to the output file
    fs::write(output_xml, xml_content)?;

    println!("Converted XML saved to {}", output_xml);

    Ok(())
}
