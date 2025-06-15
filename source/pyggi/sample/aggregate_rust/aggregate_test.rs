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
        let input = [-1, -2, -3, -4];
        let expected = vec![-3, -7];
        assert_eq!(aggregate(&input), expected);
    }
}