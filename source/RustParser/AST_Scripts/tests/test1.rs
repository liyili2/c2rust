// #![allow(dead_code, mutable_transmutes, non_camel_case_types, non_snake_case, non_upper_case_globals, unused_assignments, unused_mut)]
// #![feature(extern_types)]
// extern "C" {
//     pub type _IO_wide_data;
//     pub type _IO_codecvt;
//     pub type _IO_marker;
//     static mut stderr: *mut FILE;
//     fn fprintf(_: *mut FILE, _: *const libc::c_char, _: ...) -> libc::c_int;
//     fn printf(_: *const libc::c_char, _: ...) -> libc::c_int;
//     fn malloc(_: libc::c_ulong) -> *mut libc::c_void;
//     fn strlen(_: *const libc::c_char) -> libc::c_ulong;
// }
// pub type size_t = libc::c_ulong;
// pub type __off_t = libc::c_long;
// pub type __off64_t = libc::c_long;
// #[derive(Copy, Clone)]
// #[repr(C)]
// pub struct _IO_FILE {
//     pub _flags: libc::c_int,
//     pub _IO_read_ptr: *mut libc::c_char,
//     pub _IO_read_end: *mut libc::c_char,
//     pub _IO_read_base: *mut libc::c_char,
//     pub _IO_write_base: *mut libc::c_char,
//     pub _IO_write_ptr: *mut libc::c_char,
//     pub _IO_write_end: *mut libc::c_char,
//     pub _IO_buf_base: *mut libc::c_char,
//     pub _IO_buf_end: *mut libc::c_char,
//     pub _IO_save_base: *mut libc::c_char,
//     pub _IO_backup_base: *mut libc::c_char,
//     pub _IO_save_end: *mut libc::c_char,
//     pub _markers: *mut _IO_marker,
//     pub _chain: *mut _IO_FILE,
//     pub _fileno: libc::c_int,
//     pub _flags2: libc::c_int,
//     pub _old_offset: __off_t,
//     pub _cur_column: libc::c_ushort,
//     pub _vtable_offset: libc::c_schar,
//     pub _shortbuf: [libc::c_char; 1],
//     pub _lock: *mut libc::c_void,
//     pub _offset: __off64_t,
//     pub _codecvt: *mut _IO_codecvt,
//     pub _wide_data: *mut _IO_wide_data,
//     pub _freeres_list: *mut _IO_FILE,
//     pub _freeres_buf: *mut libc::c_void,
//     pub __pad5: size_t,
//     pub _mode: libc::c_int,
//     pub _unused2: [libc::c_char; 20],
// }
// pub type _IO_lock_t = ();
// pub type FILE = _IO_FILE;
// #[derive(Copy, Clone)]
// #[repr(C)]
pub struct C2RustUnnamed {
    pub nalt: libc::c_int,
    pub natom: libc::c_int,
}
// pub type C2RustUnnamed_0 = libc::c_uint;
// pub const Split: C2RustUnnamed_0 = 257;
// pub const Match: C2RustUnnamed_0 = 256;
// #[derive(Copy, Clone)]
// #[repr(C)]
// pub struct State {
//     pub c: libc::c_int,
//     pub out: *mut State,
//     pub out1: *mut State,
//     pub lastlist: libc::c_int,
// }
// #[derive(Copy, Clone)]
// #[repr(C)]
// pub struct Frag {
//     pub start: *mut State,
//     pub out: *mut Ptrlist,
// }
// #[derive(Copy, Clone)]
// #[repr(C)]
// pub union Ptrlist {
//     pub next: *mut Ptrlist,
//     pub s: *mut State,
// }
// #[derive(Copy, Clone)]
// #[repr(C)]
// pub struct List {
//     pub s: *mut *mut State,
//     pub n: libc::c_int,
// }

// #[no_mangle]
// pub static mut matchstate: State = {
//     let mut init = State {
//         c: Match as libc::c_int,
//         out: 0 as *const State as *mut State,
//         out1: 0 as *const State as *mut State,
//         lastlist: 0,
//     };
//     init
// };
// #[no_mangle]
// pub static mut nstate: libc::c_int = 0;

