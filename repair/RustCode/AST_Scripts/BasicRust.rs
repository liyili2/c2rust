fn main() {
    let some_number = 7;
    let add_number = some_number + 3;
}


// <STMT type = Block>
//     <STMT type = Let>  
//         <ID> some_number </ID>
//         <VEXP> 7 </VEXP> 
//     </STMT>
//     <STMT type = Let>
//         add_number 
//         <VEXP OP = Plus>
//              <ID> some_number </ID>
//              <VEXP> 3 </VEXP>
//         </VEXP>
//     </STMT>
// </STMT>

// Also, try and learn pytest and use it to test the xmlprinter
// for pytest, I need to set a config file first, then set some other initial cases (look at qgen)
// also, for some simple testing on xmlprinter, look at test_simulator
// simulator is just an interpreter
// In the simulator, for each expression, I need to define their behavior for each of the cases in the XMLprinter.
// I'm doing the same pattern as what I did in the XML printer, but instead of printing things out, I now define their
// behavior and I have an st that stores the data
// (don't need env)
// next step: learn pytest for testing xmlprinter, and write some stuff for the simulator