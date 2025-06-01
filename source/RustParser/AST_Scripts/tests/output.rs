#![allow(dead_code, mutable_transmutes, non_camel_case_types, non_snake_case, non_upper_case_globals, unused_assignments, unused_mut)]
#![feature(extern_types)]
extern "C" {
    pub type _IO_wide_data;
    pub type _IO_codecvt;
    pub type _IO_marker;
    static mut stderr: *mut FILE;
    fn fprintf(_: *mut FILE, _: *const libc::c_char, _: ...) -> libc::c_int;
    fn printf(_: *const libc::c_char, _: ...) -> libc::c_int;
    fn malloc(_: libc::c_ulong) -> *mut libc::c_void;
    fn strlen(_: *const libc::c_char) -> libc::c_ulong;
}
pub type size_t = libc::c_ulong;
pub type __off_t = libc::c_long;
pub type __off64_t = libc::c_long;
#[derive(Copy, Clone)]
#[repr(C)]
pub struct _IO_FILE {
    pub _flags: libc::c_int,
    pub _IO_read_ptr: *mut libc::c_char,
    pub _IO_read_end: *mut libc::c_char,
    pub _IO_read_base: *mut libc::c_char,
    pub _IO_write_base: *mut libc::c_char,
    pub _IO_write_ptr: *mut libc::c_char,
    pub _IO_write_end: *mut libc::c_char,
    pub _IO_buf_base: *mut libc::c_char,
    pub _IO_buf_end: *mut libc::c_char,
    pub _IO_save_base: *mut libc::c_char,
    pub _IO_backup_base: *mut libc::c_char,
    pub _IO_save_end: *mut libc::c_char,
    pub _markers: *mut _IO_marker,
    pub _chain: *mut _IO_FILE,
    pub _fileno: libc::c_int,
    pub _flags2: libc::c_int,
    pub _old_offset: __off_t,
    pub _cur_column: libc::c_ushort,
    pub _vtable_offset: libc::c_schar,
    pub _shortbuf: [libc::c_char; 1],
    pub _lock: *mut libc::c_void,
    pub _offset: __off64_t,
    pub _codecvt: *mut _IO_codecvt,
    pub _wide_data: *mut _IO_wide_data,
    pub _freeres_list: *mut _IO_FILE,
    pub _freeres_buf: *mut libc::c_void,
    pub __pad5: size_t,
    pub _mode: libc::c_int,
    pub _unused2: [libc::c_char; 20],
}
pub type _IO_lock_t = ();
pub type FILE = _IO_FILE;
#[derive(Copy, Clone)]
#[repr(C)]
pub struct C2RustUnnamed {
    pub nalt: libc::c_int,
    pub natom: libc::c_int,
}
pub type C2RustUnnamed_0 = libc::c_uint;
// pub const Split: C2RustUnnamed_0 = 257;
// pub const Match: C2RustUnnamed_0 = 256;
#[derive(Copy, Clone)]
#[repr(C)]
pub struct State {
    pub c: libc::c_int,
    pub out: *mut State,
    pub out1: *mut State,
    pub lastlist: libc::c_int,
}
#[derive(Copy, Clone)]
#[repr(C)]
pub struct Frag {
    pub start: *mut State,
    pub out: *mut Ptrlist,
}
#[derive(Copy, Clone)]
#[repr(C)]
pub union Ptrlist {
    pub next: *mut Ptrlist,
    pub s: *mut State,
}
#[derive(Copy, Clone)]
#[repr(C)]
pub struct List {
    pub s: *mut *mut State,
    pub n: libc::c_int,
}
#[no_mangle]
pub unsafe extern "C" fn re2post(mut re: *mut libc::c_char) -> *mut libc::c_char {
    let mut nalt: libc::c_int = 0;
    let mut natom: libc::c_int = 0;
    static mut buf: [libc::c_char; 8000] = [0; 8000];
    let mut dst: *mut libc::c_char = 0 as *mut libc::c_char;
    let mut paren: [C2RustUnnamed; 100] = [C2RustUnnamed { nalt: 0, natom: 0 }; 100];
    let mut p: *mut C2RustUnnamed = 0 as *mut C2RustUnnamed;
    p = paren.as_mut_ptr();
    dst = buf.as_mut_ptr();
    nalt = 0 as libc::c_int;
    natom = 0 as libc::c_int;
    if strlen(re) >= (::core::mem::size_of::[libc::c_char; 8000]() as libc::c_ulong).wrapping_div(2 as libc::c_int as libc::c_ulong)
    {
        return 0 as *mut libc::c_char;
    }
    while *re != 0 {
        match *re as libc::c_int {
            40 => {
                if natom > 1 as libc::c_int {
                    natom -= 1;
                    natom;
                    let fresh0 = dst;
                    dst = dst.offset(1);
                    *fresh0 = '.' as i32 as libc::c_char ;
                }
                if p >= paren.as_mut_ptr().offset(100 as libc::c_int as isize) {
                    return 0 as *mut libc::c_char;
                }
                (*p).nalt = nalt;
                (*p).natom = natom;
                p = p.offset(1);
                p;
                nalt = 0 as libc::c_int;
                natom = 0 as libc::c_int;
            }
            124 => {
                if natom == 0 as libc::c_int {
                    return 0 as *mut libc::c_char;
                }
                loop {
                    natom -= 1;
                    if !(natom > 0 as libc::c_int) {
                        break;
                    }
                    let fresh1 = dst;
                    dst = dst.offset(1);
                    *fresh1 = '.' as i32 as libc::c_char;
                }
                nalt += 1;
                nalt;
            }
            41 => {
                if p == paren.as_mut_ptr() {
                    return 0 as *mut libc::c_char;
                }
                if natom == 0 as libc::c_int {
                    return 0 as *mut libc::c_char;
                }
                loop {
                    natom -= 1;
                    if !(natom > 0 as libc::c_int) {
                        break;
                    }
                    let fresh2 = dst;
                    dst = dst.offset(1);
                    *fresh2 = '.' as i32 as libc::c_char;
                }
                while nalt > 0 as libc::c_int {
                    let fresh3 = dst;
                    dst = dst.offset(1);
                    *fresh3 = '|' as i32 as libc::c_char;
                    nalt -= 1;
                    nalt;
                }
                p = p.offset(-1);
                p;
                nalt = (*p).nalt;
                natom = (*p).natom;
                natom += 1;
                natom;
            }
            42 | 43 | 63 => {
                if natom == 0 as libc::c_int {
                    return 0 as *mut libc::c_char;
                }
                let fresh4 = dst;
                dst = dst.offset(1);
                *fresh4 = *re;
            }
            _ => {
                if natom > 1 as libc::c_int {
                    natom -= 1;
                    natom;
                    let fresh5 = dst;
                    dst = dst.offset(1);
                    *fresh5 = '.' as i32 as libc::c_char;
                }
                let fresh6 = dst;
                dst = dst.offset(1);
                *fresh6 = *re;
                natom += 1;
                natom;
            }
        }
        re = re.offset(1);
        re;
    }
    if p != paren.as_mut_ptr() {
        return 0 as *mut libc::c_char;
    }
    loop {
        natom -= 1;
        if !(natom > 0 as libc::c_int) {
            break;
        }
        let fresh7 = dst;
        dst = dst.offset(1);
        *fresh7 = '.' as i32 as libc::c_char;
    }
    while nalt > 0 as libc::c_int {
        let fresh8 = dst;
        dst = dst.offset(1);
        *fresh8 = '|' as i32 as libc::c_char;
        nalt -= 1;
        nalt;
    }
    *dst = 0 as libc::c_int as libc::c_char;
    return buf.as_mut_ptr();
}
#[no_mangle]
pub static mut matchstate: State = {
    let mut init = State {
        c: Match as libc::c_int,
        out: 0 as *const State as *mut State,
        out1: 0 as *const State as *mut State,
        lastlist: 0,
    };
    init
};
#[no_mangle]
pub static mut nstate: libc::c_int = 0;
#[no_mangle]
pub unsafe extern "C" fn state(
    mut c: libc::c_int,
    mut out: *mut State,
    mut out1: *mut State,
) -> *mut State  {
    let mut s: *mut State = 0 as *mut State;
    nstate += 1;
    nstate;
    //not handled yet
    s = malloc(core::mem::size_of:: <State> () as libc::c_ulong) as *mut State;
    (*s).lastlist = 0 as libc::c_int;
    (*s).c = c;
    (*s).out = out;
    (*s).out1 = out1;
    return s;
}
#[no_mangle]
pub unsafe extern "C" fn frag(mut start: *mut State, mut out: *mut Ptrlist) -> Frag {
    let mut n: Frag = {
        let mut init = Frag {
             start: start,
             out: out
            };
        init
    };
    return n;
}
#[no_mangle]
pub unsafe extern "C" fn list1(mut outp: *mut *mut State) -> *mut Ptrlist {
    let mut l: *mut Ptrlist = 0 as *mut Ptrlist;
    l = outp as *mut Ptrlist;
    (*l).next = 0 as *mut Ptrlist;
    return l;
}
#[no_mangle]
pub unsafe extern "C" fn patch(mut l: *mut Ptrlist, mut s: *mut State) {
    let mut next: *mut Ptrlist = 0 as *mut Ptrlist;
    while !l.is_null() {
        next = (*l).next;
        (*l).s = s;
        l = next;
    }
}
#[no_mangle]
pub unsafe extern "C" fn append(
    mut l1_0: *mut Ptrlist,
    mut l2_0: *mut Ptrlist,
) -> *mut Ptrlist {
    let mut oldl1: *mut Ptrlist = 0 as *mut Ptrlist;
    oldl1 = l1_0;
    while !((*l1_0).next).is_null() {
        l1_0 = (*l1_0).next;
    }
    (*l1_0).next = l2_0;
    return oldl1;
}
#[no_mangle]
pub unsafe extern "C" fn post2nfa(mut postfix: *mut libc::c_char) -> *mut State {
    let mut p: *mut libc::c_char = 0 as *mut libc::c_char;
    let mut stack: [Frag; 1000] = [Frag {
        start: 0 as *mut State,
        out: 0 as *mut Ptrlist,
    }; 1000];
    let mut stackp: *mut Frag = 0 as *mut Frag;
    let mut e1: Frag = Frag {
        start: 0 as *mut State,
        out: 0 as *mut Ptrlist,
    };
    let mut e2: Frag = Frag {
        start: 0 as *mut State,
        out: 0 as *mut Ptrlist,
    };
    let mut e: Frag = Frag {
        start: 0 as *mut State,
        out: 0 as *mut Ptrlist,
    };
    let mut s: *mut State = 0 as *mut State;
    if postfix.is_null() {
        return 0 as *mut State;
    }
    stackp = stack.as_mut_ptr();
    p = postfix;
    while *p != 0 {
        match *p as libc::c_int {
            46 => {
                stackp = stackp.offset(-1);
                e2 = *stackp;
                stackp = stackp.offset(-1);
                e1 = *stackp;
                patch(e1.out, e2.start);
                let fresh10 = stackp;
                stackp = stackp.offset(1);
                *fresh10 = frag(e1.start, e2.out);
            }
            124 => {
                stackp = stackp.offset(-1);
                e2 = *stackp;
                stackp = stackp.offset(-1);
                e1 = *stackp;
                s = state(Split as libc::c_int, e1.start, e2.start);
                let fresh11 = stackp;
                stackp = stackp.offset(1);
                *fresh11 = frag(s, append(e1.out, e2.out));
            }
            63 => {
                stackp = stackp.offset(-1);
                e = *stackp;
                s = state(Split as libc::c_int, e.start, 0 as *mut State);
                let fresh12 = stackp;
                stackp = stackp.offset(1);
                *fresh12 = frag(s, 1);
            }
            42 => {
                stackp = stackp.offset(-1);
                e = *stackp;
                s = state(Split as libc::c_int, e.start, 0 as *mut State);
                patch(e.out, s);
                let fresh13 = stackp;
                stackp = stackp.offset(1);
                *fresh13 = frag(s, list1(&mut (*s).out1));
            }
            43 => {
                stackp = stackp.offset(-1);
                e = *stackp;
                s = state(Split as libc::c_int, e.start, 0 as *mut State);
                patch(e.out, s);
                let fresh14 = stackp;
                stackp = stackp.offset(1);
                *fresh14 = frag(e.start, list1(&mut (*s).out1));
            }
            _ => {
                s = state(*p as libc::c_int, 0 as *mut State, 0 as *mut State);
                let fresh9 = stackp;
                stackp = stackp.offset(1);
                *fresh9 = frag(s, list1(&mut (*s).out));
            }
        }
        p = p.offset(1);
        p;
    }
    stackp = stackp.offset(-1);
    e = *stackp;
    if stackp != stack.as_mut_ptr() {
        return 0 as *mut State;
    }
    patch(e.out, &mut matchstate);
    return e.start;
}
#[no_mangle]
pub static mut l1: List = List {
    s: 0 as *const *mut State as *mut *mut State,
    n: 0,
};
#[no_mangle]
pub static mut l2: List = List {
    s: 0 as *const *mut State as *mut *mut State,
    n: 0,
};
static mut listid: libc::c_int = 0;
#[no_mangle]
pub unsafe extern "C" fn startlist(
    mut start: *mut State,
    mut l: *mut List,
) -> *mut List {
    (*l).n = 0 as libc::c_int;
    listid += 1;
    listid;
    addstate(l, start);
    return l;
}
#[no_mangle]
pub unsafe extern "C" fn ismatch(mut l: *mut List) -> libc::c_int {
    let mut i: libc::c_int = 0;
    i = 0 as libc::c_int;
    while i < (*l).n {
        if *((*l).s).offset(i as isize) == &mut matchstate as *mut State {
            return 1 as libc::c_int;
        }
        i += 1;
        i;
    }
    return 0 as libc::c_int;
}
#[no_mangle]
pub unsafe extern "C" fn addstate(mut l: *mut List, mut s: *mut State) {
    if s.is_null() || (*s).lastlist == listid {
        return;
    }
    (*s).lastlist = listid;
    if (*s).c == Split as libc::c_int {
        addstate(l, (*s).out);
        addstate(l, (*s).out1);
        return;
    }
    let fresh15 = (*l).n;
    (*l).n = (*l).n + 1;
    let ref mut fresh16 = *((*l).s).offset(fresh15 as isize);
    *fresh16 = s;
}
#[no_mangle]
pub unsafe extern "C" fn step(
    mut clist: *mut List,
    mut c: libc::c_int,
    mut nlist: *mut List,
) {
    let mut i: libc::c_int = 0;
    let mut s: *mut State = 0 as *mut State;
    listid += 1;
    listid;
    (*nlist).n = 0 as libc::c_int;
    i = 0 as libc::c_int;
    while i < (*clist).n {
        s = *((*clist).s).offset(i as isize);
        if (*s).c == c {
            addstate(nlist, (*s).out);
        }
        i += 1;
        i;
    }
}
#[export_name = "match"]
pub unsafe extern "C" fn match_0(
    mut start: *mut State,
    mut s: *mut libc::c_char,
) -> libc::c_int {
    let mut i: libc::c_int = 0;
    let mut c: libc::c_int = 0;
    let mut clist: *mut List = 0 as *mut List;
    let mut nlist: *mut List = 0 as *mut List;
    let mut t: *mut List = 0 as *mut List;
    // clist = startlist(start, &mut l1);
    nlist = &mut l2;
    while *s != 0 {
        c = *s as libc::c_int & 0xff as libc::c_int;
        step(clist, c, nlist);
        t = clist;
        clist = nlist;
        nlist = t;
        s = s.offset(1);
        s;
    }
    return ismatch(clist);
}
unsafe fn main_0(
    mut argc: libc::c_int,
    mut argv: *mut *mut libc::c_char,
) -> libc::c_int {
    let mut i: libc::c_int = 0;
    let mut post: *mut libc::c_char = 0 as *mut libc::c_char;
    let mut start: *mut State = 0 as *mut State;
    if argc < 3 as libc::c_int {
        fprintf(stderr, b"usage: nfa regexp string...\n\0" as *const u8 as *const libc::c_char);
        return 1 as libc::c_int;
    }
    post = re2post(*argv.offset(1 as libc::c_int as isize));
    if post.is_null() {
        fprintf(stderr,b"bad regexp %s\n\0" as *const u8 as *const libc::c_char,*argv.offset(1 as libc::c_int as isize) );
        return 1 as libc::c_int;
    }
    start = post2nfa(post);
    if start.is_null() {
        fprintf(stderr,b"error in post2nfa %s\n\0" as *const u8 as *const libc::c_char,post);
        return 1 as libc::c_int;
    }
    l1.s = malloc( (nstate as libc::c_ulong).wrapping_mul(core::mem::size_of:: <*mut State> () as libc::c_ulong) ) as *mut State;
    l2.s = malloc((nstate as libc::c_ulong).wrapping_mul(core::mem::size_of::<*mut State>() as libc::c_ulong)) as *mut State;
    i = 2 as libc::c_int;
    while i < argc {
        if match_0(start, *argv.offset(i as isize)) != 0 {
            printf(
                b"%s\n\0" as *const as *const libc::c_char,
                *argv.offset(i as isize)
            );
        }
        i += 1;
        i;
    }
    return 0 as libc::c_int;
}

pub fn main() {
    let mut args: Vec::<*mut libc::c_char> = Vec::new();
    for arg in ::std::env::args() {
        args.push( (std::ffi::CString::new(arg)).expect("Failed to convert argument into CString.").into_raw() );
    }
    args.push(core::ptr::null_mut());
    unsafe {
        std::process::exit(main_0( (args.len() - 1) as libc::c_int, args.as_mut_ptr() as *mut libc::c_char) as i32);
    }
}
