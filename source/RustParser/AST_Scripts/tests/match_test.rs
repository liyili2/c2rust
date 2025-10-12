fn main() {
    let mut a = 10;
    let q = 20;
    if 10 == q {
        a = 12;
    }
    match a {
        1 => {
        }
        2 => {
        }
        10 => {
         a = 1000;
        }
        _ => {
        }
    }
}