# Exact-statement gate: blocked

Item: `S56-M-1135-STATEMENT`  
Theorem: `THM-M-1135`  
Base revision: `2029732601188918961647a1d1565c7d55a46f04`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository
record. Its complete mathematical wording is `调和函数的基本方程` ("the
fundamental equation of harmonic functions"), under the topic title "Laplace
equation." This identifies the conventional formula `Delta u = 0`, but not a
closed theorem or even one uniquely typed predicate.

The record does not fix:

- the dimension or ambient space;
- the scalar codomain;
- an open domain, arbitrary set, point, or global scope;
- classical, weak, or distributional derivatives;
- the required regularity of `u`;
- whether the claim is a definition of harmonicity, an equation imposed on a
  function, or an equivalence with another characterization;
- ordered binders, hypotheses, boundary behavior, or a quantified conclusion.

These choices are not cosmetic. For example, pinned mathlib's
`InnerProductSpace.HarmonicAt` requires twice continuous differentiability and
eventual vanishing of the Laplacian near a point, while
`InnerProductSpace.HarmonicOnNhd` quantifies that predicate over a set. A
pointwise equation on a domain, a distributional equation, and either mathlib
predicate have different domains, regularity assumptions, and scope.
Selecting one would silently narrow or substitute the unknown source claim.
The nearby `THM-M-1136` harmonic-function target also prevents treating a
definition of harmonicity as the intended theorem without a source decision.

Consequently there is no canonical human proposition from which to determine
minimal imports, preserve an elaborated expression, check alternate
transports, or run meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. Machine state remains `M4`; statement
acceptance and theorem completion are false.

## Pinned Lean boundary

`StatementProbe.lean` uses the single direct import
`Mathlib.Analysis.InnerProductSpace.Harmonic.Basic`. It elaborates
`Laplacian.laplacian`, `InnerProductSpace.HarmonicAt`, and
`InnerProductSpace.HarmonicOnNhd`. This confirms that a classical
finite-dimensional harmonic-function substrate exists in the pinned
environment. It is discovery evidence only, not the canonical target and not
proof credit.

Environment fingerprint:

- Lean toolchain: `leanprover/lean4:v4.29.0`;
- Lean: `4.29.0`, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`;
- Lake: `5.0.0-src+98dc76e`;
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`;
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`;
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

Commands ran inside this worker clone. The existing canonical `.lake` link was
used read-only; no dependency mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1135` | 0 | Rank 340, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1135/StatementProbe.lean` | 0 | All three pinned substrate declarations elaborated |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository and pinned-mathlib `rg` searches for the target wording, Laplacian, and harmonic-function APIs | 0 | Found only the underspecified target metadata plus classical, weak, and distributional alternatives; no source-frozen proposition for this target |

## Retry condition

An accountable source review must supply an immutable edition and exact
page/theorem anchor that fixes whether this item is a proposition rather than
an equation label, then freeze every ambient-space, codomain, domain,
regularity, solution-notion, binder, hypothesis, and conclusion choice above.
A later statement run can then encode that exact claim, minimize its imports,
fingerprint the elaborated expression and environment, check alternate
transports, and execute all four required mutation classes.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
