#!/usr/bin/env bash
shopt -s expand_aliases

export CLASSPATH=$(pwd)/rust/parser/antlr/antlr-4.13.1-complete.jar:$CLASSPATH;
alias antlr4='java -jar $(pwd)/rust/parser/antlr/antlr-4.13.1-complete.jar';
antlr4 -Dlanguage=Python3 "$(pwd)/rust/parser/Rust.g4" -o "$(pwd)/rust/parser"
