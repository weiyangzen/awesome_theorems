# THM-M-1234 proof-phase recheck at `fb0fd5be`

Item: `S56-M-1234-PROOF`

Recheck date: `2026-07-15` (`Asia/Shanghai`)

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## Verdict

`blocked`. The exact target `Stage1Rev56.THMM1234.Statement` has no proof body
in the owned source or pinned dependency closure. This recheck adds no proof
body and closes no obligation. The lifecycle remains `planned`, and the root
vector stays `[H1, M3, R3] -> [H1, M3, R3]`.

The direct frozen root cut remains `M1234-A-STRUCTURE` plus
`M1234-E-CLOSURE`. Its first expanded failed gate is `M1234-A-APPROX`: there
is no checked construction of smooth global Euler approximants for every
`InitialData` witness. Uniform energy and vorticity estimates,
nonlinear-compatible compactness, structure preservation, linear and
quadratic momentum limit passage, and the one-sided initial trace also remain
open.

The checked local bodies are narrower than the root. The theorem
`root_of_construction_and_closure` consumes two explicit package premises.
The formal `CandidateConstructionPackage` is inhabited by constant-in-time
initial fields, but that under-specified interface consumes none of the three
analytic children required by the frozen graph. Its trace theorem applies
only to that candidate. The zero-field construction proves only the strict
zero-data boundary case. Constant initial fields do not establish the
arbitrary-data nonlinear weak momentum identity, and zero fields cannot meet
the arbitrary initial pairing and vorticity trace.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_158.lean` contains
statement, package, and audit interfaces and explicitly records
noncompletion. The pinned mathlib source search found no Yudovich theorem,
and the predecessor immutable anchor audit found no exact external terminal
body eligible for pinned import.

## Failed Gate And Retry

The first failed gate is `M1234-A-APPROX`. Resume only after an accepted repair
of the under-specified child-consuming interfaces and placeholder-free bodies
for smooth approximation, uniform estimates, nonlinear-compatible compactness,
momentum limit passage, and initial trace. An immutable exact Lean 4 terminal
body could instead be pinned and checked for exact type and provenance.
Assuming a package, adding an axiom, or substituting the zero-data case is not
eligible.

## Validation

All checks ran in this worker clone against the existing pinned Lake artifacts.
The pre-existing untracked `Formalizations/Lean/.lake` symlink was reused
read-only. No `lake update`, `lake build`, dependency clone/fetch, network
access, or `.lake` mutation was performed. Temporary Lean objects were removed
after the replay.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1234` | 0 | Rank 158; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1234/check_obligation_tree.py` | 0 | 14 obligations and 28 typed edges passed; denominator `cfa0a02c...34c5d`; root open at M3. |
| Isolated trust-zero five-module Lean replay below | 0 | `Statement.lean`, `AnchorAudit.lean`, `ObligationTree.lean`, `ConstructionProof.lean`, and `Proof.lean` elaborated; printed proof declarations reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| Token-anchored prohibited-device scan over owned `*.lean` files | 1 | Expected no-match exit; no `sorry`, `admit`, declared axiom, unsafe/opaque/extern injection, `sorryAx`, `implemented_by`, or `native_decide`. |
| Exact-topic search in pinned mathlib Lean sources | 1 | Expected no-match exit for Yudovich, Yudovitch, incompressible Euler, and bounded vorticity. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`; tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |

The successful narrow Lean replay was:

```bash
set -euo pipefail
tmp=$(mktemp -d /tmp/thm-m-1234-proof-head-fb0fd5be.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
cp Stage1_Instances/THM-M-1234/{Statement,AnchorAudit,ObligationTree,ConstructionProof,Proof}.lean "$tmp"/
lean=$(cd Formalizations/Lean && lake env which lean)
lean_path=$(cd Formalizations/Lean && lake env printenv LEAN_PATH)
export LEAN_NUM_THREADS=1
cd "$tmp"
LEAN_PATH="$lean_path" timeout 600 "$lean" --trust=0 -t0 -o Statement.olean Statement.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 AnchorAudit.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 -o ObligationTree.olean ObligationTree.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 ConstructionProof.lean
LEAN_PATH=".:$lean_path" timeout 600 "$lean" --trust=0 -t0 Proof.lean
```

The replay produced `Statement.olean` SHA-256
`1709e38a5b8cc96159b7042585666cb84536b4b3d9e26a63697992cd9820d308`.
The paired JSON packet records all source and output hashes.

## Status Boundary

This is current-base nonrelease blocker evidence, not a proof receipt. It does
not satisfy `S56-M-1234-PROOF`, change task state, or claim audit completion,
theorem completion, validation, release, or master acceptance.
`accepted_receipt_ids=[]`. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.
