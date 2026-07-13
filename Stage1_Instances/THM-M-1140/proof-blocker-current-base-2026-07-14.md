# THM-M-1140 proof-phase current-base blocker

Item: `S56-M-1140-PROOF`  
Intent: `prove`  
Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`  
Base tree: `bd58be98bf3046078c016d44fb4a677ea231cb23`  
Recheck date: 2026-07-14 (Asia/Shanghai)

## Verdict

`blocked`. The exact assigned proof phase remains open. The existing source has a genuine,
placeholder-free proof of `ConnectedLevelPropagation`, and the checked theorem
`harmonicStrongMaximumPrinciple_of_packages` composes that result with a supplied
`InteriorLocalRigidity`. It does not construct the latter package. No proof body or eligible pinned
import was found for `InteriorLocalRigidity`, so the exact root remains `[H2, M3, R3]` and this item
remains `[ ]`. This record makes no proof-completion, validation, release, or master-acceptance
claim.

The root quantifies over every `n : Nat`: a real `HarmonicOnNhd` function on a nonempty connected
open subset of `EuclideanSpace Real (Fin n)` that attains a maximum at an interior point is constant
on the domain. The first missing cut is `M1140-L-MEAN-VALUE / M1140-T-LOCAL-PACKAGE`, an
arbitrary-dimensional harmonic local-rigidity theorem. Specializing to the complex plane, assuming
local rigidity, or returning only the conditional composition would change or leave open the
frozen target.

## Fresh Candidate Recheck

The pinned mathlib tree at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains general
finite-dimensional harmonic definitions, regularity, continuity, and algebraic closure, but no
general mean-value, harmonic-to-real-analytic, unique-continuation, local-rigidity, or strong-maximum
theorem. Its nearby `HarmonicAt.analyticAt` and `HarmonicOnNhd.circleAverage_eq` declarations have
domain `Complex`, so they cannot discharge the root's universal Euclidean-dimension binder.

A fresh public Lean search found `facebookresearch/atlas-lean` at immutable revision
`34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its
`Atlas/IntroductionToPartialDifferentialEquations/code/CM7/LaplaceProperties.lean` defines a general
`strong_max_principle` from a volume mean-value premise. However, the harmonic-to-mean-value chain
on which its harmonic applications depend contains eight `by sorry` declarations, including the
divergence/average bridges at lines 763, 773, 817, 829, 1020, 1152, and 1162. The file also declares
two opaque analytic objects, and the repository license is CC BY-NC 4.0 with a no-training rider.
Therefore this newly discovered source is neither an eligible terminal proof body nor a dependency
that may be copied, pinned, or credited. No external dependency was installed, fetched into Lake,
or added to this repository.

## Validation

All Lean checks reused the automation-provided canonical `.lake` link read-only. Source copies and
olean output were confined to a fresh `/tmp` directory and removed by a shell trap.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1140` | 0 | Rank 345; lifecycle `planned`; theorem incomplete |
| isolated `lake env lean` trust-zero recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated; both proof declarations reported exactly `propext`, `Classical.choice`, and `Quot.sound` |
| `python3 Stage1_Instances/THM-M-1140/check_obligation_tree.py` | 0 | 16 obligations and 36 typed edges passed; frozen root remains open at `M3` |
| scoped prohibited-construct scan of the three local Lean modules | 1 | Expected no-match: no `sorry`, `admit`, `axiom`, `unsafe`, or `sorryAx` declaration |
| pinned-package search for harmonic maximum/local-rigidity/analytic bridges | 0/1 | No exact general proof body; only complex-plane mean-value and analyticity results |
| isolated `exact?` search after `import Mathlib` against the exact root | 1 | `exact? could not close the goal. Try apply?`; no full-environment mathlib proof term was found |
| Sourcegraph public Lean queries for strong maximum and harmonic mean-value declarations | 0 | The only new general candidate was the Atlas file described above |
| immutable Atlas source scan for `sorry`, `admit`, `axiom`, `unsafe`, `opaque`, or `sorryAx` | 0 | Eight `by sorry` bodies and two opaque declarations found; candidate rejected |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1140
tmp=$(mktemp -d /tmp/thm-m-1140-proof-slot49.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$tmp/Statement.lean"
cp "$target/ObligationTree.lean" "$tmp/ObligationTree.lean"
cp "$target/Proof.lean" "$tmp/Proof.lean"
cd "$tmp"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" "$lean" --trust=0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" "$lean" --trust=0 Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry Condition

Resume positive proof work only after a placeholder-free implementation of arbitrary-dimensional
harmonic local rigidity, or discovery of an immutable, license-compatible Lean 4 terminal theorem
whose complete transitive proof closure can be pinned, exact-type transported, provenance-audited,
and kernel-checked without changing the frozen target.

Because the assigned proof phase is not genuinely complete, `.stage1-worker-selftest.json` is
deliberately absent. This owned artifact is blocker evidence only.
