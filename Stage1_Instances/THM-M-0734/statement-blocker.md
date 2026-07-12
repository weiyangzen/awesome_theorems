# Exact-statement gate: blocked

Item: `S56-M-0734-STATEMENT`  
Theorem: `THM-M-0734`  
Base revision: `91055abb3f5bee7f79323bc9cbefa7f2a8145f1f`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire asserted content is the phrase `代数计算复杂性` ("algebraic computational complexity"),
together with the topic label `代数复杂性`, attribution to Leslie Valiant, and the year 1979. This
identifies a field, not a truth-valued proposition. It supplies no ordered binders, hypotheses,
conclusion, theorem number, page, or exact source edition. Stage0 also leaves the precise
definitions, assumptions, proof route, dependencies, and existing machine artifact open.

Several proposition-changing choices remain unresolved:

- arithmetic circuits versus straight-line programs, formulas, branching programs, or algorithms;
- an individual polynomial versus a polynomial family, and the family encoding and uniformity;
- coefficient semiring, ring, or field, including characteristic and constants policy;
- allowed gates, fan-in, syntactic versus semantic degree, and circuit size or depth conventions;
- exact versus border computation and the reduction/projection convention;
- membership, completeness, simulation, upper-bound, or restricted lower-bound conclusion;
- quantifier order for variables, degree, input length, family index, and asymptotic bounds;
- zero/constant polynomials, zero variables, empty families, and size/depth-zero boundaries.

Choosing any one of Valiant's 1979 definitions or results from this metadata would invent the
missing mathematics. In particular, choosing a VP/VNP relationship would collide with the adjacent
repository target `THM-M-0735`, which separately records that open problem. A convenient theorem
about `MvPolynomial` would instead substitute a polynomial fact for a complexity theorem.

The first failed rev-5.6 gate is therefore canonical human-claim identity, before a minimal Lean
import, declaration/expression, normalized expression hash, alternate-form transport, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutations can exist. No
`Statement.lean` or fake interface is emitted. The existing `IntakeProbe.lean` is rechecked only to
distinguish a working pinned Lean environment from the missing mathematical proposition; its API
checks receive no statement or proof credit.

## Narrow validation evidence

Validation ran on 2026-07-12 (Asia/Shanghai) in this worker clone. The existing canonical `.lake`
artifacts were used read-only. No update, build, dependency clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0734` | 0 | rank 771, lifecycle `planned`, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -i 'THM-M-0734\|代数复杂性\|代数计算复杂性\|algebraic computational complexity' Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Blueprint_Applicable_Theorems.md` | 0 | only the topic/gloss and open Stage0 fields identify this target; VP/VNP is a separate adjacent record |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0734/IntakeProbe.lean)` | 0 | six pinned `MvPolynomial` construction, evaluation, variable-support, and degree APIs elaborated; no target asserted |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0734 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0734/instance.json` | 0 | intake JSON is syntactically valid |
| `python3 -m json.tool Stage1_Instances/THM-M-0734/task-dag.json` | 0 | task DAG JSON is syntactically valid |

## Retry condition and status boundary

An accountable, independent source review must select an immutable primary-source edition and an
exact theorem/page, resolve errata, and freeze every model, domain, representation, resource,
reduction, quantifier, hypothesis, conclusion, and boundary choice above. It must explain why that
proved result, rather than a definition, an open problem, or another 1979 result, is the intended
repository target. Only then can a later statement worker minimize pinned imports, elaborate and
fingerprint the exact expression, check alternate encodings, and execute all four mutation classes.

Verdict: `blocked`. The statement node remains `[ ]`; lifecycle remains `planned`; root vector
remains `[H3, M4, R4]`; `audit_complete: false`; `theorem_complete: false`. The assigned phase did
not pass its completion gate, so no `.stage1-worker-selftest.json` is emitted.
