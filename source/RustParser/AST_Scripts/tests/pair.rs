#[derive(Debug)]
struct Pair {
    x: i32,
    y: i32,
}

fn main() {
    let mut p = Pair { x: 10, y: 20 };
    let x_ptr: *mut i32 = & mut p.x;
    let y_ptr: *mut i32 = & mut p.y;

    unsafe {
        *x_ptr += 5;
        *y_ptr *= 2;

        println!("x via pointer: {}", *x_ptr);
        println!("y via pointer: {}", *y_ptr);
    }

    println!("Updated struct: {:?}", p);
}
