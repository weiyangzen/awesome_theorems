# Statement gate blocker

Item: `S56-M-0546-STATEMENT`
Theorem: `THM-M-0546`
Claim order: `(v2 rank 323, phase layer 1, S56-M-0546-STATEMENT)`
Worker verdict: `blocked`; `phase_accepted=false` and no exact canonical Lean target is claimed.

## First failed gate

The authoritative metadata identifies only "Poincare duality" and "homological duality for
manifolds." It does not select coefficients, an orientation convention or local system,
compactness, connectedness, the treatment of boundary, the homology theory, grading conventions,
or the direction of cap product. These choices distinguish the closed orientable theorem from
local-coefficient, noncompact/compact-support, and Poincare-Lefschetz variants. The accepted intake
therefore left the canonical claim null and explicitly assigned this phase the unresolved variant
decision.

Hatcher, *Algebraic Topology* (2002), Theorem 3.30, page 241 is recorded only as a candidate: for a
closed `R`-orientable `n`-manifold, cap product with its fundamental class gives isomorphisms from
degree-`k` cohomology to degree-`n-k` homology. The dossier has no immutable primary-source receipt
or inspected coefficient conventions that would authorize promoting this candidate to the exact
root. Selecting it now would invent a statement decision rather than elaborate an already frozen
claim.

There is also no faithful way to encode that candidate using the pinned mathlib API. A scoped
source search found singular homology and boundaryless-manifold infrastructure, but no singular
cohomology, cap product, manifold orientation system, or fundamental-class declaration at the
required shape. The legacy `AwesomeTheorems.Stage1.S1_M_107.StatementShape` is not a substitute: it
existentially quantifies arbitrary `Homology` and `Cohomology` families, and its data structure
stores both the desired isomorphism proposition and a proof of that proposition. Reusing it would
hide rather than state Poincare duality and is prohibited by the exact-statement gate.

Consequently the ordered binders, exact hypotheses and conclusion, expression fingerprint,
checked transports, and hypothesis/boundary mutation tests required by rev-5.6 cannot truthfully
be frozen. The contract-selected `Statement.lean` is deliberately declaration-free, while
`StatementInfrastructure.lean` checks only adjacent APIs. Neither file declares a canonical
theorem, axiom, proxy predicate, or proof.

## Dependency and reuse closure

The authoritative theorem DAG has no direct hard parent, transitive hard ancestor, hard edge,
reuse hint, or shared lemma group for this target. Its exact `parent_inspection_order` is therefore
empty and was traversed exactly once before statement work. The target-owned
`dependency-reuse-ledger.json` binds graph SHA-256
`e8472863a24609e37868f215bbf0e0654b11a62f912a403ebca5feb8de5a3b9b` and context SHA-256
`068170c76abd4579d643ede04d731b974412185bd285e7b40255ec4044adec5c` with empty inspections,
decisions, and unresolved compatibility obligations. No provider bytes, receipt, declaration,
checkbox state, acceptance, or proof credit are consumed. The empty declared graph context is not
a mathematical-independence claim.

## Environment fingerprint

- Repository base revision: `1cc6aa61bb055a5c032297ee457905c849af7608`.
- Repository base tree: `dc3053b55c5724ccb2e6a247e7deffebca9dbb99`.
- Validation date: 2026-07-17.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin and checked revision:
  `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Lean commands ran from `Formalizations/Lean` using the existing canonical pinned `.lake`
artifacts. No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0546/Statement.lean` | 0 | declaration-free contract-selected boundary elaborated with empty stdout and stderr; no statement credit |
| `LC_ALL=C TZ=UTC lake env lean --trust=0 ../../Stage1_Instances/THM-M-0546/StatementInfrastructure.lean` | 0 | pinned singular-homology and boundaryless-manifold API probes elaborated; stdout SHA-256 `4d14ccd0fc7ef066d2c0f833f00d9b8f1f651d2a419feca841d2275642bda08a` |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets, v2 theorem DAG, phase contract, and execution skill passed before target-owned inventory additions |
| `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 0 | 1546 theorems, 10822 phase states, declared graph acyclic before target-owned inventory additions |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0546` | 0 | rank 107, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `python3 Docs/tools/check_stage1_phase_acceptance_contracts.py` | 0 | seven phases, twelve common gates, and twenty-three source references passed |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0546/check_statement.py` | 0 | one typed JSON object reports `status=blocked`, `phase_accepted=false`, and `phase_predicate_proven=false` |
| final `python3 Docs/tools/check_stage1_standard.py` | 1 | expected post-edit mismatch: the target-owned evidence inventory changed while the worker is forbidden to regenerate the read-only theorem DAG |
| final `python3 Docs/tools/check_stage1_theorem_dag_v2.py` | 1 | expected post-edit mismatch: checked-in theorem DAG differs from fresh deterministic generation; master regeneration is required |
| `git diff --check -- Stage1_Instances/THM-M-0546` | 0 | no whitespace diagnostics |
| scoped forbidden-construct scan over target Lean sources | 1 (expected no match) | no `sorry`, `admit`, `sorryAx`, axiom, opaque, unsafe, native-decide, or implementation escape hatch |

## Retry condition

The authoritative lane must freeze a pinpoint primary-source statement and all variant choices.
The selected Lean dependency set must then provide, or the project must first implement, the
concrete (co)homology, cap-product, orientation, and fundamental-class interfaces needed to express
that statement without assuming its conclusion. Only then can this node elaborate and fingerprint
the exact target and run meaningful mutations.

Until those inputs exist, the root remains `M4`; statement acceptance and theorem completion are
false. The worker handoff records only that this target-scoped negative packet was self-tested. A
validator exit of zero does not satisfy the positive statement predicate and does not transfer
master acceptance.
