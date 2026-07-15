# THM-M-0113 proof-phase blocker at `e57cfb09`

Item: `S56-M-0113-PROOF`

Intent: `prove`

Recheck time: `2026-07-15T20:02:10+08:00` (`Asia/Shanghai`)

Base revision: `e57cfb0904e8a827b17320aba51bd41b96109c7c`

Base tree: `79ab3544eee575a45c51d85923144ed20f607f9e`

## Verdict

`blocked`. No legal positive proof body can inhabit the exact frozen target.
The existing placeholder-free declaration

```text
Stage1Instances.THMM0113.not_hodgeDecompositionTarget :
  Not Stage1Instances.THMM0113.HodgeDecompositionTarget.{0, 0, 0, 0}
```

freshly kernel-checks at trust level zero against an isolated elaboration of
`Statement.lean`. Any universe-polymorphic positive proof would specialize to
this refuted universe instance.

The defect is in the frozen interface. `HodgeData.isKahler` is an unconstrained
proposition and does not relate the geometric hypothesis to the independently
chosen `cohomology` family or `hodgePiece` submodules. The countermodel uses
the zero-dimensional compact complex manifold `Fin 0 -> Complex`, sets
`isKahler := True`, interprets every cohomology space as `Complex`, and makes
every Hodge piece bottom. Complex conjugation supplies the required additive,
conjugate-linear, and involutive laws. In degree zero, the target would force
the supremum of bottom submodules to be top and hence force `1 = 0`.

This refutes the frozen abstract encoding, not the mathematical Hodge
decomposition theorem. Repairing or narrowing `Statement.lean` inside this
proof item would substitute a different theorem and invalidate its predecessor
chain. The checked negative declaration therefore gives no positive-root proof
credit.

The proof item remains `[ ]`. No proof receipt, state transition, audit
completion, theorem completion, validation completion, release, or master
acceptance is claimed. `.stage1-worker-selftest.json` is deliberately absent
because the requested positive proof phase is not complete.

## Failed Gates

The first failed gate is
`S56-5.1-EXACT-TARGET-CONSISTENCY / M0113-S-DATA`. The actionable cut set is
the disconnected data interface. The frozen graph also records the planned
analytic leaves `M0113-A-DR`, `M0113-A-DOL`, `M0113-A-ELL`, `M0113-K-ID`, and
`M0113-C-CHAIN`, but proof execution cannot truthfully enter that architecture
while the root admits the checked countermodel.

The statement predecessor also lacks the required mutation evidence. Its
fixtures elaborate alternate propositions rather than demonstrating that the
required non-equivalent mutations fail, and `MutationRemovedCompactness` still
binds `[CompactSpace M]`.

The obligation-tree prerequisite remains provisional `[_]`, not master-
accepted `[x]`, so dependency-legal positive acceptance is independently
unavailable.

Before this run, the target already contained 46 integrated structured proof
recheck pairs, while the scheduler authority still recorded `attempts: 0` and
no children. Those files are not the authoritative tick counter, but they show
that the same blocker has been dispatched far beyond the five-unresolved-tick
limit in section 10.2. The master must reconcile attempts and split or redirect
the item rather than reschedule the unchanged false root.

## Validation

