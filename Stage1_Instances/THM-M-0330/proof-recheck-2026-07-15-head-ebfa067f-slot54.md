# THM-M-0330 proof-phase blocker at `ebfa067f`

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T21:23:23+08:00` (`Asia/Shanghai`)

Base revision: `ebfa067f2385ca03cc0a0eeecf151993a994962c`

Base tree: `4d482bdb45ec4ff17c128d712608f7c7eea1ffc8`

## Verdict

`blocked`. No placeholder-free inhabitant of either exact direction package
exists in the repository or pinned dependency closure. No proof body was added,
the proof item remains `[ ]`, lifecycle remains `planned`, the frozen root
remains `[H3, M4, R4]`, and both audit completion and theorem completion remain
false. This is a target-scoped blocker and scheduler handoff, not a proof
receipt. The workspace-root `.stage1-worker-selftest.json` is deliberately
absent.

The exact root is
`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget`, expression SHA-256
`5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`.
Its minimal open cut remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

`root_of_direction_packages` is checked conditional composition from complete
`ForwardPackage` and `ConversePackage` arguments. It constructs neither.
`target_iff_expanded` is only definitional transport. A fresh exact-root `simp`
probe did not close the target; neither implication is vacuous or definitionally
true.

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`. The other open
proof obligations are generator closedness, Laplace/Bochner resolvent
construction, both inverse laws and the `1/a` estimate, bounded approximant
exponentials, uniform contraction, strong convergence, exact generator
identification, and both direction assemblies.

No exact child body can yet receive credit against most frozen leaves: their
`formal_target` fields are still `planned ...` descriptions and their statement
fingerprints are `planned:v1:*`, not elaborated contextual Lean propositions.
The scheduler must split this oversized task and a successor obligation-tree
phase must freeze exact child interfaces and composition certificates before
child proof execution.

The proof inputs and dependency pins are unchanged since their target-changing
commit `230f719d`. Repository history, duplicate target `THM-M-1041`, and legacy
`S1_M_234.lean` contain definitions, abstract interfaces, transports, or
conditional composition only. A current search over all `9676` Lean source
files in the pinned package cache found no Hille-Yosida or C0-semigroup
generator theorem.

The strongest immutable external candidate remains
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667`. The audited declarations cover
only parts of the forward resolvent route: they do not prove generator density
or closedness, the full-domain left inverse, or any converse generation theorem.
TauCeti at `c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` is likewise incompatible,
partial substrate. Both are outside the pinned closure. Nothing was cloned,
fetched, built, integrated, or credited.

Assuming a direction package, weakening the equivalence, or replacing the
analytic predicates with abstract fields would add an unproved premise or
substitute a different theorem and was rejected.

## Scheduler Handoff

The owned path contained `28` integrated unresolved proof-recheck/blocker JSON
artifacts before this run, while the authoritative DAG still records
`attempts: 0` and `children: []`. This exceeds the rev-5.6 rule requiring a
split after five unresolved execution ticks. The worker may not edit that DAG.
The master or scheduler must reconcile attempt history and split the item into
dependency-legal, exactly elaborated child obligations rather than schedule
another whole-root retry.

The direct prerequisite `S56-M-0330-OBLIGATION_TREE` is only `[_]`, not
master-accepted `[x]`. Consequently the proof item cannot be master-accepted on
this base even if a proof receipt were proposed.

## Validation

All commands ran inside this worker clone. Initial status showed only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. Existing
pinned artifacts were reused read-only, temporary Lean output was removed, and
no `lake update`, `lake build`, dependency clone/fetch, checkout, or other
`.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups and all `1546` uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets with ranks `1..1546` passed. |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank `823`; lifecycle `planned`; `theorem_complete=false`. |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | Exact expression SHA-256 above; all three mutations killed. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges passed; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both direction packages remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search | 1 | Expected no-match over `9676` Lean source files. |
| Scoped prohibited-token scan | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 230f719d..HEAD --` proof inputs and pins | 0 | Statement, composition, registry, typed graphs, anchor audit, validation specs, Lake manifest, and toolchain are unchanged. |
| Pinned mathlib and flt-regular `rev-parse HEAD HEAD^{tree}` | 0 | Both resolve exactly to their manifest revisions and recorded trees. |

The narrow nonmutating Lean replay used a fresh `/tmp` directory and an explicit
`LEAN_PATH` assembled from the existing pinned package objects:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-head-ebfa067f-slot54.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lp=$(printf '%s:' \
  "$repo/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean" \
  "$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
cd "$mathlib_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$lp" \
  timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 --root="$target" \
      -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lp" \
  timeout --foreground --kill-after=5s 600s \
    lake env lean --trust=0 -t0 --root="$target" \
      "$target/ObligationTree.lean"
```

The temporary `Statement.olean` SHA-256 was
`e3170bec5ab039bd33781fe439cc5236e8526bcda9648931129ae32a95bf9194`.

## Retry Condition

The master or scheduler must first reconcile attempts, accept or repair the
prerequisite, and split the proof item. Resume a child only after its exact Lean
interface is frozen and its dependencies are accepted. Relevant
placeholder-free proof bodies, or an immutable compatible exact proof, must
then enter the pinned closure.

This artifact proposes no item-state or dependency promotion and makes no
audit, validation, release, or theorem-completion claim.
