// easy for debugging / knowing what is inside
#[derive(Debug)]
struct Node {
    key: i32,
    value: String,
    left: Option<Box<Node> >,
    right: Option<Box<Node> >,
}

impl Node {
    fn new(key: i32, value: String) -> Self {
        Node {
            key,
            value,
            left: None,
            right: None,
        }
    }

    // looks like Box is helpful here
    fn insert(&mut self, key: i32, value: String) {
        if key < self.key {
            if let Some(ref mut left) = self.left {
                left.insert(key, value);
            } else {
                self.left = Some(Box::new(Node::new(key, value)));
            }
        } else if key > self.key {
            if let Some(ref mut right) = self.right {
                right.insert(key, value);
            } else {
                self.right = Some(Box::new(Node::new(key, value)));
            }
        } else {
            self.value = value;
        }
    }

    // self.left is owned by current function
    // but looks like left in Some(ref mut left) is something can be passed to other functions
    fn search(&mut self, key: i32) -> Option<&String> {
        if key < self.key {
            if let Some(ref mut left) = self.left {
                return left.search(key);
            } else {
                return None;
            }
        } else if key > self.key {
            if let Some(ref mut right) = self.right {
                return right.search(key);
            } else {
                return None;
            }
        } else {
            return Some(&self.value);
        }
    }
}

fn main() {
    // let mut root = Node::new(5, String::from("five"));
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