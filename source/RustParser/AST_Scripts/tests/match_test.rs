fn main() {
    let mut a = 10;

    match a {
            11 => {

            }
            1 => {

            }
            10 => {
                a = 1000;
            }
            12 | 10 | 9 => {

            }
            // Not handled in the original program.
            // Since '.' is a meta character in the
            // postfix syntax, it can result in UB.
            // So we reject it here.
            _ => {

            }
}