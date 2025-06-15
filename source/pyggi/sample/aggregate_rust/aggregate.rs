fn aggregate(list: &[i32]) -> Vec<i32> {
    let len = list.len();
    let mut ret = vec![0; (len >> 1) + (len & 0b0001)];
    for i in 0..len {
        if i % 2 == 1 {
            ret[i / 2] += list[i];
        } else {
            ret[i / 2] = list[i];
        }
    }
    ret
}

fn printall(list: &[i32]) {
    print!("[");
    for i in 0..list.len() {
        print!("{}, ", list[i]);
    }
    println!("]");
}

fn main() {
    let test1: [i32; 6] = [1, 2, 3, 4, 5, 6];
    let ret1 = aggregate(&test1);
    printall(&test1);
    printall(&ret1);

    let test2: [i32; 5] = [1, 2, 3, 4, 5];
    let ret2 = aggregate(&test2);
    printall(&test2);
    printall(&ret2);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_even_length_list() {
        let input = [1, 2, 3, 4, 5, 6];
        let expected = vec![3, 7, 11];
        assert_eq!(aggregate(&input), expected);
    }

    #[test]
    fn test_odd_length_list() {
        let input = [1, 2, 3, 4, 5];
        let expected = vec![3, 7, 5];
        assert_eq!(aggregate(&input), expected);
    }

    #[test]
    fn test_empty_list() {
        let input: [i32; 0] = [];
        let expected: Vec<i32> = vec![];
        assert_eq!(aggregate(&input), expected);
    }

    #[test]
    fn test_single_element() {
        let input = [42];
        let expected = vec![42];
        assert_eq!(aggregate(&input), expected);
    }

    #[test]
    fn test_two_elements() {
        let input = [10, 5];
        let expected = vec![15];
        assert_eq!(aggregate(&input), expected);
    }

    #[test]
    fn test_negatives() {
        let input =[-1, -2, -3, -4];
        let expected = vec![-3, -7];
        assert_eq!(aggregate(&input), expected);
    }
}
