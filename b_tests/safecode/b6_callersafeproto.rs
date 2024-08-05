fn sus(x: &mut [i32], y: &mut i32) -> Box<i32> {
    // Allocate memory for a single i32 on the heap and initialize it
    let mut z = Box::new(1);

    // Ensure the slice has at least two elements to safely access x[1]
    if x.len() > 1 {
        x[1] = 2; // Safely set the second element of the slice
    } else {
        panic!("The slice does not have enough elements");
    }

    z // Return the Box containing the allocated integer
}

fn foo() -> Box<i32> {
    let mut sx = 3;
    let mut sy = 4;
    let mut data = vec![sx, sy];
    let mut z = sus(&mut data, &mut sy);
    *z += 1; // Increment the value inside the Box
    z
}

fn bar() -> Box<i32> {
    let mut sx = 3;
    let mut sy = 4;
    let mut data = vec![sx, sy];
    let mut z = sus(&mut data, &mut sy);

    // Add two more elements to simulate z.offset(2)
    let mut offset_data = vec![*z, 0, 0];
    let mut z = Box::new(offset_data[2]);
    *z = -17;

    z
}

fn main() {
    let foo_result = foo();
    println!("Result from foo: {}", *foo_result);

    let bar_result = bar();
    println!("Result from bar: {}", *bar_result);
}
