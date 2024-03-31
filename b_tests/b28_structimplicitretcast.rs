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
pub unsafe extern "C" fn sus(mut x: r, mut y: r) -> *mut r {
    x.next = (x.next).offset(1 as libc::c_int as isize);
    let mut z: *mut r = malloc(::core::mem::size_of::<r>() as libc::c_ulong) as *mut r;
    (*z).data = 1 as libc::c_int;
    (*z).next = 0 as *mut r;
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn foo() -> *mut r {
    let mut x: r = r { data: 0, next: 0 as *mut r };
    let mut y: r = r { data: 0, next: 0 as *mut r };
    x.data = 2 as libc::c_int;
    y.data = 1 as libc::c_int;
    x.next = &mut y;
    y.next = &mut x;
    let mut z: *mut r = sus(x, y);
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn bar() -> *mut np {
    let mut x: r = r { data: 0, next: 0 as *mut r };
    let mut y: r = r { data: 0, next: 0 as *mut r };
    x.data = 2 as libc::c_int;
    y.data = 1 as libc::c_int;
    x.next = &mut y;
    y.next = &mut x;
    let mut z: *mut r = sus(x, y);
    return 0 as *mut np;
}
