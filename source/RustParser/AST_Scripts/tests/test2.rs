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
    // //not handled yet
    // s = malloc(core::mem::size_of:: <State> () as libc::c_ulong) as *mut State;
    // (*s).lastlist = 0 as libc::c_int;
    // (*s).c = c;
    // (*s).out = out;
    // (*s).out1 = out1;
    return s;
}
// #[no_mangle]
// pub unsafe extern "C" fn frag(mut start: *mut State, mut out: *mut Ptrlist) -> Frag {
//     let mut n: Frag = {
//         let mut init = Frag {
//              start: start,
//              out: out
//             };
//         init
//     };
//     return n;
// }
// #[no_mangle]
// pub unsafe extern "C" fn list1(mut outp: *mut *mut State) -> *mut Ptrlist {
//     let mut l: *mut Ptrlist = 0 as *mut Ptrlist;
//     l = outp as *mut Ptrlist;
//     (*l).next = 0 as *mut Ptrlist;
//     return l;
// }
// #[no_mangle]
// pub unsafe extern "C" fn patch(mut l: *mut Ptrlist, mut s: *mut State) {
//     let mut next: *mut Ptrlist = 0 as *mut Ptrlist;
//     while !l.is_null() {
//         next = (*l).next;
//         (*l).s = s;
//         l = next;
//     }
// }
// #[no_mangle]
// pub unsafe extern "C" fn append(
//     mut l1_0: *mut Ptrlist,
//     mut l2_0: *mut Ptrlist,
// ) -> *mut Ptrlist {
//     let mut oldl1: *mut Ptrlist = 0 as *mut Ptrlist;
//     oldl1 = l1_0;
//     while !((*l1_0).next).is_null() {
//         l1_0 = (*l1_0).next;
//     }
//     (*l1_0).next = l2_0;
//     return oldl1;
// }
// #[no_mangle]
// pub unsafe extern "C" fn post2nfa(mut postfix: *mut libc::c_char) -> *mut State {
//     let mut p: *mut libc::c_char = 0 as *mut libc::c_char;
//     let mut stack: [Frag; 1000] = [Frag {
//         start: 0 as *mut State,
//         out: 0 as *mut Ptrlist,
//     }; 1000];
//     let mut stackp: *mut Frag = 0 as *mut Frag;
//     let mut e1: Frag = Frag {
//         start: 0 as *mut State,
//         out: 0 as *mut Ptrlist,
//     };
//     let mut e2: Frag = Frag {
//         start: 0 as *mut State,
//         out: 0 as *mut Ptrlist,
//     };
//     let mut e: Frag = Frag {
//         start: 0 as *mut State,
//         out: 0 as *mut Ptrlist,
//     };
//     let mut s: *mut State = 0 as *mut State;
//     if postfix.is_null() {
//         return 0 as *mut State;
//     }
//     stackp = stack.as_mut_ptr();
//     p = postfix;
//     while *p != 0 {
//         match *p as libc::c_int {
//             46 => {
//                 stackp = stackp.offset(-1);
//                 e2 = *stackp;
//                 stackp = stackp.offset(-1);
//                 e1 = *stackp;
//                 patch(e1.out, e2.start);
//                 let fresh10 = stackp;
//                 stackp = stackp.offset(1);
//                 *fresh10 = frag(e1.start, e2.out);
//             }
//             124 => {
//                 stackp = stackp.offset(-1);
//                 e2 = *stackp;
//                 stackp = stackp.offset(-1);
//                 e1 = *stackp;
//                 s = state(Split as libc::c_int, e1.start, e2.start);
//                 let fresh11 = stackp;
//                 stackp = stackp.offset(1);
//                 *fresh11 = frag(s, append(e1.out, e2.out));
//             }
//             63 => {
//                 stackp = stackp.offset(-1);
//                 e = *stackp;
//                 s = state(Split as libc::c_int, e.start, 0 as *mut State);
//                 let fresh12 = stackp;
//                 stackp = stackp.offset(1);
//                 *fresh12 = frag(s, 1);
//             }
//             42 => {
//                 stackp = stackp.offset(-1);
//                 e = *stackp;
//                 s = state(Split as libc::c_int, e.start, 0 as *mut State);
//                 patch(e.out, s);
//                 let fresh13 = stackp;
//                 stackp = stackp.offset(1);
//                 *fresh13 = frag(s, list1(&mut (*s).out1));
//             }
//             43 => {
//                 stackp = stackp.offset(-1);
//                 e = *stackp;
//                 s = state(Split as libc::c_int, e.start, 0 as *mut State);
//                 patch(e.out, s);
//                 let fresh14 = stackp;
//                 stackp = stackp.offset(1);
//                 *fresh14 = frag(e.start, list1(&mut (*s).out1));
//             }
//             _ => {
//                 s = state(*p as libc::c_int, 0 as *mut State, 0 as *mut State);
//                 let fresh9 = stackp;
//                 stackp = stackp.offset(1);
//                 *fresh9 = frag(s, list1(&mut (*s).out));
//             }
//         }
//         p = p.offset(1);
//         p;
//     }
//     stackp = stackp.offset(-1);
//     e = *stackp;
//     if stackp != stack.as_mut_ptr() {
//         return 0 as *mut State;
//     }
//     patch(e.out, &mut matchstate);
//     return e.start;
// }
// #[no_mangle]
// pub static mut l1: List = List {
//     s: 0 as *const *mut State as *mut *mut State,
//     n: 0,
// };
// #[no_mangle]
// pub static mut l2: List = List {
//     s: 0 as *const *mut State as *mut *mut State,
//     n: 0,
// };
// static mut listid: libc::c_int = 0;
// #[no_mangle]
// pub unsafe extern "C" fn startlist(
//     mut start: *mut State,
//     mut l: *mut List,
// ) -> *mut List {
//     (*l).n = 0 as libc::c_int;
//     listid += 1;
//     listid;
//     addstate(l, start);
//     return l;
// }
// #[no_mangle]
// pub unsafe extern "C" fn ismatch(mut l: *mut List) -> libc::c_int {
//     let mut i: libc::c_int = 0;
//     i = 0 as libc::c_int;
//     while i < (*l).n {
//         if *((*l).s).offset(i as isize) == &mut matchstate as *mut State {
//             return 1 as libc::c_int;
//         }
//         i += 1;
//         i;
//     }
//     return 0 as libc::c_int;
// }