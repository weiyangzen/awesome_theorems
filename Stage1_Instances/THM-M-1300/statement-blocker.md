# Exact-statement gate: blocked

Item: `S56-M-1300-STATEMENT`  
Theorem: `THM-M-1300`  
Base revision: `bce57eae7d429ef0eaa638cf3a12aee8f59fe7c7`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository's authoritative
material. The complete mathematical content in the Stage0 record is the label "Triebel-Lizorkin
spaces" and the gloss "refinement of function spaces." This identifies a subject, not a
proposition. It supplies no definition, binders, hypotheses, or conclusion. The intake's candidate
reference, Hans Triebel's *Theory of Function Spaces* (1983), is explicitly only a discovery
anchor: no edition hash, theorem/page, surrounding definitions, or errata were inspected and no
exact theorem was selected.

The missing choices are substantive and non-equivalent. At minimum, a source decision must fix:

- homogeneous or inhomogeneous spaces and the treatment modulo polynomials;
- ambient domain and dimension, scalar field, and tempered-distribution convention;
- smoothness `s`, exponents `p` and `q`, endpoint and quasi-Banach ranges;
- dyadic resolution of unity, mixed sequence/function quasi-norm, and independence from cutoffs;
- which proposition "refinement" denotes: characterization, embedding, interpolation, lifting,
  atomic decomposition, or another structural result.

Choosing a standard modern definition is not enough because a definition is not the requested
theorem. Choosing a convenient embedding or asserting the desired result as a structure field
would substitute for the unknown catalog claim. Therefore there is no honest canonical Lean
expression, minimal target import, normalized expression hash, checked alternate transport, or
removed-hypothesis/domain/binder-scope/boundary mutation suite. The first failed gate is the
section 5 canonical human-statement identity gate; machine status remains `M4`.

## Lean boundary checked

`StatementProbe.lean` uses the single pinned import
`Mathlib.Analysis.Distribution.TemperedDistribution` to check the nearby substrate declarations
`TemperedDistribution`, `SchwartzMap`, `MeasureTheory.MemLp`, and `MeasureTheory.eLpNorm`. This
establishes only that tempered distributions, Schwartz maps, and ordinary `L^p` predicates/norms
are available. A case-insensitive search of pinned mathlib's `Mathlib` source for `Triebel` or
`Lizorkin` found no match. Neither result supplies the dyadic mixed norm or a theorem selected from
the source, so the probe receives no canonical-statement or proof credit.

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Lean used the existing canonical
`.lake` artifacts read-only; no update, build, clone, or fetch was run.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1300` | 0 | Rank 468, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `rg -ni 'triebel\|lizorkin' Formalizations/Lean/.lake/packages/mathlib/Mathlib Formalizations/Lean/.lake/packages/mathlib/Mathlib.lean` | 1 | No match in pinned mathlib source |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1300/StatementProbe.lean` | 0 | All four nearby substrate declarations elaborated |
| `rg -n '\\b(sorry\|axiom\|admit)\\b' Stage1_Instances/THM-M-1300/StatementProbe.lean` | 1 | No forbidden proof placeholder or added axiom found |
| `git diff --check -- Stage1_Instances/THM-M-1300` | 0 | No output |

## Retry condition

Retry after an accountable reviewer obtains and hashes a stable primary source, selects a pinpoint
theorem and page, checks its imported definitions and errata, and crosswalks every parameter,
endpoint, cutoff convention, hypothesis, and conclusion into ordered Lean binders. The statement
phase can then implement the missing analytic interfaces if necessary, minimize the imports,
serialize the elaborated expression and environment, check alternate transports, and run all four
required mutation classes.

This artifact records a blocker. It does not complete the statement node, accept a receipt, modify
the execution DAG, or claim audit/theorem completion. No `.stage1-worker-selftest.json` is emitted
because the assigned phase is not genuinely self-tested.
