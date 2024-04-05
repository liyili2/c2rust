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
pub unsafe extern "C" fn sus(mut x: p) -> p {
    let mut n: *mut p = malloc(::core::mem::size_of::<p>() as libc::c_ulong) as *mut p;
    return *n;
}
#[no_mangle]
pub unsafe extern "C" fn foo() -> p {
    let mut x: p = p {
        x: 0 as *mut libc::c_int,
        y: 0 as *mut libc::c_char,
    };
    let mut z: p = sus(x);
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn bar() -> p {
    let mut x: p = p {
        x: 0 as *mut libc::c_int,
        y: 0 as *mut libc::c_char,
    };
    let mut z: p = sus(x);
    z.x = (z.x).offset(1 as libc::c_int as isize);
    return z;
}
