// easy for debugging / knowing what is inside
#[derive(Debug)]
struct node {
    key: i32,
    value: String,
    left: Option<box<node> >,
    right: Option<box<node> >,
}

impl node {
    fn new(key: i32, value: String) -> Self {
        node {
            key,
            value,
            left: None,
            right: None,
        }
    }

    // looks like box is helpful here
    fn insert(&mut self, key: i32, value: String) {
        if key < self.key {
            if let some(ref mut left) = self.left {
                left.insert(key, value);
            } else {
                self.left = some(box::new(node::new(key, value)));
            }
        } else if key > self.key {
            if let some(ref mut right) = self.right {
                right.insert(key, value);
            } else {
                self.right = some(box::new(node::new(key, value)));
            }
        } else {
            self.value = value;
        }
    }

    // self.left is owned by current function
    // but looks like left in some(ref mut left) is something can be passed to other functions
    fn search(&mut self, key: i32) -> Option<&String> {
        if key < self.key {
            if let some(ref mut left) = self.left {
                return left.search(key);
            } else {
                return None;
            }
        } else if key > self.key {
            if let some(ref mut right) = self.right {
                return right.search(key);
            } else {
                return None;
            }
        } else {
            return some(&self.value);
        }
    }
}

// added issue:
// static mut buf: [libc::c_char; 8000] = [0; 8000];

// added issue: argument
fn main() {
    let mut root = node::new(5, String::from("five"));

    // added issue: argument
    let mut dst: *mut libc::c_int = 0;

    // println!("{:?}", root.search(5));
    // println!("{:?}", root.search(3));
    // root.insert(3, String::from("three"));
    // println!("{:?}", root.search(3));
    // println!("{:?}", root.search(7));
    // root.insert(7, String::from("seven"));
    // println!("{:?}", root.search(7));
    // println!("{:?}", root.search(4));
    // root.insert(4, String::from("four"));
    // println!("{:?}", root.search(4));
    // println!("{:?}", root.search(2));
    // root.insert(2, String::from("two"));
    // println!("{:?}", root.search(2));
    // println!("{:?}", root.search(6));
    // root.insert(6, String::from("six"));
    // println!("{:?}", root.search(6));
    // println!("{:?}", root.search(8));
    // root.insert(8, String::from("eight"));
    // println!("{:?}", root.search(8));
    // println!("{:?}", root);
}