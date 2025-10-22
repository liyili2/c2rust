
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