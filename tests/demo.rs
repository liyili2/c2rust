unsafe fn demo(mut a: i32, b: i32) -> i32 {
    if a > b {
        a = a - b;
    }
    return a + b;
}