use std::ptr;

#[derive(Debug)]
struct Node {
    key: i32,
    value: String,
    left: *mut Node,
    right: *mut Node,
}

unsafe fn new_node(key: i32, value: &str) -> *mut Node {
    let n = Node {
        key: key,
        value: value,
        left: None,
        right: None,
    };
    return n;
}

unsafe fn insert(root: *mut Node, key: i32, value: &str) -> *mut Node {
    if root == None {
        return;
    }

    if key < root.as_Ref().unwrap().key {
        if root.as_Ref().unwrap().left == None {
            let n2 = new_node(key, value);
            root.as_Ref().unwrap().left = n2;
        } else {
            root = insert(root.as_Ref().unwrap().left, key, value);
        }
    }
    else if key > root.as_Ref().unwrap().key {
        if root.as_Ref().unwrap().right == None {
            root.as_Ref().unwrap().right = new_node(key, value);
        } else {
            root = insert(root.as_Ref().unwrap().right, key, value);
        }
    } else {
        root.as_Ref().unwrap().value = value;
    }

    return root;
}

unsafe fn search(root: *mut Node, key: i32) -> *const String {
    let return_val = "None";
    if root == None {
        return return_val;
    }

    if key == root.as_Ref().unwrap().key {
        return_val = root.value;
    }

    if key < root.as_Ref().unwrap().key {
        return_val = search(root.as_Ref().unwrap().left, key);
    }

    if key > root.as_Ref().unwrap().key {
        return_val = search(root.as_Ref().unwrap().right, key);
    }

    return return_val;
}

fn main() {
    unsafe {
        let root = new_node(3, "three");
        let three_found = search(root, 3);
        root = insert(root, 5, "five");
        let five_found = search(root, 5);
        // insert(root, 7, "seven");
        // search(root, 7);
        // insert(root, 4, "four");
        // search(root, 4);
        // insert(root, 2, "two");
        // search(root, 2);
        // insert(root, 6, "six");
        // search(root, 6);
        // insert(root, 8, "eight");
        // search(root, 8);
    }
}
