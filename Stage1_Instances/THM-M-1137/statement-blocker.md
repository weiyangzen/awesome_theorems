# Exact-statement gate: blocked

Item: `S56-M-1137-STATEMENT`  
Theorem: `THM-M-1137`  
Base revision: `2029732601188918961647a1d1565c7d55a46f04`

## Decision

No exact Lean 4 target can be truthfully frozen from the repository source. The complete source
claim is only "the mean value of harmonic functions" (`调和函数的平均值`), with the title
"mean-value property", a nineteenth-century date, and attribution to "many mathematicians". It
provides no primary citation, formula, theorem/page, or definitions.

The wording leaves materially different propositions unresolved:

- an average over a circle/sphere versus an average over a disk/ball;
- harmonicity on a neighborhood of the closed ball versus harmonicity on the open ball together
  with continuity on its closure;
- the forward property versus its converse or an equivalence characterization;
- planar real-valued harmonic functions versus an arbitrary Euclidean dimension or codomain;
- the averaging measure and normalization, the permitted radii, and boundary-containment rules.

These choices change domains, binders, hypotheses, and conclusions. Selecting one would substitute
a familiar theorem for the source claim, contrary to the exact-statement gate. In particular, the
pinned mathlib module contains at least two distinct forward circle-average declarations:
`HarmonicOnNhd.circleAverage_eq` assumes harmonicity on a neighborhood of `closedBall c |R|`,
while `HarmonicContOnCl.circleAverage_eq` packages harmonicity
on `ball c |R|` and continuity on its closure. The repository source does not select between even
these two nearby candidates, much less circle and volume formulations.

`StatementCandidateProbe.lean` elaborates only those two discovery candidates with the smallest
direct pinned import that exposes them. It is deliberately not a canonical declaration, checked
transport, or proof. No `sorry`, axiom, opaque proxy predicate, weakened special case, or broadened
target was introduced. The exact expression fingerprint and meaningful removed-hypothesis,
changed-domain, binder-scope, and boundary mutation tests therefore cannot exist yet. Machine state
remains `M4`; statement acceptance and theorem completion are false.

## Pinned evidence

Validation date: 2026-07-12 (Asia/Shanghai). Commands ran inside the worker clone using the existing
read-only canonical `.lake` target. No update, build, clone, or fetch command was used.

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
| `python3 scripts/stage1_target.py show THM-M-1137` | 0 | Rank 342, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1137/StatementCandidateProbe.lean` | 0 | Printed both fully elaborated candidate types; candidate-only check, not exact-statement evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` (resolved canonical target) | 0 | Produced the pinned mathlib revision recorded above |
| repository and pinned-mathlib `rg` searches for the source wording and harmonic mean-value declarations | 0 | Found only underspecified repository metadata and the distinct pinned circle-average candidates |

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, map its assumptions and definitions, and freeze the formulation, dimension,
codomain, harmonicity predicate, center/radius scope, containment condition, measure, normalization,
and degenerate-radius policy. A later statement run can then encode that proposition, minimize its
pinned imports, fingerprint the elaborated expression, add checked transports, and run structural
mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
