// use std::{
//     process::ExitCode,
//     ptr::{addr_of_mut, null_mut},
//     // sync::atomic::{AtomicI32, Ordering},
// };

// Convert infix regexp re to postfix notation.
// Insert . as explicit concatenation operator.
// Returns `None` for invalid patterns.
fn re2post(re: &[u8]) -> Option<Vec<u8> > {
    // struct Paren {
    //     nalt: i32,
    //     natom: i32,
    // }

    // Unlike the original program, we reject the
    // empty pattern as invalid. This avoids an
    // error case in post2nfa.
    // if re.is_empty() {
    //     return None;
    // }
    // if re.len() >= (8000 / 2) {
    //     return None;
    // }
    // let (mut nalt, mut natom) = (0, 0);
    // let mut paren = vec![];
    // let mut dst = vec![];
    for &byte in re.iter() {
        let pat = re[&byte];
        match pat {
            b'(' => {
                // if natom > 1 {
                //     natom -= 1;
                //     dst.push( b'.' );
                // }
                // if paren.len() >= 100 {
                //     return None;
                // }
                // paren.push(Paren { nalt, natom });
                // nalt = 0;
                // natom = 0;
            }
            // b'|' => {
            //     if natom == 0 {
            //         return None;
            //     }
            //     natom -= 1;
            //     while natom > 0 {
            //         dst.push(b'.');
            //         natom -= 1;
            //     }
            //     nalt += 1;
            // }
            // b')' => {
            //     let p = paren.pop()?;
            //     if natom == 0 {
            //         return None;
            //     }
            //     natom -= 1;
            //     while natom > 0 {
            //         dst.push(b'.');
            //         natom -= 1;
            //     }
            //     while nalt > 0 {
            //         dst.push(b'|');
            //         nalt -= 1;
            //     }
            //     nalt = p.nalt;
            //     natom = p.natom;
            //     natom += 1;
            // }
            // b'*' | b'+' | b'?' => {
            //     if natom == 0 {
            //         return None;
            //     }
            //     dst.push(byte);
            // }
            // Not handled in the original program.
            // Since '.' is a meta character in the
            // postfix syntax, it can result in UB.
            // So we reject it here.
            // _ => {
                // if natom > 1 {
                //     natom -= 1;
                //     dst.push(b'.');
                // }
                // dst.push(byte);
                // natom += 1;
            // }
        }
    }
    // if !paren.is_empty() {
    //     return None;
    // }
    // // The original program doesn't handle this case, which in turn
    // // causes UB in post2nfa. It occurs when a pattern ends with a |.
    // // Other cases like `a||b` and `(a|)` are rejected correctly above.
    // if natom == 0 && nalt > 0 {
    //     return None;
    // }
    // natom -= 1;
    // while natom > 0 {
    //     dst.push(b'.');
    //     natom -= 1;
    // }
    // while nalt > 0 {
    //     dst.push(b'|');
    //     nalt -= 1;
    // }
    // Some(dst);
}

fn main() {
    let pattern = "a(b|c)*d";
    let input = pattern.as_bytes();
    re2post(input);
    // match re2post(pattern.as_bytes()) {
    //     Some(postfix) => {
    //         println!("Postfix: {}", String::from_utf8(postfix).unwrap());
    //     }
    //     None => {
    //         println!("Invalid pattern");
    //     }
    // }
}