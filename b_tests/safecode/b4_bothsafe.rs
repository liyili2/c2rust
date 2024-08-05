fn sus(x: &mut i32, y: &mut i32) -> Box<i32> {
    let mut z = Box::new(1); // Allocate on the heap and initialize with 1
    *x = 2; // Safely modify the value of x
    z // Return the Box containing the allocated integer
}

fn foo() -> Box<i32> {
    let mut sx: i32 = 3;
    let mut sy: i32 = 4;
    let mut z = sus(&mut sx, &mut sy);
    *z += 1; // Increment the value inside the Box
    z
}

fn bar() -> Box<i32> {
    let mut sx: i32 = 3;
    let mut sy: i32 = 4;
    let mut z = sus(&mut sx, &mut sy);
    // Use a Vec to simulate pointer arithmetic safely
    let mut vec = vec![*z, 0]; // Create a Vec with at least two elements
    vec.push(0); // Ensure there's a third element for safe access

    vec[2] = -17; // Set the third element to -17

    // Convert the Vec to a Box<[i32]> and return the third element
    let boxed_slice = vec.into_boxed_slice();
    Box::new(boxed_slice[2])
}

fn main() {
    let foo_result = foo();
    println!("Result from foo: {}", *foo_result);

    let bar_result = bar();
    println!("Result from bar: {}", *bar_result);
}
