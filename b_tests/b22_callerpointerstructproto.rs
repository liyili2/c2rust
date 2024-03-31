#![allow(dead_code, mutable_transmutes, non_camel_case_types, non_snake_case, non_upper_case_globals, unused_assignments, unused_mut)]
extern "C" {
    fn malloc(_: libc::c_ulong) -> *mut libc::c_void;
}
#[derive(Copy, Clone)]
#[repr(C)]
pub struct p {
    pub x: *mut libc::c_int,
    pub y: *mut libc::c_char,
}
#[no_mangle]
pub unsafe extern "C" fn foo() -> *mut p {
    let mut ex1: libc::c_int = 2 as libc::c_int;
    let mut ex2: libc::c_int = 3 as libc::c_int;
    let mut x: *mut p = 0 as *mut p;
    let mut y: *mut p = 0 as *mut p;
    (*x).x = &mut ex1;
    (*y).x = &mut ex2;
    (*x).y = &mut ex2 as *mut libc::c_int as *mut libc::c_char;
    (*y).y = &mut ex1 as *mut libc::c_int as *mut libc::c_char;
    let mut z: *mut p = sus(x, y);
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn bar() -> *mut p {
    let mut ex1: libc::c_int = 2 as libc::c_int;
    let mut ex2: libc::c_int = 3 as libc::c_int;
    let mut x: *mut p = 0 as *mut p;
    let mut y: *mut p = 0 as *mut p;
    (*x).x = &mut ex1;
    (*y).x = &mut ex2;
    (*x).y = &mut ex2 as *mut libc::c_int as *mut libc::c_char;
    (*y).y = &mut ex1 as *mut libc::c_int as *mut libc::c_char;
    let mut z: *mut p = sus(x, y);
    z = z.offset(2 as libc::c_int as isize);
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn sus(mut x: *mut p, mut y: *mut p) -> *mut p {
    (*x).y = ((*x).y).offset(1 as libc::c_int as isize);
    let mut z: *mut p = malloc(::core::mem::size_of::<p>() as libc::c_ulong) as *mut p;
    return z;
}
