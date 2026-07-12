# Exact-statement gate: blocked

Item: `S56-M-0336-STATEMENT`  
Theorem: `THM-M-0336`  
Base revision: `3d8dd27e4ff1200a2d9c8daaa9cae8072eca6241`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "Connes classification theorem" and "classification of injective
von Neumann algebras", attributed to Alain Connes in 1976. It gives no primary-source theorem or
page and does not identify one proposition.

The intake records Connes' 1976 article *Classification of Injective Factors. Cases II1,
II-infinity, III-lambda, lambda != 1* only as a candidate locator. The title itself describes a
package of cases, not a source-frozen theorem. The repository wording does not decide among:

- uniqueness of the injective factor of type `II_1`;
- the 1976 package for types `II_1`, `II_infinity`, and `III_lambda` with its exact parameter range;
- a later classification including type-III cases not settled in that paper;
- an injective/amenable/hyperfinite equivalence rather than a classification conclusion; or
- a central-decomposition result for general von Neumann algebras rather than factors.

These readings have different domains, factor and separability hypotheses, type parameters,
canonical models, equivalence notions, and conclusions. Selecting one would substitute or broaden
the unknown root. Consequently there is no canonical human statement from which to derive a
minimal import, elaborated expression fingerprint, checked alternate transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations. Section 5.1 of the
rev-5.6 standard fails before proof evidence may be inspected. Machine state remains `M4`; neither
statement acceptance nor theorem completion is claimed.

## Pinned Lean boundary

`IntakeProbe.lean` imports `Mathlib.Analysis.VonNeumannAlgebra.Basic` and checks the available
abstract and concrete von Neumann algebra, commutant, and star-projection APIs. It elaborates in the
pinned environment, but it contains no injectivity, factor-type, hyperfiniteness, canonical-model,
or classification target and receives no statement or proof credit. A narrow search of pinned
mathlib found no injective-factor, amenable-factor, hyperfinite-factor, type-`III_lambda`,
semidiscrete, or Connes-classification declaration.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. Existing canonical
`.lake` artifacts were used read-only; no update, build, clone, or fetch was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0336` | 0 | rank 829; planned; legacy artifacts unaccepted; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese/English labels, and classification gloss | 0 | found only underspecified metadata and the intake's unaccepted candidate locator; no exact proposition |
| pinned `Mathlib/Analysis/VonNeumannAlgebra` `rg` search for injective, amenable, hyperfinite, type-III-lambda, semidiscrete, and Connes classification terms | 1 | no relevant declaration (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0336/IntakeProbe.lean` | 0 | six operator-algebra substrate declarations elaborated; no canonical target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0336 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0336/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0336/task-dag.json` | 0 | task-DAG JSON is syntactically valid |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe one exact numbered result with its incorporated definitions and assumptions, audit
errata, distinguish the 1976 cases from later classification results, and independently approve
the mapping. The selected result must fix the algebra presentation, factor and injectivity
predicates, separability/countability assumptions, type range, canonical model, isomorphism notion,
ordered binders, and degenerate cases. A later statement run can then encode that same claim,
minimize imports, serialize and hash its elaborated expression, check alternate transports, and run
all four required mutation classes.

This is the first failed gate, not completion of the statement node or a later node. The root
remains `[H1, M4, R4]`, with `audit_complete: false` and `theorem_complete: false`. The assigned
phase is not genuinely self-tested to its completion gate, so no `.stage1-worker-selftest.json` is
emitted.
