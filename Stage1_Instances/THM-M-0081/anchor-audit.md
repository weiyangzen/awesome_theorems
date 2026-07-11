# Immutable Lean anchor audit

This audit is for `S56-M-0081-ANCHOR_AUDIT` only. The canonical expression remains

```lean
Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y)
```

## Immutable environment

- Worker base revision: `c8855fd0eb87514348ace46003c6075c576fbfb6`.
- Toolchain: `leanprover/lean4:v4.29.0`.
- mathlib: `leanprover-community/mathlib4` at
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`, as pinned by
  `Formalizations/Lean/lake-manifest.json`.
- Direct audit import: `Mathlib.CategoryTheory.Yoneda`.

The existing `.lake` package tree was read and reused. It was not updated, fetched, cloned, or
rebuilt.

## Candidate crosswalk

| Candidate | Exact type contribution | Terminal provenance | Disposition |
|---|---|---|---|
| `Yoneda.fullyFaithful.preimageIso` | representable iso implies object iso | `Yoneda.fullyFaithful` in `Mathlib/CategoryTheory/Yoneda.lean`; generic `Functor.FullyFaithful.preimageIso` in `Mathlib/CategoryTheory/Functor/FullyFaithful.lean` | exact forward-direction anchor |
| `yoneda.mapIso` | object iso implies representable iso | generic `Functor.mapIso`, available through the pinned Yoneda import | exact reverse-direction anchor |
| `yonedaEquiv` | `(yoneda.obj X ⟶ F) ≃ F.obj (op X)` | definition in pinned `Mathlib/CategoryTheory/Yoneda.lean` | strong element-level anchor, not the exact iff |
| `yonedaLemma` | `yonedaPairing C ≅ yonedaEvaluation C` | definition in pinned `Mathlib/CategoryTheory/Yoneda.lean` | strong natural-isomorphism anchor, not the exact iff |
| legacy `yoneda_obj_iso_iff_object_iso` | exact canonical iff | repository file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_138.lean` at the worker base revision | discovery only; rev-5.6 rejects inherited legacy credit |

The checked terminal definitions contain no `sorry`, new `axiom`, `unsafe` declaration, or oracle.
Lean's `#print axioms` reports ordinary mathlib foundational dependencies: the detailed per-anchor
results are preserved in `anchor-audit.json` and the command output below. This is a trust inventory,
not a claim that these dependencies are absent.

All installed, immutable non-mathlib packages under `Formalizations/Lean/.lake/packages` were
searched for the exact/nearby symbols `Yoneda.fullyFaithful`, `yonedaEquiv`, `yonedaLemma`, and
`preimageIso`; none supplied another candidate. An exact-symbol public grep.app request returned
HTTP 429 on 2026-07-12 and therefore contributes no result. The negative conclusion is deliberately
bounded: no additional credible external Lean 4 candidate was established from the installed pins
or that public-search attempt.

## Validation

| Command | Result |
|---|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0081/AnchorAudit.lean` | exit 0; all five declarations elaborated; `#print axioms` completed |
| `python3 -m json.tool Stage1_Instances/THM-M-0081/anchor-audit.json` | exit 0 |
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0081` | exit 0; rank 138, planned, theorem completion false |
| installed pinned-package `rg` search recorded above | exit 1 from no matches; no external candidate found |
| grep.app exact-symbol `curl` request | exit 22; HTTP 429; explicitly not treated as evidence |

The narrow Lean run reported:

- `Yoneda.fullyFaithful`: `[propext, Classical.choice, Quot.sound]`;
- `Functor.FullyFaithful.preimageIso`: `[propext, Quot.sound]`;
- `Functor.mapIso`: `[propext, Classical.choice, Quot.sound]`;
- `yonedaEquiv`: `[propext, Classical.choice, Quot.sound]`;
- `yonedaLemma`: `[propext, Classical.choice, Quot.sound]`.

## Boundary

The pinned mathlib route is feasible and covers both directions, but this phase does not create the
canonical proof wrapper or inspect its eventual composed body. `H2 / M4 / R4`, audit incomplete,
and theorem incomplete therefore remain unchanged. Obligation freezing, source-page and errata
verification, proof execution, hermetic replay, independent verification, and master acceptance are
all downstream gates.
