unsafe fn main_0(
    // mut argc: libc::c_int,
    // mut argv: *mut *mut libc::c_char,
) -> libc::c_int {
    // let mut i: libc::c_int = 0;
    // let mut post: *mut libc::c_char = 0 as *mut libc::c_char;
    // let mut start: *mut State = 0 as *mut State;
    // if argc < 3 as libc::c_int {
    //     fprintf(stderr, b"usage: nfa regexp string...\n\0" as *const u8 as *const libc::c_char);
    //     return 1 as libc::c_int;
    // }
    // post = re2post(*argv.offset(1 as libc::c_int as isize));
    // if post.is_null() {
    //     fprintf(stderr,b"bad regexp %s\n\0" as *const u8 as *const libc::c_char,*argv.offset(1 as libc::c_int as isize) );
    //     return 1 as libc::c_int;
    // }
    // start = post2nfa(post);
    // if start.is_null() {
    //     fprintf(stderr,b"error in post2nfa %s\n\0" as *const u8 as *const libc::c_char,post);
    //     return 1 as libc::c_int;
    // }
    // l1.s = malloc( (nstate as libc::c_ulong).wrapping_mul(core::mem::size_of:: <*mut State> () as libc::c_ulong) ) as *mut State;
    // l2.s = malloc((nstate as libc::c_ulong).wrapping_mul(core::mem::size_of::<*mut State>() as libc::c_ulong)) as *mut State;
    // i = 2 as libc::c_int;
    // while i < argc {
    //     if match_0(start, *argv.offset(i as isize)) != 0 {
            // printf(
            //     b"%s\n\0" as *const as *const libc::c_char,
            //     *argv.offset(i as isize)
            // );
        // }
        i += 1;
        i;
    // }
    // return 0 as libc::c_int;
}