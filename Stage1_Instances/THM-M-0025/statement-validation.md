# THM-M-0025 statement validation

Item: `S56-M-0025-STATEMENT`; base revision:
`936bf2b9e968abd3b79b5b36d32f2f2bff648c7e`; base tree:
`8c9d3261b0ba9a81deb5bfc19a335a02cb80f962`.

## Frozen target

`Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget` quantifies over an implicit
`R : Type u`, its `CommRing R` instance, and its `IsNoetherianRing R` instance, and concludes
`IsNoetherianRing (Polynomial R)`. It has no nontriviality, domain, field, characteristic, or
finiteness premise. Thus it is the exact encoding of the conventional commutative, univariate
repository scope selected and frozen at intake, including the zero ring.

The checked `hilbertBasisTheoremTarget_iff_idealFiniteGenerationTarget` transport expands the
Noetherian hypothesis and conclusion into finite generation of every ideal. The two direct imports
are minimal statement-supporting modules. In particular, this artifact does not import
`Mathlib.RingTheory.Polynomial.Basic` or invoke `Polynomial.isNoetherianRing`.

## Commands and results

All commands ran at the repository root unless the table gives a different working directory.
The automation-provided canonical `.lake` symlink was reused read-only; no update, build, clone,
fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard projection and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0025` | 0 | rank 1070; planned; intake provisional; theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0025/Statement.lean` | 0 | exact target, checked ideal-FG iff, four expected type rejections, zero-ring boundary, axiom reports, and explicit expression elaborated |
| `cd Formalizations/Lean && python3 ../../Stage1_Instances/THM-M-0025/check_statement.py` | 0 | expression SHA-256 `9bb5ed6d...564`, source SHA-256 `d629f0c4...f6c`, output SHA-256 `d805957a...b02`; all four mutations distinguished; imports, pins, and receipts agree |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0025/BoundaryProbe.lean` | 0 | `PUnit` checks as a concrete `CommRing`, `IsNoetherianRing`, and zero ring (`0 = 1`) |
| deletion probe without `Mathlib.Algebra.Polynomial.Basic` | 1 expected | `Polynomial` and its required structure are unavailable |
| deletion probe without `Mathlib.RingTheory.Noetherian.Defs` | 1 expected | `IsNoetherianRing` and the ideal finite-generation interface are unavailable |
| `python3 -m json.tool` over all owned JSON and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| prohibited Lean construct scan over owned `.lean` sources | 1 expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration occurs in source |
| `git diff --check -- Stage1_Instances/THM-M-0025 .stage1-worker-selftest.json` plus no-index checks | 0 | no whitespace diagnostics |

## Boundary and status

The validator serializes each mutation under the same explicit/universe options and rejects any
mutation whose expression fingerprint equals the root. Lean also rejects each mutation as a term
of the root using `#check_failure`: removal of the Noetherian hypothesis, specialization to fields,
moving the Noetherian hypothesis into a conjunction, and adding `Nontrivial` to exclude zero rings.
The subsingleton witness checks that the latter premise cannot silently be present.

This is statement-only evidence pending master acceptance. It does not inspect or credit the
pinned Hilbert basis theorem proof body, settle primary-source fidelity, or advance anchor-audit,
obligation-tree, proof, validation, release, audit-completion, or theorem-completion state.
