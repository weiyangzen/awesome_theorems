# Exact-statement gate: blocked

Item: `S56-M-0695-STATEMENT`  
Theorem: `THM-M-0695`  
Base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "correspondence between proofs and programs". A duplicate
computer-science inventory adds the slogan "propositions as types, proofs as programs", but it is
not the selected mathematical target and does not state a proposition. Stage0 leaves the exact
definitions, assumptions, formal system, equivalent formulations, and axioms open.

The Curry-Howard correspondence is a family of syntax-sensitive results. The metadata does not
select a source logic or proof calculus, a typed term calculus, formula/context/proof translations,
equality and reduction relations, or the property called a correspondence. Materially different
roots remain compatible with it, including:

1. derivability of a formula iff inhabitation of its translated type;
2. a bijection between derivations and typed terms, usually only modulo specified equalities;
3. alignment of logical rules with type introduction and elimination rules;
4. preservation or reflection between proof normalization and term reduction;
5. substitution compatibility or a dependent, classical, linear, or categorical extension.

These readings require different syntax, binders, hypotheses, conclusions, boundary cases, and
quotient conventions. Selecting an intuitionistic propositional/STLC adequacy theorem, a dependent
type-theory interpretation, or a handful of Lean tautologies would invent or substitute
mathematics. Consequently no canonical human statement, minimal import set, elaborated expression
hash, checked alternate transport, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutation suite exists. Section 5.1 fails before proof evidence may be inspected.

## Pinned Lean boundary

The existing `IntakeProbe.lean` was re-elaborated under the pinned environment. It checks `Prop`,
logical connective/type constructors, introduction and elimination constants, and representative
function terms. This confirms only that Lean embodies proposition/type and proof/term primitives.
It does not relate independently specified calculi and receives no statement or proof credit. No
`sorry`, `admit`, or `axiom` occurs in the target's Lean source.

The environment is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned
mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing canonical
`.lake` artifacts were used read-only. No update, build, clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0695` | 0 | rank 736, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese/English title, and both slogans | 0 | found only the underspecified metadata and open Stage0 fields; no exact proposition |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0695/IntakeProbe.lean` | 0 | all eleven proposition/type primitive checks elaborated; no correspondence theorem asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0695 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0695/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0695/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Retry condition and boundary

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact result, freeze both calculi and every translation, equality, reduction,
assumption, binder, and boundary convention, dispose of errata, and independently approve the
mapping. A later statement run can then encode that same claim, minimize pinned imports, serialize
and hash the elaborated expression, check alternate transports, and execute all four mutation
classes.

This is the first failed gate. The statement node remains `[ ]`, machine state remains `M4`, and
`audit_complete` and `theorem_complete` remain false. The assigned phase is not genuinely
self-tested to its completion gate, so no `.stage1-worker-selftest.json` is emitted.
