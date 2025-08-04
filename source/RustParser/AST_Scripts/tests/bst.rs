// // easy for debugging / knowing what is inside
// #[derive(Debug)]
// struct Node {
//     key: i32,
//     value: String,
//     left: Option<Box<Node> >,
//     right: Option<Box<Node> >,
// }

// impl Node {
//     fn new(key: i32, value: String) -> Self {
//         Node {
//             key,
//             value,
//             left: None,
//             right: None,
//         }
//     }

//     // looks like Box is helpful here
//     fn insert(&mut self, key: i32, value: String) {
//         if key < self.key {
//             if let Some(ref mut left) = self.left {
//                 left.insert(key, value);
//             } else {
//                 self.left = Some(Box::new(Node::new(key, value)));
//             }
//         } else if key > self.key {
//             if let Some(ref mut right) = self.right {
//                 right.insert(key, value);
//             } else {
//                 self.right = Some(Box::new(Node::new(key, value)));
//             }
//         } else {
//             self.value = value;
//         }
//     }

//     // self.left is owned by current function
//     // but looks like left in Some(ref mut left) is something can be passed to other functions
//     fn search(&mut self, key: i32) -> Option<&String> {
//         if key < self.key {
//             if let Some(ref mut left) = self.left {
//                 return left.search(key);
//             } else {
//                 return None;
//             }
//         } else if key > self.key {
//             if let Some(ref mut right) = self.right {
//                 return right.search(key);
//             } else {
//                 return None;
//             }
//         } else {
//             return Some(&self.value);
//         }
//     }
// }

fn main() {
    let a : i32 = 1;
    pub struct List {
        pub s: *mut *mut State,
        pub n: libc::c_int,
    }
    let ptr : String = "Razie";
    let val = *ptr;
}