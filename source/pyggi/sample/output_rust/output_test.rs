#[cfg(test)]
mod tests {
    use super::*;
    use std::ffi::CString;
    use std::{mem, ptr};

    /// Compile `pattern`, build an NFA, and run it on `text`.
    /// Returns `true` if the whole string matches.
    ///
    /// Safety: relies on many `unsafe extern "C"` C-style functions,
    /// so the call itself must be wrapped in `unsafe`.
    unsafe fn match_regex(pattern: &str, text: &str) -> bool {
        use libc::{c_char, c_ulong, malloc};

        /* ---------- compile pattern to postfix ---------- */
        let cpat = CString::new(pattern).unwrap();
        let post = re2post(cpat.as_ptr() as *mut c_char);
        assert!(
            !post.is_null(),
            "Pattern `{}` was rejected by re2post()",
            pattern
        );

        /* ---------- build NFA ---------- */
        let start = post2nfa(post);
        assert!(
            !start.is_null(),
            "post2nfa() failed on `{}`",
            pattern
        );

        /* ---------- prepare the working lists ---------- */
        // Allocate room for every State* in the global array l1 / l2
        let bytes = (nstate as usize * mem::size_of::<*mut State>()) as c_ulong;
        l1.s = malloc(bytes) as *mut *mut State;
        l2.s = malloc(bytes) as *mut *mut State;

        /* ---------- run the NFA ---------- */
        let clist = startlist(start, &mut l1); // initialise list with ε-closure
        let mut clist_ptr = clist;
        let mut nlist_ptr: *mut List = &mut l2;

        for &byte in text.as_bytes() {
            step(clist_ptr, byte as libc::c_int, nlist_ptr);
            ptr::swap(&mut clist_ptr, &mut nlist_ptr); // make n the current list
        }

        ismatch(clist_ptr) != 0
    }

    /// Helper that asserts every `yes` string matches and every `no` string fails.
    unsafe fn check(pattern: &str, yes: &[&str], no: &[&str]) {
        for s in yes {
            assert!(
                match_regex(pattern, s),
                "❌  `{}` should match `{}` but did not",
                pattern,
                s
            );
        }
        for s in no {
            assert!(
                !match_regex(pattern, s),
                "❌  `{}` should *not* match `{}` but did",
                pattern,
                s
            );
        }
    }

    /* -------------------------------------------------- */
    /*  Functional test cases                             */
    /* -------------------------------------------------- */

    /// Alternation (`|`) and Kleene-star (`*`)
    #[test]
    fn alternation_and_star() {
        unsafe {
            check(
                "a(b|c)*d",
                &["ad", "abd", "acd", "abbd", "abcbcd"],
                &["a", "abcdx", "ac", "bd"],
            );
        }
    }

    /// One-or-more repetition (`+`)
    #[test]
    fn plus_repetition() {
        unsafe {
            check(
                "ab+c",
                &["abc", "abbc", "abbbbbc"],
                &["ac", "ab", "a", "abcx"],
            );
        }
    }

    /// Kleene star on a grouped alternation
    #[test]
    fn star_on_group() {
        unsafe {
            check(
                "(a|b)*c",
                &["c", "ac", "bc", "abababc"],
                &["ab", "abcabc", "ca"],
            );
        }
    }

    /// Optional (`?`) combined with `+`
    #[test]
    fn optional_and_plus_mix() {
        unsafe {
            check(
                "a?b+c?",
                &["b", "bb", "ab", "abb", "bc", "bbc", "abc", "abbc"],
                &["a", "c", "ac", ""],
            );
        }
    }
}
