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
pub struct p {
    pub x: *mut libc::c_int,
    pub y: *mut libc::c_char,
}
#[no_mangle]
pub unsafe extern "C" fn sus(mut x: p, mut y: p) -> *mut np {
    let mut z: *mut np = malloc(::core::mem::size_of::<np>() as libc::c_ulong)
        as *mut np;
    (*z).x = 1 as libc::c_int;
    (*z).x = 2 as libc::c_int;
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn foo() -> *mut np {
    let mut x: p = p {
        x: 0 as *mut libc::c_int,
        y: 0 as *mut libc::c_char,
    };
    let mut y: p = p {
        x: 0 as *mut libc::c_int,
        y: 0 as *mut libc::c_char,
    };
    x.x = 1 as libc::c_int as *mut libc::c_int;
    x.y = 2 as libc::c_int as *mut libc::c_char;
    y.x = 3 as libc::c_int as *mut libc::c_int;
    y.y = 4 as libc::c_int as *mut libc::c_char;
    let mut z: *mut np = sus(x, y);
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn bar() -> *mut np {
    let mut x: p = p {
        x: 0 as *mut libc::c_int,
        y: 0 as *mut libc::c_char,
    };
    let mut y: p = p {
        x: 0 as *mut libc::c_int,
        y: 0 as *mut libc::c_char,
    };
    x.x = 1 as libc::c_int as *mut libc::c_int;
    x.y = 2 as libc::c_int as *mut libc::c_char;
    y.x = 3 as libc::c_int as *mut libc::c_int;
    y.y = 4 as libc::c_int as *mut libc::c_char;
    let mut z: *mut np = sus(x, y);
    return z;
}
