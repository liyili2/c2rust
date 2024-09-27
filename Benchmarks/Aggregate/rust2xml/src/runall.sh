#!/bin/bash


rm -fr output.json output.xml output_b.json output_b.rs
cargo run --bin rust2xml
cargo run --bin xml2json
cargo run --bin json2rust


rustc output_b.rs
./output_b