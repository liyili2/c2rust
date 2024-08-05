

fn sus(x: &mut i32, y: &mut i32) -> Box<i32> {
    let  z = Box::new(1); // Allocate and initialize  using Box
    *x = 2; // Safely modify 
    z // Return the Box<i32> 
}

fn foo() -> Box<i32> {
    let mut sx: i32 = 3;
    let mut sy: i32 = 4;
    let mut z = sus(&mut sx, &mut sy);
    *z += 1; // value inside the Box<i32>
    z
}

fn bar() -> Box<i32> {
    let mut sx: i32 = 3;
    let mut sy: i32 = 4;
    let z = sus(&mut sx, &mut sy);
    z
}

fn main() {
    let foo_result = foo();
    println!("Result from foo: {}", *foo_result);

    let bar_result = bar();
    println!("Result from bar: {}", *bar_result);
}