// #[no_mangle]
pub unsafe extern "C" fn re2post(mut re: *mut libc::c_char) -> *mut libc::c_char {
    // let mut nalt: libc::c_int = 0;
    // let mut natom: libc::c_int = 0;
    // static mut buf: [libc::c_char; 8000] = [0; 8000];
    // let mut dst: *mut libc::c_char = 0 as *mut libc::c_char;
    // let mut paren: [C2RustUnnamed; 100] = [C2RustUnnamed { nalt: 0, natom: 0 }; 100];
    // let mut p: *mut C2RustUnnamed = 0 as *mut C2RustUnnamed;
    // p = paren.as_mut_ptr();
    // dst = buf.as_mut_ptr();
    // nalt = 0 as libc::c_int;
    // natom = 0 as libc::c_int;
    // if strlen(re) >= (::core::mem::size_of::[libc::c_char; 8000] () as libc::c_ulong).wrapping_div(2 as libc::c_int as libc::c_ulong)
    // {
    //     return 0 as *mut libc::c_char;
    // }
    while (*re) != 0 {
        // match *re as libc::c_int {
        //     40 => {
        //         if natom > 1 as libc::c_int {
        //             natom -= 1;
        //             natom;
        //             let fresh0 = dst;
        //             dst = dst.offset(1);
        //             *fresh0 = '.' as i32 as libc::c_char ;
        //         }
        //         if p >= paren.as_mut_ptr().offset(100 as libc::c_int as isize) {
        //             return 0 as *mut libc::c_char;
        //         }
        //         (*p).nalt = nalt;
        //         (*p).natom = natom;
        //         p = p.offset(1);
        //         p;
        //         nalt = 0 as libc::c_int;
        //         natom = 0 as libc::c_int;
        //     }
        //     124 => {
        //         if natom == 0 as libc::c_int {
        //             return 0 as *mut libc::c_char;
        //         }
        //         loop {
        //             natom -= 1;
        //             if !(natom > 0 as libc::c_int) {
        //                 break;
        //             }
        //             let fresh1 = dst;
        //             dst = dst.offset(1);
        //             *fresh1 = '.' as i32 as libc::c_char;
        //         }
        //         nalt += 1;
        //         nalt;
        //     }
        //     41 => {
        //         if p == paren.as_mut_ptr() {
        //             return 0 as *mut libc::c_char;
        //         }
        //         if natom == 0 as libc::c_int {
        //             return 0 as *mut libc::c_char;
        //         }
        //         loop {
        //             natom -= 1;
        //             if !(natom > 0 as libc::c_int) {
        //                 break;
        //             }
        //             let fresh2 = dst;
        //             dst = dst.offset(1);
        //             *fresh2 = '.' as i32 as libc::c_char;
        //         }
        //         while nalt > 0 as libc::c_int {
        //             let fresh3 = dst;
        //             dst = dst.offset(1);
        //             *fresh3 = '|' as i32 as libc::c_char;
        //             nalt -= 1;
        //             nalt;
        //         }
        //         p = p.offset(-1);
        //         p;
        //         nalt = (*p).nalt;
        //         natom = (*p).natom;
        //         natom += 1;
        //         natom;
        //     }
        //     42 | 43 | 63 => {
        //         if natom == 0 as libc::c_int {
        //             return 0 as *mut libc::c_char;
        //         }
        //         let fresh4 = dst;
        //         dst = dst.offset(1);
        //         *fresh4 = *re;
        //     }
        //     _ => {
        //         if natom > 1 as libc::c_int {
        //             natom -= 1;
        //             natom;
        //             let fresh5 = dst;
        //             dst = dst.offset(1);
        //             *fresh5 = '.' as i32 as libc::c_char;
        //         }
        //         let fresh6 = dst;
        //         dst = dst.offset(1);
        //         *fresh6 = *re;
        //         natom += 1;
        //         natom;
        //     }
        // }
        // re = re.offset(1);
        // re;
    }
    // if p != paren.as_mut_ptr() {
    //     return 0 as *mut libc::c_char;
    // }
    // loop {
    //     natom -= 1;
    //     if !(natom > 0 as libc::c_int) {
    //         break;
    //     }
    //     let fresh7 = dst;
    //     dst = dst.offset(1);
    //     *fresh7 = '.' as i32 as libc::c_char;
    // }
    // while nalt > 0 as libc::c_int {
    //     let fresh8 = dst;
    //     dst = dst.offset(1);
    //     *fresh8 = '|' as i32 as libc::c_char;
    //     nalt -= 1;
    //     nalt;
    // }
    // *dst = 0 as libc::c_int as libc::c_char;
    // return buf.as_mut_ptr();
}