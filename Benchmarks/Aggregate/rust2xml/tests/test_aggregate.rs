extern crate rust2xml;

use std::time::Instant;

#[cfg(test)]
mod tests {
    use rust2xml::output_b::aggregate;
    use std::time::Instant;
    
    #[allow(dead_code)] // This will prevent the warning for unused code
    fn run_with_timer<F: FnOnce()>(test_fn: F, test_name: &str) {
        let start = Instant::now();
        test_fn();
        // let duration = start.elapsed();
        // println!("{} runtime: {:.2?}", test_name, duration);
        let duration = start.elapsed().as_secs_f64();  // Get duration in seconds as a floating-point value
    println!("{} runtime: {:.4} seconds", test_name, duration);
    }

    #[test]
    fn test_aggregate_empty() {
        run_with_timer(|| {
            let result = aggregate(&[]);
            assert_eq!(result, vec![]);
        }, "test_aggregate_empty");
    }

    #[test]
    fn test_aggregate_natnum() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3, 4, 5]);
            assert_eq!(result, vec![3, 7, 5]);
        }, "test_aggregate_natnum");
    }

    #[test]
    fn test_aggregate_even_num() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3, 4]);
            assert_eq!(result, vec![3, 7]);
        }, "test_aggregate_even_num");
    }

    #[test]
    fn test_aggregate_single_element() {
        run_with_timer(|| {
            let result = aggregate(&[5]);
            assert_eq!(result, vec![5]);
        }, "test_aggregate_single_element");
    }

    #[test]
    fn test_aggregate_all_same_elements() {
        run_with_timer(|| {
            let result = aggregate(&[2, 2, 2, 2]);
            assert_eq!(result, vec![4, 4]);
        }, "test_aggregate_all_same_elements");
    }

    #[test]
    fn test_aggregate_negative_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[-1, -2, -3, -4]);
            assert_eq!(result, vec![-3, -7]);
        }, "test_aggregate_negative_numbers");
    }

    #[test]
    fn test_aggregate_mixed_pos_neg() {
        run_with_timer(|| {
            let result = aggregate(&[1, -2, 3, -4]);
            assert_eq!(result, vec![-1, -1]);
        }, "test_aggregate_mixed_pos_neg");
    }

    #[test]
    fn test_aggregate_zeroes() {
        run_with_timer(|| {
            let result = aggregate(&[0, 0, 0, 0]);
            assert_eq!(result, vec![0, 0]);
        }, "test_aggregate_zeroes");
    }

    #[test]
    fn test_aggregate_large_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[1000, 2000, 3000, 4000]);
            assert_eq!(result, vec![3000, 7000]);
        }, "test_aggregate_large_numbers");
    }

    #[test]
    fn test_aggregate_alternating_pos_neg() {
        run_with_timer(|| {
            let result = aggregate(&[10, -10, 20, -20, 30]);
            assert_eq!(result, vec![0, 0, 30]);
        }, "test_aggregate_alternating_pos_neg");
    }

    #[test]
    fn test_aggregate_max_integers() {
        run_with_timer(|| {
            let result = aggregate(&[1073741823, 1073741823, 1073741823, 1073741823]);  
            assert_eq!(result, vec![2147483646, 2147483646]);  
        }, "test_aggregate_max_integers");
    }

    #[test]
    fn test_aggregate_increasing_sequence() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3, 4, 5, 6]);
            assert_eq!(result, vec![3, 7, 11]);
        }, "test_aggregate_increasing_sequence");
    }

    #[test]
    fn test_aggregate_decreasing_sequence() {
        run_with_timer(|| {
            let result = aggregate(&[6, 5, 4, 3, 2, 1]);
            assert_eq!(result, vec![11, 7, 3]);
        }, "test_aggregate_decreasing_sequence");
    }

    #[test]
    fn test_aggregate_single_pair() {
        run_with_timer(|| {
            let result = aggregate(&[7, 8]);
            assert_eq!(result, vec![15]);
        }, "test_aggregate_single_pair");
    }

    #[test]
    fn test_aggregate_large_sequential() {
        run_with_timer(|| {
            let range: Vec<i32> = (1..=100).collect();
            let result = aggregate(&range);
            let expected: Vec<i32> = (1..=100)
                .step_by(2)
                .zip((2..=101).step_by(2))
                .map(|(a, b)| a + b)
                .collect();
            assert_eq!(result, expected);
        }, "test_aggregate_large_sequential");
    }

    #[test]
    fn test_aggregate_alternating_large_negatives() {
        run_with_timer(|| {
            let result = aggregate(&[1000, -100000, 2000, -200000]);
            assert_eq!(result, vec![-99000, -198000]);
        }, "test_aggregate_alternating_large_negatives");
    }

    #[test]
    fn test_aggregate_two_elements() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2]);
            assert_eq!(result, vec![3]);
        }, "test_aggregate_two_elements");
    }

    #[test]
    fn test_aggregate_three_elements() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3]);
            assert_eq!(result, vec![3, 3]);
        }, "test_aggregate_three_elements");
    }

    #[test]
    fn test_aggregate_four_elements() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3, 4]);
            assert_eq!(result, vec![3, 7]);
        }, "test_aggregate_four_elements");
    }

    #[test]
    fn test_aggregate_five_elements() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3, 4, 5]);
            assert_eq!(result, vec![3, 7, 5]);
        }, "test_aggregate_five_elements");
    }

    #[test]
    fn test_aggregate_six_elements() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3, 4, 5, 6]);
            assert_eq!(result, vec![3, 7, 11]);
        }, "test_aggregate_six_elements");
    }

    #[test]
    fn test_aggregate_seven_elements() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 3, 4, 5, 6, 7]);
            assert_eq!(result, vec![3, 7, 11, 7]);
        }, "test_aggregate_seven_elements");
    }

    #[test]
    fn test_aggregate_alternating_ones_zeros() {
        run_with_timer(|| {
            let result = aggregate(&[1, 0, 1, 0, 1, 0]);
            assert_eq!(result, vec![1, 1, 1]);
        }, "test_aggregate_alternating_ones_zeros");
    }

    #[test]
    fn test_aggregate_large_multiples_of_10() {
        run_with_timer(|| {
            let result = aggregate(&[100, 200, 300, 400, 500, 600]);
            assert_eq!(result, vec![300, 700, 1100]);
        }, "test_aggregate_large_multiples_of_10");
    }

    #[test]
    fn test_aggregate_large_multiples_of_5() {
        run_with_timer(|| {
            let result = aggregate(&[5, 10, 15, 20, 25, 30]);
            assert_eq!(result, vec![15, 35, 55]);
        }, "test_aggregate_large_multiples_of_5");
    }

    #[test]
    fn test_aggregate_mixed_positive_and_negative() {
        run_with_timer(|| {
            let result = aggregate(&[10, -10, 20, -20, 30]);
            assert_eq!(result, vec![0, 0, 30]);
        }, "test_aggregate_mixed_positive_and_negative");
    }

    #[test]
    fn test_aggregate_large_negative_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[-100000, -200000, -300000, -400000, -500000, -600000]);
            assert_eq!(result, vec![-300000, -700000, -1100000]);
        }, "test_aggregate_large_negative_numbers");
    }

    #[test]
    fn test_aggregate_large_positive_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[100000, 200000, 300000, 400000, 500000, 600000]);
            assert_eq!(result, vec![300000, 700000, 1100000]);
        }, "test_aggregate_large_positive_numbers");
    }

    #[test]
    fn test_aggregate_powers_of_two() {
        run_with_timer(|| {
            let result = aggregate(&[1, 2, 4, 8, 16, 32, 64, 128]);
            assert_eq!(result, vec![3, 12, 48, 192]);
        }, "test_aggregate_powers_of_two");
    }

    #[test]
    fn test_aggregate_alternating_pos_neg_small() {
        run_with_timer(|| {
            let result = aggregate(&[5, -5, 10, -10, 15]);
            assert_eq!(result, vec![0, 0, 15]);
        }, "test_aggregate_alternating_pos_neg_small");
    }

    #[test]
    fn test_aggregate_max_positive_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[1073741823, 1073741823, 1073741823, 1073741823]);
            assert_eq!(result, vec![2147483646, 2147483646]);
        }, "test_aggregate_max_positive_numbers");
    }

    #[test]
    fn test_aggregate_max_negative_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[-1073741823, -1073741823, -1073741823, -1073741823]);
            assert_eq!(result, vec![-2147483646, -2147483646]);
        }, "test_aggregate_max_negative_numbers");
    }

    #[test]
    fn test_aggregate_mixed_large_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[500000000, -500000000, 1000000000, -1000000000]);
            assert_eq!(result, vec![0, 0]);
        }, "test_aggregate_mixed_large_numbers");
    }

    #[test]
    fn test_aggregate_large_sequence_of_consecutive_integers() {
        run_with_timer(|| {
            let range: Vec<i32> = (1..=50).collect();
            let result = aggregate(&range);
            let expected: Vec<i32> = (1..=50)
                .step_by(2)
                .zip((2..=51).step_by(2))
                .map(|(a, b)| a + b)
                .collect();
            assert_eq!(result, expected);
        }, "test_aggregate_large_sequence_of_consecutive_integers");
    }

    #[test]
    fn test_aggregate_small_negative_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[-1, -2, -3, -4, -5]);
            assert_eq!(result, vec![-3, -7, -5]);
        }, "test_aggregate_small_negative_numbers");
    }

    #[test]
    fn test_aggregate_only_zeroes() {
        run_with_timer(|| {
            let result = aggregate(&[0, 0, 0, 0, 0]);
            assert_eq!(result, vec![0, 0, 0]);
        }, "test_aggregate_only_zeroes");
    }

    #[test]
    fn test_aggregate_two_large_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[1000000000, 1000000000]);
            assert_eq!(result, vec![2000000000]);
        }, "test_aggregate_two_large_numbers");
    }

    #[test]
    fn test_aggregate_all_zeroes() {
        run_with_timer(|| {
            let result = aggregate(&[0, 0, 0, 0, 0, 0]);
            assert_eq!(result, vec![0, 0, 0]);
        }, "test_aggregate_all_zeroes");
    }

    #[test]
    fn test_aggregate_floating_point_like_values() {
        run_with_timer(|| {
            let result = aggregate(&[1, 3, 2, 4, 3, 5, 4, 6]);
            assert_eq!(result, vec![4, 6, 8, 10]);
        }, "test_aggregate_floating_point_like_values");
    }

    #[test]
    fn test_aggregate_repeating_increasing_numbers() {
        run_with_timer(|| {
            let result = aggregate(&[1, 1, 2, 2, 3, 3, 4, 4, 5, 5]);
            assert_eq!(result, vec![2, 4, 6, 8, 10]);
        }, "test_aggregate_repeating_increasing_numbers");
    }

    #[test]
    fn test_aggregate_two_identical_elements() {
        run_with_timer(|| {
            let result = aggregate(&[42, 42]);
            assert_eq!(result, vec![84]);
        }, "test_aggregate_two_identical_elements");
    }

    #[test]
    fn test_aggregate_two_identical_negative_elements() {
        run_with_timer(|| {
            let result = aggregate(&[-42, -42]);
            assert_eq!(result, vec![-84]);
        }, "test_aggregate_two_identical_negative_elements");
    }

    #[test]
    fn test_aggregate_negative_and_zero() {
        run_with_timer(|| {
            let result = aggregate(&[-42, 0, -42, 0]);
            assert_eq!(result, vec![-42, -42]);
        }, "test_aggregate_negative_and_zero");
    }

    #[test]
    fn test_aggregate_single_negative_and_zero() {
        run_with_timer(|| {
            let result = aggregate(&[-42, 0]);
            assert_eq!(result, vec![-42]);
        }, "test_aggregate_single_negative_and_zero");
    }

    #[test]
    fn test_aggregate_with_mostly_zeroes() {
        run_with_timer(|| {
            let result = aggregate(&[0, 0, 0, 0, 42]);
            assert_eq!(result, vec![0, 0, 42]);
        }, "test_aggregate_with_mostly_zeroes");
    }
}

