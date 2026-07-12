# THM-M-0032 statement validation

Item: `S56-M-0032-STATEMENT`

Base revision: `94f6abf9359f26384e0f68bef694dc5b9aae624c`

## Frozen target

`Stage1Instances.THM_M_0032.AuslanderBuchsbaumUFDTarget` states
`forall (R : Type u) [CommRing R] [IsRegularLocalRing R], UniqueFactorizationMonoid R`.
This is the unrestricted regular-local-ring claim in the repository and primary Theorem 5, not the
Auslander-Buchsbaum depth formula or the dimension-at-most-three intermediate result.

The only direct import is `Mathlib.RingTheory.RegularLocalRing.Defs`. It transitively exposes the
UFD interface, so the separate UFD definitions import used by the intake probe is unnecessary.
The checked iff changes only the regularity evidence from an instance binder to an explicit
hypothesis. No target proof body is declared, inspected, or credited.

## Commands and results

All commands ran in the isolated worker clone. Lean ran from `Formalizations/Lean` against the
existing pinned Lake environment. No dependency or `.lake` mutation command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets passed; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0032` | 0 | rank 1076; planned; no legacy slot; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake env lean ../../Stage1_Instances/THM-M-0032/Statement.lean` | 0 | exact target, checked iff, four expected type rejections, rational-field boundary, axiom report, and explicit expression elaborated; output SHA-256 `2a26d392...37d1` |
| `python3 -B ../../Stage1_Instances/THM-M-0032/check_statement.py` | 0 | expression SHA-256 `199d16d6...8d8`; source SHA-256 `5391ab5c...7f3a`; all mutations, import deletion, pins, fingerprints, and structured records agree |
| deletion probe without `Mathlib.RingTheory.RegularLocalRing.Defs` | 1 expected | `CommRing`, `IsRegularLocalRing`, and `UniqueFactorizationMonoid` target vocabulary is unavailable |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib revision `8a178386...a95`, tree `bdc39a31...b7` |
| `python3 -m json.tool` over all owned JSON and `.stage1-worker-selftest.json` | 0 | all structured artifacts are valid JSON |
| prohibited Lean construct scan over owned Lean sources | 1 expected no match | no `sorry`, `admit`, `sorryAx`, `axiom`, `constant`, `opaque`, or `unsafe` declaration occurs |
| `git diff --check -- Stage1_Instances/THM-M-0032 .stage1-worker-selftest.json` plus new-file no-index checks | 0 | no whitespace diagnostics |

## Mutation and status boundary

The validator serializes the canonical target and each mutation under the same explicit/universe
options, then rejects any mutation with the canonical fingerprint. Lean type-checks expected
failures for removal of regularity, specialization to fields, existential binder scope, and a
mutation excluding fields. `Rat` separately kernel-checks as both regular local and a field, so the
dimension-zero field boundary is genuinely included.

This is statement-only evidence pending master acceptance. Source-definition fidelity remains H1,
and anchor audit, obligation tree, target proof, validation, release, readable reconstruction,
audit completion, and theorem completion remain open.
