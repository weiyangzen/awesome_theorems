# THM-M-0579 proof-phase recheck at base 11a448c9

Item: `S56-M-0579-PROOF`

Intent: `prove`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `11a448c97289d30fe7c8c05dbac5a283a9d00896`

Base tree: `a79f60552d328e98302026909ec6676cb6cd6ea2`

## Verdict

`blocked`. The exact proposition `Stage1Instances.THMM0579.Statement` is the
full topological three-dimensional Poincare theorem. Neither this repository
nor its pinned Lean dependency closure contains an eligible retained proof
body. This attempt adds no proof body. The item stays `[ ]`, lifecycle stays
`planned`, the root vector stays `[H3, M3, R4]`, and audit and theorem
completion remain false. Because the requested proof phase is not complete,
`.stage1-worker-selftest.json` is intentionally absent.

The first failed gate is terminal proof-body availability. The frozen immediate
root cut contains `M0579-T-RECOGNITION` and `M0579-T-RIGIDITY`, both `M4`.
Their checked assembly theorem accepts these packages as premises; it does not
inhabit either package. Recognition still expands through open smoothing,
prime normalization, Ricci flow, surgery control, analytic estimates, finite
extinction, and recomposition packages.

The trust-zero `ProofBlockerProbe.lean` proves

```text
(HomotopySphereRecognition and HomotopySphereTopologicalRigidity) iff Statement
```

The root gives recognition via `Homeomorph.toHomotopyEquiv` and gives rigidity
by ignoring its extra homotopy-equivalence premise. Consequently, the current
immediate cut is root-equivalent rather than a difficulty-reducing proof
decomposition. This worker did not alter the frozen obligation architecture.

Pinned mathlib contains matching signatures only as Batteries `proof_wanted`
source markers. Batteries elaborates those temporary declarations under
`withoutModifyingEnv`, so importing the module retains none of their names. The
permanent probe checks all three names with `#check_failure`; each reports
`Unknown constant`. The audited immutable external candidates contain either a
three-dimensional statement with an unrelated dimension-zero proof or an
explicit `sorry` body. Neither can receive proof credit.

## Validation

All commands used only existing pinned artifacts. Lean outputs were placed in
a disposable `/tmp` directory and removed. No `lake update`, `lake build`,
dependency clone/fetch, checkout, or `.lake` mutation was performed. The
automation-provided untracked `.lake` symlink was reused read-only, so this is
nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0579` | 0 | Rank 114; planned hard-mathlib lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-0579/check_obligation_tree.py` | 0 | 16 obligations and 34 typed edges passed; denominator `984bcfffcea5afa7c11e3f2eb78ad31c2eed6b99e1a0913496186ceb1595776f`; root M3 and both cut packages M4 |
| `python3 Stage1_Instances/THM-M-0579/check_anchor_audit.py` | 0 | Frozen target, five candidates, discarded `proof_wanted` boundary, dependency pins, and noncompletion status agreed |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| Isolated `lake env lean --trust=0` replay | 0 | `Statement.lean`, `AnchorAudit.lean`, `ObligationTree.lean`, and `ProofBlockerProbe.lean` elaborated against existing pinned artifacts |
| `#print axioms root_of_recognition_and_rigidity` | 0 | `[propext, Classical.choice, Quot.sound]` |
| `#print axioms immediate_cut_iff_statement` | 0 | `[propext, Classical.choice, Quot.sound]` |
| Three trust-zero `#check_failure` probes | 0 | The generalized, topological-three, and smooth-three matching mathlib names each reported `Unknown constant` |
| Scoped retained-declaration search | 1 | Expected no-match across the owned dossier, repository Lean source, pinned mathlib, and pinned Batteries |
| Prohibited-construct scan | 1 | Expected no-match across the four checked owned Lean modules |
| Frozen-input diff against `ed959a5a` | 0 | All eight proof inputs plus the toolchain and dependency manifest are unchanged since the latest prior recheck |
| `git diff --check` before writing the blocker record | 0 | No whitespace errors |
| `python3 -m json.tool Stage1_Instances/THM-M-0579/proof-recheck-2026-07-15-head-11a448c9.json >/dev/null` | 0 | The current-base machine-readable blocker record parsed successfully |
| `jq -e` current-base blocker invariants | 0 | Item, theorem, base, blocked state, noncompletion flags, absent proof body, and changed-path count agreed |
| `git diff --check` after writing the blocker artifacts | 0 | No whitespace errors |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is absent because this proof item remains blocked |

The exact isolated replay recipe from the repository root was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0579
tmp=$(mktemp -d /tmp/thm-m-0579-proof-slot20-11a448c9.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/AnchorAudit.olean" AnchorAudit.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/ObligationTree.olean" ObligationTree.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  -o "$tmp/ProofBlockerProbe.olean" ProofBlockerProbe.lean
```

The proof-relevant hashes are:

```text
Statement.lean              307061f5847f145fb8cb4e91116ed8ab0c76e3ddc0e9301486fd879be1cf3de8
AnchorAudit.lean            40a767ff49b55bcbfccc9455cec77ae7878476b64b0cecd36dfe639fb2c3550f
ObligationTree.lean         f5214263374c23fd2f235cdf4d06bc9cadfd50d4abbe41de32dd55a7e35f0c63
ProofBlockerProbe.lean      e4bc1b79c8e1525b8bf8f7f8edceeb95be6cd95251aa1e69f6052b32618541a3
obligation-registry.json    8b70a187e8d4e071c3a658f8b5d8d31fb78dcb2fabc1bedeeddca3fd4c62b31a
typed-graphs.json           e8a756448de68ee250734fc480a06bd3fc55f1827f6da5a847b6bd31677ddce7
anchor-audit.json           0285a80d4d59466d71fdd1d163e1c6a09f7a96b1d0372ea8f682fd69c251f7e7
validation-specs.json       353bdfdcd8341bbd3b3c324b634804144b119ed0b8d0ed161e28d222074aa
```

## Retry Condition

Implement the frozen missing packages locally without placeholders, or
integrate a licensed immutable compatible Lean 4 proof with exact transport and
complete kernel, composition, provenance, axiom, trust, and pinned-replay
evidence. A future obligation-tree revision should replace the tautological
immediate cut with non-tautological executable contracts before route-based
proof execution.

Assuming a package, treating `proof_wanted` as a theorem, importing a
placeholder candidate, or proving a conditional or special case would
substitute a different theorem. These artifacts are blocker evidence, not a
proof receipt. They do not satisfy `S56-M-0579-PROOF`, change scheduler state,
or claim audit completion, theorem completion, release, or master acceptance.
