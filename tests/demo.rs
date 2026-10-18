unsafe fn demo(mut a: i32, b: i32) -> i32 {
    let c = a * b;
    if a > b {
        a = c - b;
    }
    return c + b;
}