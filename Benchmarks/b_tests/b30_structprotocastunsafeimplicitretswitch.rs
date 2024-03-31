#![allow(dead_code, mutable_transmutes, non_camel_case_types, non_snake_case, non_upper_case_globals, unused_assignments, unused_mut)]
extern "C" {
    fn malloc(_: libc::c_ulong) -> *mut libc::c_void;
}
#[derive(Copy, Clone)]
#[repr(C)]
pub struct np {
    pub x: libc::c_int,
    pub y: libc::c_int,
}
#[derive(Copy, Clone)]
#[repr(C)]
pub struct r {
    pub data: libc::c_int,
    pub next: *mut r,
}
#[no_mangle]
pub unsafe extern "C" fn foo() -> *mut np {
    let mut x: *mut r = 0 as *mut r;
    let mut y: *mut r = 0 as *mut r;
    (*x).data = 2 as libc::c_int;
    (*y).data = 1 as libc::c_int;
    (*x).next = &mut y as *mut *mut r as *mut r;
    (*y).next = &mut x as *mut *mut r as *mut r;
    let mut z: *mut np = sus(x, y) as *mut r as *mut np;
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn bar() -> *mut r {
    let mut x: *mut r = 0 as *mut r;
    let mut y: *mut r = 0 as *mut r;
    (*x).data = 2 as libc::c_int;
    (*y).data = 1 as libc::c_int;
    (*x).next = &mut y as *mut *mut r as *mut r;
    (*y).next = &mut x as *mut *mut r as *mut r;
    let mut z: *mut r = sus(x, y) as *mut r;
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn sus(mut x: *mut r, mut y: *mut r) -> *mut np {
    (*x).next = ((*x).next).offset(1 as libc::c_int as isize);
    let mut z: *mut np = malloc(::core::mem::size_of::<np>() as libc::c_ulong)
        as *mut np;
    (*z).x = 1 as libc::c_int;
    (*z).y = 0 as libc::c_int;
    return z;
}
