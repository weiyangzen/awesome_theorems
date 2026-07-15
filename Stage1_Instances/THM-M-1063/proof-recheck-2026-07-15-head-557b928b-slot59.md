# THM-M-1063 proof recheck at current base

Item: `S56-M-1063-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T08:08:23+08:00`

Base revision: `557b928b377b386864527c9fb4831d45857837aa`

Base tree: `e677879a6eb4cb9d6795ba1bd78726af06ab9465`

## Verdict

`blocked`. The proof phase remains `[ ]`; no proof body or proof credit was added.

The exact root is the finite-second-moment Donsker principle in continuous path space.
`target_iff_expandedSourceShape` only unfolds its local definitions, and
`ObligationTree.exactRoot_of_exactRoot` assumes that complete root and returns it unchanged.
Neither is a proof of Donsker's theorem. All 29 machine-required frozen obligations still have
null terminal proof-body IDs, and neither the pinned Lake packages nor the audited external
candidates contain an exact placeholder-free Donsker or functional-CLT declaration.

This base does contain useful, newer repo-local substrate that earlier blocker summaries did not
identify. `Stage1_Instances/THM-M-0990/GeneralizedLindeberg.lean` supplies a checked eventual
triangular-array Lindeberg-Feller theorem, and `Stage1_Instances/THM-M-1013/Proof.lean` supplies a
checked Cramer-Wold theorem. Their isolated `--trust=0` replays passed and reported only `propext`,
`Classical.choice`, and `Quot.sound`. They can support `M1063-L-CLT` and `M1063-L-CRAMER` after
target-specific weighted-array and covariance adapters are proved, but they do not themselves have
either frozen THM-M-1063 type. `THM-M-1016` also demonstrates checked generic tight-measure APIs;
its tightness theorem starts from already established weak convergence and therefore cannot prove
the required path-law tightness without circularity.

The first logical unavailable package is `M1063-C-MEAS`: the target already receives each
`W n omega` as a bundled continuous map and an equality with `polygonalValue`, but the assumptions do
not directly supply `AEMeasurable (W n) P`, which is a field of the conclusion. Even after that
construction/interface issue, the substantive analytic cut remains finite-second-moment uniform
path tightness (`M1063-L-MAX`, `M1063-L-MODULUS`, `M1063-L-ASCOLI`, and `M1063-L-TIGHT`), followed
by subsequential extraction, continuous-path Brownian-law identification, and final
`TendstoInDistribution` composition. Assuming any of these packages, strengthening the moment
hypothesis, or substituting scalar or finite-dimensional convergence would change the frozen
theorem and is forbidden.

## Narrow evidence

All commands ran in this worker clone using the automation-provided untracked
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. Isolated auxiliary replays wrote
only to temporary directories under `/tmp`, which were removed on exit. No `lake update`,
`lake build`, dependency clone/fetch, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1,546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1,546 unique targets, ranks 1 through 1,546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1063` | 0 | Rank 506; planned lifecycle; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1063/check_obligation_tree.py` | 0 | 31 obligations and 125 typed edges passed; denominator `a55c3e2...26a7703`; root open at M4. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/DonskerTarget.lean` | 0 | Exact target and definitional expansion elaborated; output identified `DonskerInvariancePrinciple : Prop`. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/ObligationTree.lean` | 0 | Identity interface elaborated; its complete Donsker input and output are definitionally equal. |
| `cd Formalizations/Lean && lake env lean --trust=0 ../../Stage1_Instances/THM-M-1063/AnchorAudit.lean` | 0 | Scalar CLTs and generic convergence anchors resolved; reported axioms were only the three allowed foundations above. |
| pinned-package Donsker/FCLT source scans | 1 | Expected no-match exits; no pinned package contains a topical Lean declaration. |
| prohibited-construct scan over owned Lean sources | 1 | Expected no-match exit; no placeholder, bodyless declaration, unsafe/oracle, or native proof shortcut was found. |
| scoped JSON assertion over `obligation-registry.json` | 0 | 31 obligations, 29 machine-required, and all 29 required terminal proof-body IDs are null. |
| `bash Stage1_Instances/THM-M-0990/check_proof.sh` | 0 | Nine isolated modules elaborated with `--trust=0`; 24 target declarations, including `eventualLindebergFeller_exact`, reported exactly the allowed axiom set. |
| isolated `--trust=0` replay of `THM-M-1013/{Statement,Proof}.lean` | 0 | `Proof.cramerWold` and all three supporting declarations elaborated with exactly the allowed axiom set. |
| `TMPDIR=/tmp bash Stage1_Instances/THM-M-1016/check_proof.sh` | 0 | Seven delta-method/tightness declarations elaborated with exactly the allowed axiom set; this is API-pattern evidence only. |
| `cd Formalizations/Lean && lake env lean --version && lake --version` | 0 | Lean 4.29.0 at `98dc76e...`; Lake 5.0.0-src. |
| pinned mathlib revision/tree check | 0 | Clean revision `8a178386...`, tree `bdc39a3...`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test deliberately absent because the proof deliverable is incomplete. |

One exploratory direct invocation of `GeneralizedLindeberg.lean` exited 1 before elaboration because
the repo-root `Stage1_Instances` namespace was not on `LEAN_PATH`. The documented isolated replay
above supplied that local module tree and passed; no failed command was credited as proof evidence.

## Boundary and retry condition

Lifecycle stays `planned`; `audit_complete=false` and `theorem_complete=false`. The root vector
stays `[H2, M4, R4]`, with no accepted receipt IDs or proof-phase delta. This current-base artifact
is nonrelease blocker evidence, not a proof receipt. It does not satisfy `S56-M-1063-PROOF`, alter
scheduler state, or support master acceptance.

Resume after implementing the frozen path-valued measurability, finite-second-moment tightness,
subsequential limit identification, Brownian-law uniqueness, and final composition packages, while
using the now-checked triangular-array CLT and Cramer-Wold bodies where their exact types apply; or
after an immutable exact Lean 4 Donsker proof becomes available for pinned integration. Because
the assigned proof phase is incomplete, `.stage1-worker-selftest.json` is deliberately absent.
