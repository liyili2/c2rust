// // // easy for debugging / knowing what is inside
// #[derive(Debug)]
// struct Node {
//     key: i32,
//     value: string,
//     left: Option<Box<Node> >,
//     right: Option<Box<Node> >,
// }

// unsafe unsafeTopLevelVarDef: i32 = 11;

// impl Node {
//     unsafe fn new(key: i32, value: string) -> Self {
//         Node {
//             key,
//             value,
//             left: None,
//             right: None,
//         }
//     }

//     // looks like Box is helpful here
//     fn insert() {
//         if key < self.key {
//             if let some(ref mut left) = self.left {
//                 left.insert(key, value);
//             }
//             else {
//                 self.left = some(box::new(Node::new(key, value) ) );
//             }
//         }
//         else if key > self.key {
//             if let some(ref mut right) = self.right {
//                 right.insert(key, value);
//             } 
//         else {
//                 self.right = some(box::new(Node::new(key, value) ) );
//             }
//         } else {
//             self.value = value;
//         }
//     }

//     // self.left is owned by current function
//     // but looks like left in Some(ref mut left) is something can be passed to other functions
//     fn search(&mut self, key: i32) -> Option<&string> {
//         if key < self.key {
//             if let some(ref mut left) = self.left {
//                 return left.search(key);
//             } else {
//                 return None;
//             }
//         } else if key > self.key {
//             if let some(ref mut right) = self.right {
//                 return right.search(key);
//             } else {
//                 return None;
//             }
//         } else {
//             return some(&self.value);
//         }
//     }
// }

// impl Node {
//     fn foo() {
//         let a : i32 = 0;
//         a = 12;
//         while a {
//             print("hello!");
//         }
//     }
// }

// fn foo(mut argv: *mut *mut libc::c_char, mut argv2: *mut *mut libc::c_int, mut argv3: *mut *mut libc::c_int) {

// }

// fn main(mut argv: *mut *mut libc::c_char, mut argv2: *mut *mut libc::c_int, mut argv3: *mut *mut libc::c_int) {

fn main() {
//     let a: *mut libc::c_char = "googoolii";
    // let a: i32 = "1";
    // let s : i32 = 1;
    // s += 13;
    // println!("{}", s);
    // let a : i32 = 0;
    // let b : i32 = 1;
    // a = 12;
    // while a {
    //     print("hello!");
    // }
    // a = b.val;
    // let a : i32 = 11;
    // if a {
    //     print("hello")
    // }
    // let a : aa::bb::cc = 1 as bb;
    unsafe {
        // let mut root = Node::new(5, string::from("five") );
        let a: i32 = 1;
        a = 22;
    }
    // let a : i32 = unsafe{22};
    // println!("{:?}", root.search(5));
    // println!("{:?}", root.search(3));
    // root.insert(3, string::from("three"));
    // println!("{:?}", root.search(3));
    // println!("{:?}", root.search(7));
    // root.insert(7, string::from("seven"));
    // println!("{:?}", root.search(7));
    // println!("{:?}", root.search(4));
    // root.insert(4, string::from("four"));
    // println!("{:?}", root.search(4));
    // println!("{:?}", root.search(2));
    // root.insert(2, string::from("two"));
    // println!("{:?}", root.search(2));
    // println!("{:?}", root.search(6));
    // root.insert(6, string::from("six"));
    // println!("{:?}", root.search(6));
    // println!("{:?}", root.search(8));
    // root.insert(8, string::from("eight"));
    // println!("{:?}", root.search(8));
    // println!("{:?}", root);
}

// static mut listid0: libc::c_int = 0;
// static mut listid1: libc::c_int = 1;
// static mut listid2: libc::c_int = 2;

// fn main() {
//     let mut dst: *mut libc::c_char = 0 as *mut libc::c_char;
//     let a = 2;
//     a = 44;
//     let mut dst : Option<NonNull<libc::c_char>> = None;
//     let mut dst: Option<NonNull<libc::c_char> > = None;
//     let mut dst: i32 = 1;
// }