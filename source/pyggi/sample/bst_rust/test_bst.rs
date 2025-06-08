#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_insert_and_search_single_node() {
        let mut root = Node::new(10, "Root".to_string());
        assert_eq!(root.search(10), Some(&"Root".to_string()));
    }

    #[test]
    fn test_insert_and_search_multiple_nodes() {
        let mut root = Node::new(10, "Root".to_string());
        root.insert(5, "Left".to_string());
        root.insert(15, "Right".to_string());

        assert_eq!(root.search(5), Some(&"Left".to_string()));
        assert_eq!(root.search(15), Some(&"Right".to_string()));
    }

    #[test]
    fn test_update_existing_key() {
        let mut root = Node::new(10, "Root".to_string());
        root.insert(10, "Updated Root".to_string());

        assert_eq!(root.search(10), Some(&"Updated Root".to_string()));
    }

    #[test]
    fn test_search_nonexistent_key() {
        let mut root = Node::new(10, "Root".to_string());
        root.insert(5, "Left".to_string());
        root.insert(15, "Right".to_string());

        assert_eq!(root.search(100), None);
    }

    #[test]
    fn test_deep_insertion_and_search() {
        let mut root = Node::new(50, "Root".to_string());
        let keys = vec![25, 75, 10, 30, 60, 90];
        for &k in &keys {
            root.insert(k, format!("Value {}", k));
        }

        for &k in &keys {
            assert_eq!(root.search(k), Some(&format!("Value {}", k)));
        }
    }
}
