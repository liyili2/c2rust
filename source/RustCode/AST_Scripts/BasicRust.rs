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