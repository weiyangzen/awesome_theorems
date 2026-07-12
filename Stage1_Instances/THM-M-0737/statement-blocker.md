# Exact-statement gate: blocked

Item: `S56-M-0737-STATEMENT`  
Theorem: `THM-M-0737`  
Base revision: `3159849a5319960dea505779c7c20894ea30487c`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `Frege证明系统的下界` ("lower bounds for Frege proof systems"),
with an attribution to Alexander Razborov and the year 1985. There is no primary-source citation,
theorem/page, exact proposition, or definition. Stage0 marks the definitions, assumptions, proof
route, dependencies, axiom requirements, and machine artifacts as open.

The missing choices alter the proposition rather than merely its Lean presentation:

- unrestricted Frege, bounded-depth Frege with a fixed depth and connective basis, or another
  restricted system;
- Hilbert, sequent, line, tree, or DAG presentation and the relevant simulation convention;
- the hard tautology family and its input-size parameter;
- proof length measured in lines, symbols, or encoded bits;
- a concrete polynomial, superpolynomial, or exponential bound; and
- pointwise, eventual, infinitely-often, or worst-case quantification, plus explicitness and
  constructibility conditions.

In particular, substituting a known restricted-Frege result for an unspecified unrestricted Frege
claim, or substituting nearby circuit, monotone-circuit, or resolution work suggested by the
attribution and year, would violate exact-statement identity. The repository's `已验证` label is
explicitly untrusted metadata and cannot settle these choices.

Therefore no canonical human claim exists from which to derive a minimal import, ordered Lean
binders, an elaborated kernel-expression hash, checked alternate transports, or meaningful removed-
hypothesis, changed-domain, binder-scope, and boundary mutations. This is the first failed gate in
section 5.1 of the rev-5.6 standard. Machine state remains `M4`; statement acceptance and theorem
completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports `Mathlib.Computability.Encoding` and
`Mathlib.Analysis.Asymptotics.Defs`. It checks only generic encodings, encoded-length substrate,
`atTop`, and `IsBigO`. Re-elaboration proves that the pinned Lean environment is usable, not that a
Frege system or lower-bound theorem has been encoded. A narrow name search of pinned mathlib found
no Frege or proof-complexity declaration. Neither result receives statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing `.lake`
artifacts were used read-only. No update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on `2026-07-12` (`Asia/Shanghai`).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0737` | 0 | rank 773, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| repository `rg` search for the theorem ID and Chinese/English claim | 0 | found only the topic-level metadata and intake dossier; no exact source proposition |
| pinned-mathlib `rg` search for Frege and proof-complexity names | 1 | no matching declaration (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0737/IntakeProbe.lean` | 0 | elaborated all six generic substrate checks; no canonical theorem target asserted |
| `rg -n '\\b(sorry|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0737 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition

An accountable reviewer must preserve and inspect an immutable primary-source edition, identify an
exact theorem/page, incorporate all definitions and assumptions, dispose of errata and the
historical attribution, and independently approve its identity with this catalog target. A later
statement worker can then encode that same proposition, minimize pinned imports, fingerprint the
elaborated expression, check alternate encodings, and run all required statement mutations.

The assigned phase did not pass its completion gate. The statement node remains `[ ]`, the root
remains `[H3, M4, R4]`, and no `.stage1-worker-selftest.json` is emitted.
