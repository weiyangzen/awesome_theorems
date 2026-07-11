# Exact-statement gate: blocked

Item: `S56-M-0548-STATEMENT`  
Theorem: `THM-M-0548`  
Base revision: `6ba79369e24bfba400ebdfd7dbacd4fd64e18d2c`

## Decision

The exact Lean 4 target cannot yet be frozen truthfully. The repository source record says only
"duality for subspaces in a sphere." The intake selected a conservative classical variant for a
compact locally contractible subset `A` of `S^n`, but deliberately deferred the choices required
to turn that prose into one proposition:

- the coefficient ring or coefficient object and whether coefficients are constant or local;
- the concrete reduced singular homology and reduced singular cohomology constructions;
- homological versus cohomological orientation of the displayed isomorphism;
- integer grading and the treatment of `n - i - 1`, rather than truncated `Nat` subtraction;
- whether naturality is part of the root conclusion and, if so, its category of admissible maps;
- the empty/full subset, `n = 0`, and out-of-range degree policies.

These are semantic choices, not Lean syntax. Different choices produce non-equivalent targets. In
particular, the pinned mathlib snapshot exposes ordinary singular chains and homology, but the
repository contains no selected reduced singular cohomology construction for this topological
claim. Inventing an opaque cohomology object, or accepting an isomorphism as an input field, would
substitute a statement shape for Alexander duality.

The legacy `AwesomeTheorems.Stage1.S1_M_120.StatementShape` does exactly that: its
`AlexanderDualityData` asks the caller to supply `subsetReducedCohomology`, the degree shift, and
`dualityIso`; it also uses ordinary complement singular homology and only assumes that the carrier
is closed. It neither expresses the intake-selected compact/local-contractibility hypotheses nor
constructs the theorem's reduced theories. It is therefore discovery input only and cannot supply
canonical-statement identity, a checked transport, or proof credit.

Consequently section 5.1's exact-statement gate fails before expression serialization and mutation
testing. No canonical declaration, expression hash, alternate-encoding credit, statement
acceptance, or theorem completion is claimed. Because this assigned phase is not complete, no
`.stage1-worker-selftest.json` is emitted.

## Checked Lean boundary

`StatementProbe.lean` uses the smallest pinned imports found for the unambiguous substrate:

```lean
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Topology.Category.TopCat.Sphere
import Mathlib.Topology.Homotopy.LocallyContractible
```

It elaborates the sphere subset and complement, the conjunction `IsCompact A ∧
LocallyContractibleSpace A`, and the available ordinary complement singular-homology object. It
deliberately declares no canonical Alexander-duality proposition, proof, axiom, or proxy predicate.

## Environment and validation evidence

Commands ran from this worker clone on 2026-07-12. Lean commands ran from `Formalizations/Lean`
against the existing canonical `.lake` symlink. No update, build, fetch, or clone was performed.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256: `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- `StatementProbe.lean` SHA-256:
  `16e3ecfefb86d23a4f7e91728e60f678c970aab11efc72b3919aa0e18b0180a8`.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0548/StatementProbe.lean` | 0 | subset hypotheses and ordinary complement singular-homology types elaborated and printed |
| `lake env lean --version` | 0 | Lean version and commit match the fingerprint above |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | mathlib revision matches the Lake pin above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0548` | 0 | rank 120, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

Known failure: without an authoritative coefficient, reduced-theory, grading, naturality, and
boundary-case decision, the canonical expression and meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutations cannot be produced.

## Retry condition

An accountable source reviewer must select and pinpoint a stable formulation and freeze every
choice listed above. The statement phase can then implement the actual reduced (co)homology types,
minimize imports, serialize the elaborated expression, and run all four mutation classes.
