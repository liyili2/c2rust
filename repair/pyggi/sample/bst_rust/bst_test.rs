#[test]
fn test_insert_and_search_exact() {
    let mut root = Node::new(10, "ten".to_string());
    root.insert(5, "five".to_string());
    root.insert(15, "fifteen".to_string());

    assert_eq!(root.search(10), Some(&"ten".to_string()));
    assert_eq!(root.search(5), Some(&"five".to_string()));
    assert_eq!(root.search(15), Some(&"fifteen".to_string()));
}

#[test]
fn test_search_nonexistent() {
    let mut root = Node::new(10, "ten".to_string());
    root.insert(5, "five".to_string());

    assert_eq!(root.search(99), None);
    assert_eq!(root.search(0), None);
}

#[test]
fn test_update_existing_key() {
    let mut root = Node::new(10, "ten".to_string());
    root.insert(10, "TEN updated".to_string());

    assert_eq!(root.search(10), Some(&"TEN updated".to_string()));
}

#[test]
fn test_deep_tree_search() {
    let mut root = Node::new(50, "root".to_string());
    root.insert(30, "left".to_string());
    root.insert(70, "right".to_string());
    root.insert(20, "left-left".to_string());
    root.insert(40, "left-right".to_string());
    root.insert(60, "right-left".to_string());
    root.insert(80, "right-right".to_string());

    assert_eq!(root.search(20), Some(&"left-left".to_string()));
    assert_eq!(root.search(40), Some(&"left-right".to_string()));
    assert_eq!(root.search(60), Some(&"right-left".to_string()));
    assert_eq!(root.search(80), Some(&"right-right".to_string()));
}
