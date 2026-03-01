use std::ptr::{null_mut, addr_of_mut};

const MATCH: i32 = 256;
const SPLIT: i32 = 257;

struct State {
    c: i32,
    out: *mut State,
    out1: *mut State,
    lastlist: i32,
}

static mut MATCH_STATE: State = State {
    c: MATCH,
    out: null_mut(),
    out1: null_mut(),
    lastlist: 0,
};

static mut NSTATE: i32 = 0;
static mut LIST_ID: i32 = 0;

unsafe fn new_state(c: i32, out: *mut State, out1: *mut State) -> *mut State {
    NSTATE += 1;
    let s = Box::new(State {
        c,
        out,
        out1,
        lastlist: 0,
    });
    Box::into_raw(s)
}

struct Frag {
    start: *mut State,
    out: *mut PtrList,
}

impl Frag {
    fn new(start: *mut State, out: *mut PtrList) -> Frag {
        Frag { start, out }
    }
}

union PtrList {
    next: *mut PtrList,
    s: *mut State,
}

unsafe fn list1(outp: *mut *mut State) -> *mut PtrList {
    let l = outp.cast::<PtrList>();
    (*l).next = null_mut();
    l
}

unsafe fn patch(mut l: *mut PtrList, s: *mut State) {
    while !l.is_null() {
        let next = (*l).next;
        (*l).s = s;
        l = next;
    }
}

unsafe fn append(mut l1: *mut PtrList, l2: *mut PtrList) -> *mut PtrList {
    let start = l1;
    while !(*l1).next.is_null() {
        l1 = (*l1).next;
    }
    (*l1).next = l2;
    start
}

fn re2post(re: &[u8]) -> Option<Vec<u8>> {
    struct Paren {
        nalt: i32,
        natom: i32,
    }

    if re.is_empty() || re.len() > 4000 {
        return None;
    }

    let mut nalt = 0;
    let mut natom = 0;
    let mut paren: Vec<Paren> = vec![];
    let mut dst: Vec<u8> = vec![];

    let mut i = 0;
    while i < re.len() {
        let b = re[i];
        match b {
            b'(' => {
                if natom > 1 {
                    natom -= 1;
                    dst.push(b'.');
                }
                if paren.len() > 100 {
                    return None;
                }
                paren.push(Paren { nalt, natom });
                nalt = 0;
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
                if paren.is_empty() {
                    return None;
                }
                let p = paren.pop().unwrap();
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
                natom = p.natom + 1;
            }
            b'*' | b'+' | b'?' => {
                if natom == 0 {
                    return None;
                }
                dst.push(b);
            }
            _ => {
                if natom > 1 {
                    natom -= 1;
                    dst.push(b'.');
                }
                dst.push(b);
                natom += 1;
            }
        }
        i += 1;
    }

    if !paren.is_empty() {
        return None;
    }
    if natom == 0 && nalt > 0 {
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

    Some(dst)
}

unsafe fn post2nfa(postfix: &[u8]) -> *mut State {
    let mut stack: [Frag; 1000] = [Frag { start: null_mut(), out: null_mut() }; 1000];
    let mut sp = 0;

    for &p in postfix {
        if p == b'.' {
            let e2 = stack[sp - 1];
            let e1 = stack[sp - 2];
            patch(e1.out, e2.start);
            stack[sp - 2] = Frag::new(e1.start, e2.out);
            sp -= 1;
        } else if p == b'|' {
            let e2 = stack[sp - 1];
            let e1 = stack[sp - 2];
            let s = new_state(SPLIT, e1.start, e2.start);
            let list = append(e1.out, e2.out);
            stack[sp - 2] = Frag::new(s, list);
            sp -= 1;
        } else if p == b'?' {
            let e = stack[sp - 1];
            let s = new_state(SPLIT, e.start, null_mut());
            let list = append(e.out, list1(addr_of_mut!((*s).out1)));
            stack[sp - 1] = Frag::new(s, list);
        } else if p == b'*' {
            let e = stack[sp - 1];
            let s = new_state(SPLIT, e.start, null_mut());
            patch(e.out, s);
            let list = list1(addr_of_mut!((*s).out1));
            stack[sp - 1] = Frag::new(s, list);
        } else if p == b'+' {
            let e = stack[sp - 1];
            let s = new_state(SPLIT, e.start, null_mut());
            patch(e.out, s);
            let list = list1(addr_of_mut!((*s).out1));
            stack[sp - 1] = Frag::new(e.start, list);
        } else {
            let s = new_state(p as i32, null_mut(), null_mut());
            let list = list1(addr_of_mut!((*s).out));
            stack[sp] = Frag::new(s, list);
            sp += 1;
        }
    }

    let e = stack[sp - 1];
    patch(e.out, addr_of_mut!(MATCH_STATE));
    e.start
}

struct List {
    s: [*mut State; 1000],
    n: i32,
}

unsafe fn add_state(l: &mut List, s: *mut State) {
    if s.is_null() || (*s).lastlist == LIST_ID {
        return;
    }
    (*s).lastlist = LIST_ID;
    if (*s).c == SPLIT {
        add_state(l, (*s).out);
        add_state(l, (*s).out1);
        return;
    }
    l.s[l.n as usize] = s;
    l.n += 1;
}

unsafe fn start_list(start: *mut State, l: &mut List) {
    l.n = 0;
    LIST_ID += 1;
    add_state(l, start);
}

unsafe fn step(clist: &List, c: i32, nlist: &mut List) {
    LIST_ID += 1;
    nlist.n = 0;
    let mut i = 0;
    while i < clist.n {
        let s = clist.s[i as usize];
        if (*s).c == c {
            add_state(nlist, (*s).out);
        }
        i += 1;
    }
}

unsafe fn is_match(l: &List) -> bool {
    let mut i = 0;
    while i < l.n {
        if l.s[i as usize] == addr_of_mut!(MATCH_STATE) {
            return true;
        }
        i += 1;
    }
    false
}

unsafe fn rmatch(start: *mut State, s: &[u8]) -> bool {
    let mut l1 = List {
        s: [null_mut(); 1000],
        n: 0,
    };
    let mut l2 = List {
        s: [null_mut(); 1000],
        n: 0,
    };

    start_list(start, &mut l1);
    let mut clist = &mut l1;
    let mut nlist = &mut l2;

    let mut i = 0;
    while i < s.len() {
        step(clist, s[i] as i32, nlist);
        let tmp = clist;
        clist = nlist;
        nlist = tmp;
        i += 1;
    }

    is_match(clist)
}

fn main() {
    let pattern = b"(a|b)*abb";
    let text = b"aabbabb";

    let post = re2post(pattern).unwrap();
    let start = unsafe { post2nfa(&post) };
    let matched = unsafe { rmatch(start, text) };

    if matched {
        println!("Matched!");
    } else {
        println!("No match.");
    }
}
