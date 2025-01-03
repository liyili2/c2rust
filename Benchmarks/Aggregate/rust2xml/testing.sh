#!/bin/bash

##cd Benchmarks/Aggregate/rust2xml
##cp src/output.xml output.xml
pwd
cargo test -- --nocapture

#cp output.xml src/output.xml

#cargo run --bin xml2json
#cargo run --bin json2rust
