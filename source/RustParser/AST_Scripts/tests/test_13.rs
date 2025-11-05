struct Node {
    key: i32,
    value: String,
    left: *mut Node,
    right: *mut Node,
}

static mut NSTATE: AtomicI32 = AtomicI32::new(0);

unsafe fn insert(root: *mut Node, key: i32, value: &str) -> *mut Node {
    if root == None {
        return;
    }

    if key < (*root).key {
        if (*root).left == None {
            let n2 = new_node(key, value);
            (*root).left = n2;
        } else {
            root = insert((*root).left, key, value);
        }
    }
    else if key > (*root).key {
        if (*root).right == None {
            (*root).right = new_node(key, value);
        } else {
            root = insert((*root).right, key, value);
        }
    } else {
        (*root).value = value;
    }

    return root;
}