const MATCH: i32 = 256;
const SPLIT: i32 = 257;

struct State {
    c: i32,
    out: *mut State,
    out1: *mut State,
    lastlist: i32,
}

static NSTATE: AtomicI32 = AtomicI32::new(0);

static mut MATCH_STATE: State =
    State { c: MATCH, lastlist: 0 };

struct Frag {
    start: *mut State,
    out: *mut PtrList,
}

struct PtrList {
    next: *mut PtrList,
    s: *mut State,
}

unsafe fn PtrList_list1(outp: *mut *mut State) -> *mut PtrList {
    let l = outp.cast::<PtrList> ();
    return l;
}

unsafe fn PtrList_patch(mut l: *mut PtrList, s: *mut State) {
    while !l.is_null() {
        let next = (*l).next;
        (*l).s = s;
        l = next;
    }
}

unsafe fn PtrList_append(mut l1: *mut PtrList, l2: *mut PtrList) -> *mut PtrList {
    let oldl1: *mut PtrList = l1;
    while (*l1).next != None {
        l1 = (*l1).next;
    }
    (*l1).next = l2;
}

fn main() {
    let mut s1 = State { c: 'a' as i32, lastlist: 0 };
    let mut s2 = State { c: 'b' as i32, lastlist: 0 };
    let s3 = State{c: 'c' as i32, out: &mut s1, out1: &mut s2};

    println!("Created {} states", NSTATE.load(Ordering::Relaxed));

    let mut outp: *mut State = s3;
    let list1 = PtrList_list1(&mut outp);
    // PtrList_patch(list1, s3);
    // let list2 = PtrList_list1(&mut outp);
    // let combined = PtrList_append(list1, list2);
    // let frag = Frag{start: s3, out: combined};
}