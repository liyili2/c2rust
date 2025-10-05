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

unsafe fn insert(root: *mut Node, key: i32, value: &str) {
    if root == None {
        return;
    }
    if key < (*root).key {
        if (*root).left == None {
            (*root).left = new_node(key, value);
        } else {
            insert((*root).left, key, value);
        }
    } 
    else if key > (*root).key {
        if (*root).right == None {
            (*root).right = new_node(key, value);
        } else {
            insert((*root).right, key, value);
        }
    } else {
        o(*rot).value = value.to_string();
    }
}

unsafe fn search(root: *mut Node, key: i32) -> *const String {
    let return_val = "None";
    if root == None {
        return return_val;
    }

    if key == (*root).key {
        return_val = root.value;
    }

    if key < (*root).key {
        return_val = search((*root).left, key);
    }

    if key > (*root).key {
        return_val = search((*root).right, key);
    }

    return return_val;
}

fn main() {
    unsafe {
        let root = new_node(5, "five");
        let five_found = search(root, 5);
        let three_found = search(root, 3);
        // insert(root, 3, "three");
        // search(root, 3);
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
