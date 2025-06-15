#[derive(Debug)]
pub struct Node {
    key: i32,
    value: String,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

impl Node {
    pub fn new(key: i32, value: String) -> Self {
        Node {
            key,
            value,
            left: None,
            right: None,
        }
    }

    pub fn insert(&mut self, key: i32, value: String) {
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

    pub fn search(&self, key: i32) -> Option<&String> {
        if key < self.key {
            if let Some(ref left) = self.left {
                left.search(key)
            } else {
                None
            }
        } else if key > self.key {
            if let Some(ref right) = self.right {
                right.search(key)
            } else {
                None
            }
        } else {
            Some(&self.value)
        }
    }
}

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
