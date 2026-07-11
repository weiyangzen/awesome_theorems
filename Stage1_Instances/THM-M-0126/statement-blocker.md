# Statement gate blocker

Item: `S56-M-0126-STATEMENT`  
Theorem: `THM-M-0126`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The source record identifies only the topic "Shimura curve theorem" and the phrase "modular curve
over a quaternion algebra." It gives no primary source, theorem/page, base field, ramification or
indefiniteness assumptions, quaternion order, level, moduli functor, equivalence relation, or exact
conclusion. In particular it does not decide whether the target is representability, algebraicity,
properness/smoothness, complex uniformization, a canonical model, or another theorem customarily
called a Shimura-curve theorem.

Selecting any one of these inequivalent claims would invent missing mathematics and violate the
exact-statement gate. Therefore the ordered binders, hypotheses, conclusion, degenerate cases,
expression fingerprint, checked transports, and mutation tests required by section 5.1 of the
rev-5.6 standard cannot truthfully be produced. The legacy
`AwesomeTheorems.Stage1.S1_M_045.QuaternionicModuliStatementShape` does not cure this defect: its
order, level, functor, sheaf, and representation interfaces are explicitly lightweight locally
invented placeholders, and the intake crosswalk classifies it as discovery input rather than a
source-faithful formalization.

`StatementInfrastructure.lean` checks only the uncontroversial pinned API surface for a generic
quaternion algebra and schemes. It deliberately declares no canonical theorem, proof, axiom, or
proxy predicate.

## Environment fingerprint

- Repository base revision: `b11e1f5a1a404420eee7320a845fdb9df48bec0c`.
- Validation date: 2026-07-12.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin and checked revision:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Lean commands ran from `Formalizations/Lean` with the existing pinned `.lake` artifacts. No update,
fetch, clone, or build command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0126/StatementInfrastructure.lean` | 0 | generic quaternion-algebra and scheme infrastructure elaborated; two expected `#check` types printed |
| `lake env lean AwesomeTheorems/Stage1/S1_M_045.lean` | 0 | legacy discovery artifact elaborated, including its candidate statement shape; this is not exact-statement credit |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0126` | 0 | rank 45, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0126` | 0 | no whitespace errors |

## Retry condition

The authoritative lane must select a primary source and pinpoint theorem, including every arithmetic
and moduli assumption and the exact conclusion. The statement phase can then encode that claim with
minimal pinned imports, compare it against (or reject) the legacy candidate, and run removed-
hypothesis, changed-domain, binder-scope, and boundary mutations.

Until that input exists, the statement gate remains blocked at `M4`; statement acceptance and
theorem completion are both false. Because the assigned phase is not genuinely self-tested to its
completion gate, no `.stage1-worker-selftest.json` is emitted.
