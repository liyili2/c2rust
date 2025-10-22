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

fn post2nfa(postfix: &[u8]) -> *mut State {
    let mut stack: Vec<Frag> = vec![];
    for &p in postfix.iter() {
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

struct List {
    s: Box< [*mut State] >,
    n: i32,
}
static LIST_ID: AtomicI32 = AtomicI32::new(0);

unsafe fn list_start(&mut self, start: *mut State) -> &mut List {
    self.n = 0;
    LIST_ID.fetch_add(1, Ordering::AcqRel);
    self.list_add_state(start);
    return self;
}

unsafe fn list_is_match(&mut self) -> bool {
    for i in 0..self.n {
        if self.s[i] == addr_of_mut!(MATCH_STATE) {
            return true;
        }
    }
    return false;
}

unsafe fn list_add_state(&mut self, s: *mut State) {
    if s.is_null() || (*s).lastlist == LIST_ID.load(Ordering::Acquire) {
        return;
    }
    (*s).lastlist = LIST_ID.load(Ordering::Acquire);
    if (*s).c == SPLIT {
        // follow unlabeled arrows
        list_add_state(self, (*s).out);
        list_add_state(self, (*s).out1);
        return;
    }
    self.s[self.n as usize] = s;
    self.n += 1;
}

unsafe fn step(clist: &mut List, c: i32, nlist: &mut List) {
    LIST_ID.fetch_add(1, Ordering::AcqRel);
    nlist.n = 0;
    for i in 0..clist.n {
        let s = clist.s[i as usize];
        if (*s).c == c {
            list_add_state(nlist, (*s).out);
        }
    }
}

unsafe fn rmatch(l1: &mut List, l2: &mut List, start: *mut State, s: &[u8]) -> bool {
    let clist = list_start(l1, start);
    let nlist = l2;
    for &byte in s.iter() {
        step(clist, i32::from(byte), nlist);
        std::mem::swap(clist, nlist);
    }
    list_is_match(clist);
}

fn main() {
    let psot : String = "a*(a+b)+";
    let start = post2nfa(&post);
}