// struct Node {
//     key: i32,
//     value: String,
//     left: Option<Box<Node> >,
//     right: Option<Box<Node> >,
// }

fn main() {
    let node : Node = Node{
        key: 12,
        value: "razie",
        left: None,
        right: None
    }

    let b : i32 = node.key;
    // println(node.value);
}