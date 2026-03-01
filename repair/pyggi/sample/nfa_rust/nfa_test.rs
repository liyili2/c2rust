#[cfg(test)]
mod tests {
    use super::*;

    fn match_regex(pattern: &str, input: &str) -> bool {
        let post = re2post(pattern.as_bytes()).expect("invalid pattern");
        let start = post2nfa(&post);
        assert!(!start.is_null());

        let nstate = NSTATE.load(Ordering::Acquire) as usize;
        let mut l1 = List { s: vec![std::ptr::null_mut(); nstate].into_boxed_slice(), n: 0 };
        let mut l2 = List { s: vec![std::ptr::null_mut(); nstate].into_boxed_slice(), n: 0 };
        unsafe { rmatch(&mut l1, &mut l2, start, input.as_bytes()) }
    }

    #[test]
    fn test_literal_match() {
        assert!(match_regex("abc", "abc"));
        assert!(!match_regex("abc", "ab"));
    }

    #[test]
    fn test_alternation() {
        assert!(match_regex("a|b", "a"));
        assert!(match_regex("a|b", "b"));
        assert!(!match_regex("a|b", "c"));
    }

    #[test]
    fn test_kleene_star() {
        assert!(match_regex("a*", ""));
        assert!(match_regex("a*", "aaaa"));
        assert!(!match_regex("a*", "aaab"));
    }

    #[test]
    fn test_concatenation_and_plus() {
        assert!(match_regex("ab+c", "abc"));
        assert!(match_regex("ab+c", "abbbc"));
        assert!(!match_regex("ab+c", "ac"));
    }
}