All Lean checks reused the existing pinned toolchain and read-only automation
symlink to canonical Lake artifacts. No `lake update`, `lake build`, dependency
clone/fetch, network command, or `.lake` mutation occurred. Lean output was
confined to a fresh directory under `/tmp` and removed by a shell trap. The
external `.lake` symlink makes this narrow nonrelease evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0113` | 0 | Rank 25; lifecycle `planned`; baseline `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0113/check_anchor_audit.py` | 0 | Target boundary, four candidate rows, 12 Lean probes, and pinned mathlib revision agree. |
| `python3 Stage1_Instances/THM-M-0113/check_obligation_tree.py` | 0 | `PASS`: 26 obligations and 49 typed edges; denominator `e509c192...cbd5`; the frozen graph root remains M4. |
| Isolated `lake env lean` recipe below | 0 | Statement and countermodel elaborated at trust level zero. Lean printed the exact negation and axioms `[propext, Classical.choice, Quot.sound]`. Statement-output SHA-256 `483a37eb...7e84`; proof-output SHA-256 `ee6378a7...2d4c`; `Statement.olean` SHA-256 `94fe8a21...75e0`. |
| Scoped prohibited-declaration scan | 1 | Expected no-match: no placeholder, bodyless declaration, unsafe declaration, `implemented_by`, or `extern` occurs; the axiom report contains no `sorryAx`. |
| Lake-manifest package checkout audit | 0 | All 11 package worktrees matched their recorded revisions and were tracked-clean; mathlib was `8a178386...a95`. |
| `python3 -m json.tool <current blocker JSON> >/dev/null` | 0 | The structured current-base blocker packet is valid JSON. |
| Current-base invariant assertions | 0 | Item/base identity, source hashes, exact checked negation, empty receipts, open state, dependency state, and deliberate self-test absence agree. |
| Scoped tracked and added-file whitespace assertions | 0 | `git diff --check` exited 0. Both `git diff --no-index --check /dev/null <addition>` commands had expected diff-present exit 1 with no whitespace diagnostic. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The incomplete proof phase emitted no worker-completion packet. |

The isolated Lean replay, run from the repository root, was:

```bash
set -euo pipefail
ROOT=$PWD
LEAN_ROOT=$ROOT/Formalizations/Lean
TMP=$(mktemp -d /tmp/thm-m-0113-proof-recheck-heade57cfb09-slot12.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
cp Stage1_Instances/THM-M-0113/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-0113/Proof.lean "$TMP/Proof.lean"
BASE_PATH=$(cd "$LEAN_ROOT" && timeout --foreground 600 \
  lake env printenv LEAN_PATH)
(cd "$LEAN_ROOT" && \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$BASE_PATH" timeout --foreground 600 lake env lean \
  --trust=0 -t0 --root="$TMP" -o "$TMP/Statement.olean" \
  "$TMP/Statement.lean" >"$TMP/statement-output.txt" 2>&1)
(cd "$LEAN_ROOT" && \
  ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 \
  LEAN_PATH="$TMP:$BASE_PATH" timeout --foreground 600 lake env lean \
  --trust=0 -t0 --root="$TMP" "$TMP/Proof.lean" \
  >"$TMP/proof-output.txt" 2>&1)
cat "$TMP/statement-output.txt" "$TMP/proof-output.txt"
sha256sum "$TMP/statement-output.txt" "$TMP/proof-output.txt" \
  "$TMP/Statement.olean"
```

The scoped prohibited-declaration scan was:

```bash
rg -n --pcre2 \
  '\b(?:sorry|admit|sorryAx|native_decide)\b|^[[:space:]]*(?:axiom|constant|opaque|unsafe)[[:space:]]|implemented_by|extern[[:space:]]' \
  Stage1_Instances/THM-M-0113 --glob '*.lean'
```

Its exit code was 1, the expected no-match result. Lean's printed axiom
dependency report is the kernel-derived trust evidence for the countermodel.

## Retry Condition

Do not reschedule the unchanged positive root. Replace the disconnected
`isKahler` proposition and arbitrary cohomology/Hodge-piece fields with native
definitions tied to the compact complex manifold, or add noncircular
law-bearing hypotheses. Repair the mutation evidence, publish a new target
fingerprint, and freshly freeze and accept the statement, anchor audit,
obligation registry, and typed graphs before proof execution resumes.
Alternatively, explicitly redirect this item to the checked counterexample
target. The master must also reconcile attempts and perform the section 10.2
split or redirection.

This is current-base target-scoped blocker evidence, not a proof receipt.
