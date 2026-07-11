# Statement gate blocker

Item: `S56-M-0448-STATEMENT`  
Base revision: `7d17b9db8c379ed7c645c8cd1f7b0c7073736926`

## Verdict

The exact Harris--Taylor target cannot truthfully be frozen from the repository evidence available
to this worker. The intake correctly records the unresolved choice of labelled primary-source
result, field coverage, coefficient field, rank boundary, reciprocity/Frobenius normalization, and
compatibility clauses. Selecting any of these without the exact source result would invent part of
the theorem. Consequently the rev-5.6 statement gate remains blocked and this phase is not marked
self-tested.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_062.lean` cannot repair that gap. Its
`StatementShape` is `Nonempty (HarrisTaylorPackage K i)`, where the package stores abstract
automorphic and Galois parameter types, a `Corresponds` relation, the desired existence and
uniqueness laws, and assumed geometric/trace properties. That is an explicitly documented API
boundary, not an encoding shown equivalent to a labelled Harris--Taylor theorem. Reusing it as the
canonical target would violate the no-broadened/no-substituted-theorem rule.

## Pinned Lean boundary

`StatementProbe.lean` uses only three pinned mathlib imports to elaborate the concrete substrate
currently identifiable without guessing the theorem: a nonarchimedean local-field context,
`Matrix.GeneralLinearGroup n K`, and `Field.absoluteGaloisGroup K`. Repository and pinned-mathlib
search found no declarations for local Langlands, Weil--Deligne representations, or the category of
smooth irreducible admissible representations. The probe deliberately contains no proposed
correspondence theorem, axiom, or proof placeholder.

Environment fingerprint:

- Lean toolchain: `leanprover/lean4:v4.29.0`
- mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`
- Lake manifest and package checkout agree on that revision
- imports: `Mathlib.FieldTheory.AbsoluteGaloisGroup`,
  `Mathlib.LinearAlgebra.Matrix.GeneralLinearGroup.Basic`, and
  `Mathlib.NumberTheory.LocalField.Basic`
- foundation profile: ordinary Lean/mathlib definitions only; no added axioms or declarations
  purporting to prove the root

## Validation record

Run from the repository root on 2026-07-12:

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0448` | exit 0; rank 62, L0/rework_required, planned, theorem_complete false |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'local.?langlands\|weil.?deligne\|smooth.*admissible\|admissible.*smooth' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | exit 1 with no matches |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0448/StatementProbe.lean` | exit 0; printed `k[K] : Type uK` (Lean notation `𝓀[K]`) from the deliberate `#check` |

## First failed gate and unblock condition

First failed gate: rev-5.6 section 5/5.1 canonical-claim identification, before expression hashing,
transport checks, and mutation tests can be meaningful.

To unblock, an integration lane must obtain a stable primary-source edition and freeze the exact
labelled result with its incorporated definitions, pages, assumptions, normalizations, and errata.
It must then either provide concrete Lean definitions for both sides of that exact correspondence
or pin a compatible upstream implementation. Only after that can an exact proposition be
elaborated, serialized, fingerprinted, transported, and mutation-tested. No proof, audit
completion, or theorem completion is claimed here.
