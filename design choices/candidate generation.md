# Mutation Candidate Generation

This document summarizes how replacement candidates are generated for each expression type. In every case, a marked node is mutated by swapping in something drawn from what is currently in scope: function parameters plus `let`-bindings seen so far.

## Summary

| Expression type | Example | Mutation |
|---|---|---|
| `IdentifierExpression` | `x` | Replace with another in-scope name (type-filtered when types are known) |
| `BinaryExpression` | `x + 1` | Swap operator within its group, **or** replace left operand, **or** replace right operand |
| `FunctionCallExpression` | `foo(x)` | Replace one randomly chosen argument with an in-scope name |
| `BorrowExpression` | `&x` / `&mut x` | Flip `is_mutable()` |
| `ArrayLiteral` | `[1, 2, 3]` | Swap two elements within the array |
| `CastExpression` | `x as i64` | Replace the source expression with an in-scope name |
| `UnaryExpr` | `-x`, `!x` | Replace the operand with an in-scope name |
| `DereferenceExpr` | `*x` | Replace the inner expression with an in-scope name |
| `ParenExpr` | `(x)` | Replace the inner expression with an in-scope name |
| `RangeExpression` | `0..10` | Coin flip: replace the start or the end with an in-scope name |
| `QualifiedExpression` | | Replace the inner expression with an in-scope name |
| Anything else | | Rebuilt unchanged; no mutation attempted |

## Details per type

### IdentifierExpression (`x`)

Looks at everything currently in scope, excluding the identifier's own name. If the original identifier's type is known and a candidate's type is known, only type-matching candidates are kept. One is picked at random. If nothing else is visible, the identifier is returned unchanged.

### BinaryExpression (`x + 1`)

Builds up to three separate candidate expressions, then picks one at random:

1. **Operator swap:** replace the operator with another from the same group. Groups are arithmetic (`+ - * / %`), comparison (`< > <= >= == !=`), and logical (`&& ||`). It never crosses groups.
2. **Left operand:** replace the left operand with another in-scope name.
3. **Right operand:** replace the right operand with another in-scope name.

### FunctionCallExpression (`foo(x)`)

Picks one argument at random and replaces it with another in-scope name. The function being called (`foo` itself) is never mutated.

### BorrowExpression (`&x` / `&mut x`)

Flips `is_mutable()`. The inner expression is left as-is.

### ArrayLiteral (`[1, 2, 3]`)

Swaps two elements within the same array at random.

### CastExpression (`x as i64`)

Replaces the source expression with another in-scope name. The target type is left untouched.

### UnaryExpr (`-x`, `!x`)

Replaces the operand with another in-scope name. The operator itself is left as-is.

### DereferenceExpr (`*x`)

Replaces the inner expression with another in-scope name.

### ParenExpr (`(x)`)

Replaces the inner expression with another in-scope name. The parentheses are always preserved.

### RangeExpression (`0..10`)

Coin flip: replaces either the start or the end with an in-scope name.

### QualifiedExpression

Treated the same as `ParenExpr` and `DereferenceExpr`: the inner expression is replaced with an in-scope name.

### Anything else

A marked node whose type isn't one of the above is returned rebuilt but otherwise unchanged. No mutation is attempted.

## Cross-cutting rules

- **Candidates come from scope:** function parameters and `let`-bindings seen so far.
- **Structure is preserved:** operators (unary), target types (casts), callees (calls), and parentheses are never altered. The exceptions are binary operators, which swap within their own group, and borrows, which flip mutability.
- **Selection is random** wherever more than one candidate exists.
