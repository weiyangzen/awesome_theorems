# Exact-statement gate: blocked

Item: `S56-M-0550-STATEMENT`  
Base revision: `885dbbecf4ba550a8fad85762f17925c4a87a420`

## Decision

The exact Lean 4 target cannot be truthfully selected from the repository
source. Its complete mathematical wording is `上积与斯廷罗德运算的关系`
("the relationship between the cup product and Steenrod operations"). That
identifies the Cartan-formula family, but does not determine one proposition.
In particular, it leaves open:

- the mod-2 Steenrod-square formula or an odd-prime reduced-power formula;
- a component identity or multiplicativity of a total operation;
- the space, simplicial, or cochain model of ordinary cohomology;
- the coefficient object, grading conventions, index range, and treatment of
  operations outside the instability range; and
- for odd primes, which reduced-power/Bockstein operations and sign conventions
  are included.

These alternatives are not definitionally interchangeable and some are
mathematically different theorems. Selecting the familiar component formula

`Sq^n (x cup y) = sum_{i+j=n} Sq^i x cup Sq^j y`

would therefore add the coefficient prime, operation family, domains, and
grading conventions that the source never fixes. An abstract record containing
an arbitrary cup product and arbitrary operations would elaborate, but would
only restate the desired equality as unconstrained data; it would not encode
Steenrod operations on cohomology. Either construction would be a broadened or
substituted theorem and is forbidden by the rev-5.6 statement gate.

The intake record already preserves this ambiguity with
`gate_state: open_pending_source_backed_statement_selection`. Its two listed
candidate encodings have no checked witness and deliberately receive no
statement credit. The statement worker cannot override that source-selection
boundary.

## Pinned Lean boundary

The existing pinned environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The toolchain and Lake manifest
SHA-256 values are respectively
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2` and
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

A literal case-insensitive search for `Steenrod`, `Cartan formula`, or
`Cartan.*formula` in the pinned mathlib `Mathlib` tree returned no matches
(exit 1). A broader cup-product search found no singular-cohomology cup-product
API that could resolve the missing source choices. This is only a local API
boundary check, not the later anchor audit and not evidence that no external
formalization exists. No dependency update, fetch, or mutation of `.lake` was
performed.

## Commands and results

All commands ran inside this worker automation clone on 2026-07-12.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0550` | 0 | rank 602, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | pinned-file hashes recorded above |
| `rg -n -i 'Steenrod\|Cartan formula\|Cartan.*formula' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 1 | no matching pinned mathlib source; exit 1 means no matches |

## Gate result and retry condition

The first failed gate is section 5 exact-statement identity. Without an
authoritative source-backed choice, there is no canonical human proposition to
map to Lean, so minimal imports, a normalized expression hash, checked
alternate transports, and meaningful removed-hypothesis/domain/binder-scope/
boundary mutation tests cannot be produced. Machine status remains `M4`; no
proof, audit completion, or theorem completion is claimed.

Retry after an accountable source decision pins one exact formula and freezes
the prime, operation family, cohomology model, coefficients, ordered binders,
grading/index conventions, and boundary behavior. No
`.stage1-worker-selftest.json` is emitted because the assigned statement phase
is not self-tested to completion.
