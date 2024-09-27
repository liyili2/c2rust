use xml2json_rs::JsonBuilder;
use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input_xml_file = "output.xml";  
    let output_json_file = "output_b.json";  
    
    // Read the XML file
    let xml_content = fs::read_to_string(input_xml_file)?;
    
    // Initialize JsonBuilder
    let json_builder = JsonBuilder::default();
    
    // Convert XML to JSON
    let json = json_builder.build_pretty_string_from_xml(&xml_content)?;
    
    // Save the JSON to a file
    fs::write(output_json_file, json.clone())?;
    
    println!("Converted JSON saved to {}", output_json_file);
    
    Ok(())
}
