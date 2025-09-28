#[derive(Debug)]
struct Node {
    key: i32,
    value: String,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
    parent_ptr: *mut Node, // raw pointer to parent node
}

// static mutable counter of nodes (example of global unsafe variable)
static mut NODE_COUNT: i32 = 0;

impl Node {
    fn new(key: i32, value: String) -> Self {
        unsafe { NODE_COUNT += 1; } // increment global counter
        Node {
            key,
            value,
            left: None,
            right: None,
            parent_ptr: std::ptr::null_mut(), // initially null
        }
    }

    fn insert(&mut self, key: i32, value: String) {
        if key < self.key {
            if let Some(ref mut left) = self.left {
                // update parent_ptr for child
                unsafe { left.parent_ptr = self; }
                left.insert(key, value);
            } else {
                let mut new_node = Box::new(Node::new(key, value));
                unsafe { new_node.parent_ptr = self; } // set raw pointer to parent
                self.left = Some(new_node);
            }
        } else if key > self.key {
            if let Some(ref mut right) = self.right {
                unsafe { right.parent_ptr = self; }
                right.insert(key, value);
            } else {
                let mut new_node = Box::new(Node::new(key, value));
                unsafe { new_node.parent_ptr = self; }
                self.right = Some(new_node);
            }
        } else {
            self.value = value;
        }
    }

    fn search(&mut self, key: i32) -> Option<&String> {
        if key < self.key {
            if let Some(ref mut left) = self.left {
                left.search(key)
            } else {
                None
            }
        } else if key > self.key {
            if let Some(ref mut right) = self.right {
                right.search(key)
            } else {
                None
            }
        } else {
            // unsafe raw pointer dereference example
            unsafe {
                if !self.parent_ptr.is_null() {
                    println!("Parent key (via raw pointer): {}", (*self.parent_ptr).key);
                }
            }
            Some(&self.value)
        }
    }
}

fn main() {
    let mut root = Node::new(5, String::from("five"));

    println!("{:?}", root.search(5));
    root.insert(3, String::from("three"));
    println!("{:?}", root.search(3));
    root.insert(7, String::from("seven"));
    println!("{:?}", root.search(7));
    root.insert(4, String::from("four"));
    println!("{:?}", root.search(4));
    root.insert(2, String::from("two"));
    println!("{:?}", root.search(2));
    root.insert(6, String::from("six"));
    println!("{:?}", root.search(6));
    root.insert(8, String::from("eight"));
    println!("{:?}", root.search(8));

    unsafe {
        println!("Total nodes (via static mutable global): {}", NODE_COUNT);
    }
}
