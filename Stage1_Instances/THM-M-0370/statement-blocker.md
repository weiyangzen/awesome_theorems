# Exact-statement gate: blocked

Item: `S56-M-0370-STATEMENT`  
Theorem: `THM-M-0370`  
Base revision: `b8a117cd19ae3b30b59087d7bc9c8071ee7212ab`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is `A_p` weights and operator boundedness, together with the title
"weighted norm inequality", Benjamin Muckenhoupt, and 1972. It does not identify an operator,
state a proposition, or give a primary-source theorem/page. The accepted intake therefore leaves
the canonical claim and formal target null.

The metadata is compatible with several inequivalent results: the strong `(p,p)` boundedness of a
centered or uncentered Hardy-Littlewood maximal operator characterized by `A_p` for `1 < p <
infinity`; an endpoint weak-type result for `A_1`; one direction of either result; or a weighted
bound for a different operator. Even the likely maximal-function reading does not fix Euclidean
dimension, balls versus cubes, the base measure, real versus complex functions, the definition of
the weight and its characteristic, the weighted norm convention, or qualitative versus
quantitative constant dependence.

Those choices alter the domains, ordered binders, hypotheses, conclusion, and boundary cases.
Selecting one from mathematical familiarity would substitute a theorem for the repository's
unresolved label. The bibliographic locator Benjamin Muckenhoupt, *Weighted norm inequalities for
the Hardy maximal function* (1972), recorded by intake has not been accepted as an immutable,
pinpoint-inspected statement crosswalk and cannot fill the missing claim in this phase.

Consequently there is no canonical expression to serialize or hash, no meaningful alternate-form
transport, and no sound removed-hypothesis, changed-domain, binder-scope, or boundary mutation
suite. Section 5.1 of the rev-5.6 blueprint fails before proof evidence may be inspected. No Lean
declaration, assumed operator interface, placeholder, axiom, weakened special case, or broadened
target was introduced. Machine state remains `M4`; statement acceptance and theorem completion are
false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports the weighted-measure and `L^p` representation modules and
checks `Measure.withDensity`, `withDensity_apply`, `eLpNorm`, `MemLp`, `lintegral`, and measure
restriction. Re-elaboration confirms that these APIs exist in the pinned environment. They neither
define an `A_p` predicate nor identify the intended operator or theorem, so the probe receives no
statement or proof credit. A narrow pinned-mathlib name/text search found no Muckenhoupt, `A_p`
weight, or Hardy-Littlewood maximal-function theorem.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the `lake-manifest.json`
SHA-256 is `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The existing canonical
`.lake` link and artifacts were used read-only. No update, build, clone, fetch, or dependency
mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0370` | 0 | rank 862, planned, legacy artifacts unaccepted, theorem incomplete |
| `git rev-parse HEAD` | 0 | base revision recorded above |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English labels, source title, and Muckenhoupt | 0 | only underspecified metadata and the intake's unaccepted bibliographic locator were found; no source-frozen proposition |
| pinned-mathlib `rg` search for Muckenhoupt, `A_p` weights, and Hardy-Littlewood maximal theorems | 1 | no matching theorem-specific API (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0370/IntakeProbe.lean` | 0 | all six representation APIs elaborated; no canonical theorem target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0370 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe the exact definition and theorem with all incorporated assumptions, audit errata,
and independently approve the clause-by-clause mapping. In particular, the review must fix the
operator, averaging sets, base space and measure, exponent range, weight conventions, norm,
quantifier direction, constant dependence, and all degenerate cases. A later statement run can
then encode that same claim, minimize pinned imports, fingerprint the elaborated expression, check
alternate transports, and execute all four required mutation classes.

This is the first failed gate, not completion of the statement node or a later phase. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
