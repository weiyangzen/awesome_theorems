# THM-M-0419 proof-phase attempt

Item: `S56-M-0419-PROOF`

Intent: `prove`

Base revision: `c15c649568664c4e58150dd755cb28f156d15ecb`

Base tree: `792c3ed97f9263da7e6a39abdce8d5e37a100368`

Recorded: 2026-07-15 16:30:00 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target remains `Stage1.THM_M_0419.Statement`: every number
field `K` that is abelian Galois over `Q` embeds over `Q` into some
`CyclotomicField n Q` with `n != 0`.

The first failed gate is `M0419-B-INDUCTION`. No placeholder-free body
inhabits `LocalInductionPackage`, which must strong-induct on local degree and
recombine complementary proper fixed fields through a common local
cyclotomic compositum. Independently, no body inhabits any of the tame,
odd-wild, or 2-adic-wild cyclic branch packages, and no body inhabits
`GlobalizationPackage`. The frozen minimal open proof cut is therefore:

```text
M0419-B-INDUCTION
M0419-L-TAME
M0419-L-WILD-ODD
M0419-L-WILD-TWO
M0419-T-GLOBAL
```

`ObligationTree.lean` contains real checked bodies for branch exhaustiveness,
positive-index transport, and conditional local/root composition. Every
substantive input stays explicit. In particular, `root_of_packages` consumes
local containment and globalization packages; it constructs neither.
Returning it would substitute a conditional theorem for the exact root, and
declaring one of the missing packages as an axiom or bodyless constant would
be a prohibited placeholder.

Pinned mathlib does provide useful substrate: cyclotomic fields, the easy
abelian-Galois direction, p-adics, fixed fields, conductor and ramification
APIs, and an equivalence between two singleton cyclotomic extensions. It does
not provide the local Kronecker-Weber branches or the global
completion/conductor/inertia bridge. The only audited terminal-shaped external
candidate, `facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`,
contains 22 `sorry` occurrences, including its conductor and inertia/embedding
bridges. It receives zero proof credit.

No proof body, proof receipt, obligation closure, dependency, authoritative
cursor, or frozen graph was changed. Lifecycle stays `planned`; the accepted
root vector stays `[H1, M3, R3]`; `audit_complete=false` and
`theorem_complete=false`. Because the assigned proof deliverable is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone using the existing pinned Lake closure.
The automation-provided untracked `Formalizations/Lean/.lake` symlink was
reused read-only. No `lake update`, `lake build`, dependency clone/fetch,
checkout, network request, or `.lake` mutation ran. Temporary Lean artifacts
were created under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0419` | 0 | Rank 74; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0419/check_anchor_audit.py` | 0 | The negative boundary, 13 Lean probes, mathlib pin, and external placeholder classification agree. |
| `python3 -B Stage1_Instances/THM-M-0419/check_obligation_tree.py` | 1 | The historical prerequisite validator is stale: it hardcodes its original worker base `80f0191c...`, so it rejects current integrated base `c15c6495...` before reaching its former ephemeral self-test-packet check. No pass is claimed. |
| Isolated `lake env lean --trust=0 -t0` replay described below | 0 | `Statement.lean` and `ObligationTree.lean` elaborated. Every conditional declaration reported exactly `propext`, `Classical.choice`, and `Quot.sound`; no root body was introduced. |
| Prohibited-construct scan over owned `*.lean` | 1 expected | No `sorry`, `admit`, `sorryAx`, `native_decide`, axiom/bodyless constant, unsafe/opaque declaration, external implementation, or `implemented_by` marker. |
| Bounded repo-local and pinned-source terminal/package search | 0/1 expected | No additional inhabitant of an open package and no terminal Kronecker-Weber converse were found. The broad alias search produced only unrelated contextual matches. |
| Environment, pin, status, and frozen-input hash inspection | 0 | Lean `4.29.0` (`98dc76e3...6740`), Lake `5.0.0-src+98dc76e`, mathlib `8a178386...ea95` tree `bdc39a31...c2b`, and flt-regular `56161b6e...a27`; both dependency worktrees were clean. |
| `python3 -m json.tool Stage1_Instances/THM-M-0419/proof-blocker.json`; `test ! -e .stage1-worker-selftest.json` | 0 | The blocker packet parses, and no completion self-test manifest exists. |
| Scoped tracked and new-file `git diff --check` | 0 | No whitespace diagnostics; the two no-index checks returned the expected new-file difference status. |

The isolated replay ran from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-0419
tmp=$(mktemp -d /tmp/thm-m-0419-proof-attempt.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$lean_path" timeout 180 "$lean" --trust=0 -t0 \
  -o "$tmp/Statement.olean" Statement.lean
LC_ALL=C LANG=C TZ=UTC NO_COLOR=1 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean" --trust=0 -t0 \
  ObligationTree.lean
```

The captured statement output SHA-256 was
`d30ce90a242e9fe3900ec73e893184ad8878c5b90f5362a4f70ca3846342faeb`.
The obligation output SHA-256 was
`043ffeecbbd1d4b2f7574df4f0f23210d621e68982a2dab5d43773224b695a71`.

## Retry Condition

Resume after placeholder-free implementations of the five minimal-cut
packages and their frozen dependencies exist in the pinned closure, or after
an immutable, compatible, lawfully reusable no-placeholder Lean 4 terminal
proof can be pinned/imported, exactly transported to the unchanged target, and
checked. Until then this item stays `[ ]`; validation, release, master
acceptance, `AUDIT-Z`, and `THEOREM-Z` remain open.
