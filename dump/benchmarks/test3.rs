#[no_mangle]
pub static mut l2: List = List {
    s: 0 as *const *mut State as *mut *mut State,
    n: 0,
};
pub static mut l1: List = List {
    s: 0 as *const *mut State as *mut *mut State,
    n: 0,
};
// static mut listid: libc::c_int = 0;
// pub unsafe extern "C" fn addstate(mut l: *mut List, mut s: *mut State) {
//     if s.is_null() || (*s).lastlist == listid {
//         return;
//     }
//     (*s).lastlist = listid;
//     if (*s).c == Split as libc::c_int {
//         addstate(l, (*s).out);
//         addstate(l, (*s).out1);
//         return;
//     }
//     let fresh15 = (*l).n;
//     (*l).n = (*l).n + 1;
//     let ref mut fresh16 = *((*l).s).offset(fresh15 as isize);
//     *fresh16 = s;
// }
// #[no_mangle]
// pub unsafe extern "C" fn step(
//     mut clist: *mut List,
//     mut c: libc::c_int,
//     mut nlist: *mut List,
// ) {
//     let mut i: libc::c_int = 0;
//     let mut s: *mut State = 0 as *mut State;
//     listid += 1;
//     listid;
//     (*nlist).n = 0 as libc::c_int;
//     i = 0 as libc::c_int;
//     while i < (*clist).n {
//         s = *((*clist).s).offset(i as isize);
//         if (*s).c == c {
//             addstate(nlist, (*s).out);
//         }
//         i += 1;
//         i;
//     }
// }
// #[export_name = "match"]
pub unsafe extern "C" fn match_0(
    mut start: *mut State,
    mut s: *mut libc::c_char,
) -> libc::c_int {
    let mut i: libc::c_int = 0;
    let mut c: libc::c_int = 0;
    let mut clist: *mut List = 0 as *mut List;
    let mut nlist: *mut List = 0 as *mut List;
    let mut t: *mut List = 0 as *mut List;
    clist = startlist(start, &mut l1);
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
