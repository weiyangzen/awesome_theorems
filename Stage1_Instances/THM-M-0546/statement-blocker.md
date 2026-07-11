# Statement gate blocker

Item: `S56-M-0546-STATEMENT`
Theorem: `THM-M-0546`
Verdict: blocked; no exact canonical Lean target is claimed.

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
be frozen. `StatementInfrastructure.lean` deliberately declares no canonical theorem, axiom,
proxy predicate, or proof.

## Environment fingerprint

- Repository base revision: `9e3fd02a2a952da7031bb1dd61387443dd4c1cc7`.
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

Lean commands ran from `Formalizations/Lean` using the existing canonical pinned `.lake`
artifacts. No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| initial `lake env lean ../../Stage1_Instances/THM-M-0546/StatementInfrastructure.lean` | 1 | probe types printed, but doc comments immediately before commands were rejected; comments were corrected before the evidentiary rerun |
| `lake env lean ../../Stage1_Instances/THM-M-0546/StatementInfrastructure.lean` | 0 | pinned singular-homology and boundaryless-manifold API probes elaborated; their types printed |
| `lake env lean AwesomeTheorems/Stage1/S1_M_107.lean` | 0 | legacy discovery artifact elaborated; this supplies neither exact-statement nor proof credit |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json` | 0 | hashes match the environment fingerprint above |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0546` | 0 | rank 107, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0546` | 0 | no tracked diff output; owned additions were still untracked |
| scoped whitespace check over both new owned files, plus forbidden-declaration-token check over the Lean file | 0 | no trailing whitespace; Lean probe contains no prohibited declaration or proof token |

## Retry condition

The authoritative lane must freeze a pinpoint primary-source statement and all variant choices.
The selected Lean dependency set must then provide, or the project must first implement, the
concrete (co)homology, cap-product, orientation, and fundamental-class interfaces needed to express
that statement without assuming its conclusion. Only then can this node elaborate and fingerprint
the exact target and run meaningful mutations.

Until those inputs exist, the root remains `M4`; statement acceptance and theorem completion are
false. Because the assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
