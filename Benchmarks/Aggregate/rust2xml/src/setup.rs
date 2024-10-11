// src/setup.rs
use std::time::Instant;

pub struct Timer {
    start: Instant,
}

impl Timer {
    pub fn new() -> Self {
        Timer { start: Instant::now() }
    }

    pub fn elapsed(&self) -> f64 {
        self.start.elapsed().as_secs_f64()
    }
}

