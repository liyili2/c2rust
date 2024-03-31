#![allow(dead_code, mutable_transmutes, non_camel_case_types, non_snake_case, non_upper_case_globals, unused_assignments, unused_mut)]
extern "C" {
    fn malloc(_: libc::c_ulong) -> *mut libc::c_void;
}
#[no_mangle]
pub unsafe extern "C" fn sus(
    mut x: *mut libc::c_int,
    mut y: *mut libc::c_int,
) -> *mut libc::c_int {
    let mut z: *mut libc::c_int = malloc(
        ::core::mem::size_of::<libc::c_int>() as libc::c_ulong,
    ) as *mut libc::c_int;
    *z = 1 as libc::c_int;
    x = x.offset(1);
    x;
    *x = 2 as libc::c_int;
    z = z.offset(1);
    z;
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn foo() -> *mut libc::c_int {
    let mut sx: libc::c_int = 3 as libc::c_int;
    let mut sy: libc::c_int = 4 as libc::c_int;
    let mut x: *mut libc::c_int = &mut sx;
    let mut y: *mut libc::c_int = &mut sy;
    let mut z: *mut libc::c_int = sus(x, y);
    *z = *z + 1 as libc::c_int;
    return z;
}
#[no_mangle]
pub unsafe extern "C" fn bar() -> *mut libc::c_int {
    let mut sx: libc::c_int = 3 as libc::c_int;
    let mut sy: libc::c_int = 4 as libc::c_int;
    let mut x: *mut libc::c_int = &mut sx;
    let mut y: *mut libc::c_int = &mut sy;
    let mut z: *mut libc::c_int = sus(x, y);
    return z;
}
