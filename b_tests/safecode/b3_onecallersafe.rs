extern crate libc;

use libc::{c_int, c_void, c_ulong};
use std::boxed::Box;

extern "C" {
    fn malloc(size: c_ulong) -> *mut c_void;
}

fn sus(x: &mut c_int, y: &mut c_int) -> Box<c_int> {
    let mut z = Box::new(1); // Allocate and initialize using Box
    *x = 2; // Safely modify 
    z // Return the Box<i32> 
}

fn foo() -> Box<c_int> {
    let mut sx: c_int = 3;
    let mut sy: c_int = 4;
    let mut z = sus(&mut sx, &mut sy);
    *z += 1; // value inside the Box<i32>
    z
}

fn bar() -> Box<c_int> {
    let mut sx: c_int = 3;
    let mut sy: c_int = 4;
    let mut z = sus(&mut sx, &mut sy);
    *z = -17; // Set the value in the Box<i32> to -17
    z
}

fn main() {
    let foo_result = foo();
    println!("Result from foo: {}", *foo_result);

    let bar_result = bar();
    println!("Result from bar: {}", *bar_result);
}
