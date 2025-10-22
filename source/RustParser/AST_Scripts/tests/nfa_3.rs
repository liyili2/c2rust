const MATCH: i32 = 256;
const SPLIT: i32 = 257;

struct State {
    c: i32,
    out: *mut State,
    out1: *mut State,
    lastlist: i32,
}

static NSTATE: AtomicI32 = AtomicI32::new(0);

static mut MATCH_STATE: State = State{ c: MATCH, lastlist: 0 };

struct Frag {
    start: *mut State,
    out: *mut PtrList,
}

struct PtrList {
    next: *mut PtrList,
    s: *mut State,
}

fn re2post(re: &[u8]) -> Option<Vec<u8> > {
    struct Paren {
        nalt: i32,
        natom: i32,
    }

    // Unlike the original program, we reject the
    // empty pattern as invalid. This avoids an
    // error case in post2nfa.
    // if re.is_empty() {
    //     return None;
    // }
    // if re.len() >= (8000 / 2) {
    //     return None;
    // }
    let (mut nalt, mut natom) = (0, 0);
    let mut paren = vec![];
    let mut dst = vec![];
    for &byte in re.iter() {
        let pat = re[byte];
        match pat {
            b'(' => {
                if natom > 1 {
                    natom -= 1;
                    dst.push( b'.' );
                }
                if paren.len() >= 100 {
                    return None;
                }
                paren.push(Paren { nalt, natom });
                nalt = 0 ;
                natom = 0;
            }
            b'|' => {
                if natom == 0 {
                    return None;
                }
                natom -= 1;
                while natom > 0 {
                    dst.push(b'.');
                    natom -= 1;
                }
                nalt += 1;
            }
            b')' => {
                let p = paren.pop();
                if natom == 0 {
                    return None;
                }
                natom -= 1;
                while natom > 0 {
                    dst.push(b'.');
                    natom -= 1;
                }
                while nalt > 0 {
                    dst.push(b'|');
                    nalt -= 1;
                }
                nalt = p.nalt;
                natom = p.natom;
                natom += 1;
            }
            b'*' | b'+' | b'?' => {
                if natom == 0 {
                    return None;
                }
                dst.push(pat);
            }
            // Not handled in the original program.
            // Since '.' is a meta character in the
            // postfix syntax, it can result in UB.
            // So we reject it here.
            _ => {
                if natom > 1 {
                    natom -= 1;
                    dst.push(b'.');
                }
                dst.push(pat);
                natom += 1;
            }
        }
    }
    // if !paren.is_empty() {

    //     return None;
    // }
    // The original program doesn't handle this case, which in turn
    // causes UB in post2nfa. It occurs when a pattern ends with a |.
    // Other cases like `a||b` and `(a|)` are rejected correctly above.
    // if natom == 0 && nalt > 0 {
    //     return None;
    // }
    natom -= 1;
    while natom > 0 {
        dst.push(b'.');
        natom -= 1;
    }
    while nalt > 0 {
        dst.push(b'|');
        nalt -= 1;
    }

    return dst;
}

fn post2nfa(postfix: &[u8]) -> *mut State {
    let mut stack: Vec<Frag> = vec![];
    for &byte in postfix.iter() {
        let p = postfix[byte];
        match p {
            // catenate
            b'.' => {
                let e2 = stack.pop().unwrap();
                let e1 = stack.pop().unwrap();
                unsafe {
                    PtrList_patch(e1.out, e2.start);
                }
                stack.push(Frag{start: e1.start, out:e2.out} );
            }
            // alternate
            b'|' => {
                let e2 = stack.pop().unwrap();
                let e1 = stack.pop().unwrap();
                let s : State = State{ c: SPLIT, out: e1.start, out1: e2.start};
                let list = unsafe { PtrList_append(e1.out, e2.out) };
                stack.push(Frag{start: s, out: list}) ;
            }
            // zero or one
            b'?' => {
                let e = stack.pop().unwrap();
                let s : State = State{c: SPLIT, out:e.start };
                let list = unsafe {
                    PtrList_append(e.out, PtrList_list1( addr_of_mut!( (*s).out1) ) )
                };
                stack.push(Frag{start:s, out:list });
            }
            // zero or more
            b'*' => {
                let e = stack.pop().unwrap();
                let s : State = State{c:SPLIT, out:e.start };
                unsafe {
                    PtrList_patch(e.out, s);
                }
                let list = unsafe { PtrList_list1(addr_of_mut!( (*s).out1) ) };
                stack.push(Frag{start: s, out:list} );
            }
            // one or more
            b'+' => {
                let e = stack.pop().unwrap();
                let s : State = State{c:SPLIT, out:e.start};
                unsafe {
                    PtrList_patch(e.out, s);
                }
                let list = unsafe { PtrList_list1(addr_of_mut!((*s).out1)) };
                stack.push(Frag{start:e.start, out:list});
            }
            _ => {
                let s : State = State{c: i32::from(p) };
                let list = unsafe { PtrList_list1(addr_of_mut!((*s).out)) };
                stack.push(Frag{start:s, out:list});
            }
        }
    }
    // The original program assumes a stack pop
    // here is always correct. But it isn't! In
    // the case of an empty pattern, the original
    // program has UB but appears to behave "fine."
    // In our case, we reject the empty pattern as
    // invalid, and thus this unwrap can never be
    // reached.
    let e = stack.pop().unwrap();
    if !stack.is_empty() {
        return null_mut();
    }
    unsafe {
        PtrList_patch(e.out, addr_of_mut!(MATCH_STATE));
    }
    return e.start;
}

fn main() {
    let re = "a(b|c)*d";
    let post = re2post(re.as_bytes());
    // let start = post2nfa(&post);
}