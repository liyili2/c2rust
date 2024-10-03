fn aggregate(list: &[i32]) -> Vec<i32> {
    let len = list.len();
    // the size of the result array is not known until runtime
    // using vec is unavoidable
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
    fn test_aggregate_empty() {
        let result = aggregate(&[]);
        assert_eq!(result, vec![]);
    }

    #[test]
    fn test_aggregate_natnum() {
        let result = aggregate(&[1, 2, 3, 4, 5]);
        assert_eq!(result, vec![3, 7, 5]);
    }

    #[test]
    fn test_aggregate_even_num() {
        let result = aggregate(&[1, 2, 3, 4]);
        assert_eq!(result, vec![3, 7]);
    }

    #[test]
    fn test_aggregate_single_element() {
        let result = aggregate(&[5]);
        assert_eq!(result, vec![5]);
    }

    #[test]
    fn test_aggregate_all_same_elements() {
        let result = aggregate(&[2, 2, 2, 2]);
        assert_eq!(result, vec![4, 4]);
    }

    #[test]
    fn test_aggregate_negative_numbers() {
        let result = aggregate(&[-1, -2, -3, -4]);
        assert_eq!(result, vec![-3, -7]);
    }

    #[test]
    fn test_aggregate_mixed_pos_neg() {
        let result = aggregate(&[1, -2, 3, -4]);
        assert_eq!(result, vec![-1, -1]);
    }

    #[test]
    fn test_aggregate_zeroes() {
        let result = aggregate(&[0, 0, 0, 0]);
        assert_eq!(result, vec![0, 0]);
    }

    #[test]
    fn test_aggregate_large_numbers() {
        let result = aggregate(&[1000, 2000, 3000, 4000]);
        assert_eq!(result, vec![3000, 7000]);
    }

    #[test]
    fn test_aggregate_alternating_pos_neg() {
        let result = aggregate(&[10, -10, 20, -20, 30]);
        assert_eq!(result, vec![0, 0, 30]);
    }

    #[test]
    fn test_aggregate_max_integers() {
        let result = aggregate(&[2147483647, 2147483647, 2147483647, 2147483647]);
        assert_eq!(result, vec![4294967294, 4294967294]);
    }

    #[test]
    fn test_aggregate_increasing_sequence() {
        let result = aggregate(&[1, 2, 3, 4, 5, 6]);
        assert_eq!(result, vec![3, 7, 11]);
    }

    #[test]
    fn test_aggregate_decreasing_sequence() {
        let result = aggregate(&[6, 5, 4, 3, 2, 1]);
        assert_eq!(result, vec![11, 7, 3]);
    }

    #[test]
    fn test_aggregate_single_pair() {
        let result = aggregate(&[7, 8]);
        assert_eq!(result, vec![15]);
    }

    #[test]
    fn test_aggregate_large_sequential() {
        let range: Vec<i32> = (1..=100).collect();
        let result = aggregate(&range);
        let expected: Vec<i32> = (1..=100)
            .step_by(2)
            .zip((2..=101).step_by(2))
            .map(|(a, b)| a + b)
            .collect();
        assert_eq!(result, expected);
    }

    #[test]
    fn test_aggregate_alternating_large_negatives() {
        let result = aggregate(&[1000, -100000, 2000, -200000]);
        assert_eq!(result, vec![-99000, -198000]);
    }
}

