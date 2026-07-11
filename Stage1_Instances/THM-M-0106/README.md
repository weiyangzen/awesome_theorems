# THM-M-0106 intake dossier

## Status boundary

This remains a `planned` rev-5.6 instance for the Noether normalization lemma. The statement node has now self-tested an exact Lean target and a checked historical-shape transport, pending master acceptance. It does not claim accepted source fidelity, proof closure, or theorem completion. The historical `S1-M-030` proof material and the manifest label `已验证` remain discovery inputs only.

## Scope map

| Scope ID | Included claim | Boundary |
|---|---|---|
| `SCOPE-ROOT` | A nonzero finite-type commutative algebra over a field is finite over an injectively embedded polynomial algebra in finitely many variables. | Exact binders and universes await the statement gate. |
| `SCOPE-ALG` | Coordinate-ring form using `MvPolynomial (Fin s) k`, injectivity, and `AlgHom.Finite`. | No legacy wrapper receives proof credit at intake. |
| `SCOPE-GEO` | Contravariant affine form: `Spec R` admits a finite morphism to affine space over `Spec k`. | Only the affine-scheme translation is included; a theorem for arbitrary varieties is not asserted. |
| `SCOPE-TRANSPORT` | Equivalence/implications between algebraic and affine formulations. | Must be kernel-checked in later phases. |
| `SCOPE-EXCLUDED` | Zero rings, arbitrary non-affine schemes, and claims about a specific primary-source formulation. | Excluded until assumptions and transports are explicitly audited. |

## Source-statement crosswalk

| Crosswalk ID | Source surface | Source wording or artifact | Intended node | Intake assessment |
|---|---|---|---|---|
| `SRC-MANIFEST` | `Docs/Stage1_Targets_rev-5.6.json`, rank 30 | Name `诺特正规化引理`; geometry/algebraic-geometry; untrusted status `已验证` | `SCOPE-ROOT` | Membership and scheduling evidence only; not H or M evidence. |
| `SRC-LEGACY-BP` | `Docs/Stage1_Blueprint.md`, `S1-M-030` | “仿射簇到仿射空间的有限态射” | `SCOPE-GEO` | Too terse to freeze all hypotheses; mapped as a scope clue, not an exact statement. |
| `SRC-LEGACY-LEAN` | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_030.lean` | `IntegralStatementShape`, `AlgebraicStatementShape`, `AffineSchemeStatementShape` | `SCOPE-ALG`, `SCOPE-GEO` | Candidate encodings only; rev-5.6 statement elaboration and transports remain open. |
| `SRC-MATHLIB-CANDIDATE` | `Mathlib.RingTheory.NoetherNormalization` import named by the legacy module | candidate `exists_integral_inj_algHom_of_fg` | `SCOPE-ALG` | Anchor audit is a later node; no immutable source/body or closure claim is made here. |
| `SRC-PRIMARY-OPEN` | Primary mathematical publication/textbook | not yet pinpointed | `SCOPE-ROOT` | H status remains unclassified. Edition, theorem/page, assumptions, proof, errata, and reviewer are required before H0. |

The statement phase selected a checked package containing both the algebraic normalization data and its affine-space consequence. See `Statement.lean`, `statement.json`, and `statement-validation.md`. The package is checked equivalent to the legacy affine-Spec shape, while arbitrary non-affine varieties remain excluded.

## Open task DAG

`S56-M-0106-INTAKE` precedes `STATEMENT`, `ANCHOR_AUDIT`, `OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE` in that order. The statement artifacts are provisional worker evidence only. Immediate next work after master acceptance is the immutable anchor audit; primary-source pinpointing also remains required.

## Validation record

Base revision: `a8d6489fd935cd71fa4499f2f3f5b051998203f4`.

The intake was structurally checked with:

```text
python3 Docs/tools/check_stage1_standard.py
  exit 0: check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)
python3 scripts/stage1_target.py check
  exit 0: stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)
python3 scripts/stage1_target.py show THM-M-0106
  exit 0: rank 30; baseline L0; lifecycle planned; theorem_complete false
```

The original intake commands above remain intake evidence. Statement-specific Lean evidence and exact commands are recorded separately in `statement-validation.md`; no theorem proof or later gate is credited.
