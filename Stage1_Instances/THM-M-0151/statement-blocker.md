# Exact-statement gate: blocked

Item: `S56-M-0151-STATEMENT`  
Theorem: `THM-M-0151`  
Base revision: `d9657b35845b4b10e25345050fe228f872bc50ad`

## Source identification and exact human claim

The repository catalogue gives only "Hacon theorem", Christopher Hacon, 2007, and the gloss
"pluricanonical maps of varieties of general type". Inspection resolves the intended primary
result to Christopher D. Hacon and James McKernan, *Boundedness of pluricanonical maps of varieties
of general type*, Inventiones Mathematicae 166 (2006), 1--25, DOI
`10.1007/s00222-006-0504-1`. The inspected immutable source is arXiv `math/0504327v3`, dated
2006-01-18, PDF SHA-256
`0adb404914a354cb0f4f78991de60ccc2e3ad8e50ca909be79f544cdca4ff994`.

Theorem 1.1 on page 2 states:

> For any positive integer n, there exists an integer r_n such that if X is a smooth projective
> variety of general type and dimension n, then the rational map from X to the projective space of
> global sections of O_X(rK_X), induced by rK_X, is birational for every integer r at least r_n.

Section 2.1 on page 4 fixes the base field to the complex numbers. Thus the exact binder order is
`forall n > 0, exists r_n, forall X, smooth/projective/general-type/dimension-n X -> forall r >=
r_n, birational (phi_(r K_X))`. The conclusion is for every sufficiently large `r`, not merely for
one `r`, for sufficiently divisible `r`, or for a map assumed as input. The source has two authors,
and its print publication year is 2006; the catalogue's single-author/2007 metadata is inaccurate.

## Lean statement blocker

The pinned mathlib snapshot has a generic scheme rational-map type in
`Mathlib.AlgebraicGeometry.RationalMap`, but it does not provide the interfaces needed to express
the source theorem:

- no canonical divisor or canonical sheaf of a smooth complex variety;
- no pluricanonical complete linear system or its induced rational map;
- no Kodaira dimension or predicate saying that a variety is of general type;
- no algebraic-geometric birational predicate for a rational map;
- no available dimension interface tying the source's variety dimension to all of the preceding
  data.

Repository and pinned-mathlib source searches found no existing declaration that supplies these
missing definitions. Consequently there is no faithful Lean proposition to elaborate with any set
of pinned imports. Introducing opaque predicates for `GeneralType`, `pluricanonicalMap`, or
`Birational`, or quantifying over those notions as caller-supplied data, would merely assume the
mathematical content and would not be the exact target. Replacing the source theorem by the generic
existence of a rational map would weaken it. Both are forbidden substitutions.

The statement phase therefore stops fail-closed before creating a `.lean` declaration. No `sorry`,
axiom, placeholder, abstract package containing the conclusion, broadened theorem, or weakened
special case was introduced. The exact human statement is identified, but its exact Lean 4 target,
minimal imports, expression fingerprint, transports, and statement mutations remain unavailable;
machine debt remains `M4`, and theorem completion remains false.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). Existing `.lake` artifacts were
read only. No update, build, dependency clone, or fetch command was used.

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
| `python3 scripts/stage1_target.py show THM-M-0151` | 0 | Rank 325, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| `curl -L https://arxiv.org/pdf/math/0504327` followed by `pdftotext -layout` and source inspection | 0 | Identified v3, Theorem 1.1, its binder order, page, base field, and exact conclusion |
| repository search for `pluricanonical`, Hacon, and the catalogue labels | 0 | Found the underspecified catalogue metadata and dossier; no formal target |
| pinned-mathlib search for pluricanonical, Kodaira/general type, canonical divisor/sheaf, and algebraic-geometric birational APIs | 1 | No matching required interfaces; generic `Scheme.RationalMap` alone is present |

There is no applicable `lake env lean <target>.lean` validation: the absent definitions are needed
to construct the exact expression that such a file would contain. Compiling an invented predicate
shell would be fake elaboration evidence rather than validation of the assigned deliverable.

## Retry condition

Add pinned, kernel-checkable definitions for smooth projective complex varieties of general type,
canonical divisors and their multiples, global-section projective spaces, the induced
pluricanonical rational map, dimension, and birationality. A later statement run must crosswalk
those definitions to Theorem 1.1, elaborate the binder order above with minimal imports, fingerprint
the expression, and run removed-hypothesis, changed-domain, binder-scope, and boundary mutations.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
