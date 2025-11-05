// struct Node {
//     key: i32,
//     value: String,
//     left: *mut Node,
//     right: *mut Node,
// }

static mut NSTATE: AtomicI32 = AtomicI32::new(0);

unsafe fn foo(root: *mut Node, key: i32, value: &str) -> *mut Node {
    let mut stack: Node = (*value).inner_str;
}