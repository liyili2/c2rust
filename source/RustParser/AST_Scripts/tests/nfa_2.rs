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
    State { c: MATCH, out: null_mut(), out1: null_mut(), lastlist: 0 };

impl State {
    fn new(c: i32, out: *mut State, out1: *mut State) -> *mut State {
        NSTATE.fetch_add(1, Ordering::AcqRel);
        let state = Box::new(State { c, out, out1, lastlist: 0 });
        Box::into_raw(state);
    }
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

impl PtrList {
    unsafe fn list1(outp: *mut *mut State) -> *mut PtrList {
        let l = outp.cast::<PtrList> ();
        (*l).next = null_mut();
    }

    unsafe fn patch(mut l: *mut PtrList, s: *mut State) {
        while !l.is_null() {
            let next = (*l).next;
            (*l).s = s;
            l = next;
        }
    }

    unsafe fn append(mut l1: *mut PtrList, l2: *mut PtrList) -> *mut PtrList {
        let oldl1: *mut PtrList = l1;
        while !(*l1).next.is_null() {
            l1 = (*l1).next;
        }
        (*l1).next = l2;
    }
}


fn main() {


}