# THM-M-0330 proof-phase blocker at `b4d23994`

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T20:00:38+08:00` (`Asia/Shanghai`)

Base revision: `b4d239943a37f6c25c377bbfd85c0e1ec7f4acaa`

Base tree: `5f13e0e86bde3bcaaef38b979819490c648166e3`

## Verdict

`blocked`. The repository and existing pinned dependency closure contain no
placeholder-free inhabitant of either exact direction package. The proof phase
remains `[ ]`, lifecycle remains `planned`, the frozen root remains
`[H3, M4, R4]`, and both audit completion and theorem completion remain false.
This is a target-scoped blocker and scheduler handoff, not a proof receipt. The
workspace-root `.stage1-worker-selftest.json` is therefore deliberately absent.

The exact root is
`Stage1Instances.THM_M_0330.HilleYosidaContractionTarget`, expression SHA-256
`5696285042abd39e340c7e72b2c2855d17e2e335106b1aa6a724056fd68bd75e`.
Its minimal open cut remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` checks only conditional composition from complete
`ForwardPackage` and `ConversePackage` arguments. It constructs neither, while
`target_iff_expanded` is only definitional transport.

The proof inputs and dependency pins are unchanged since the obligation-tree
integration at `230f719d`. Repository history, duplicate target `THM-M-1041`,
and legacy `S1_M_234.lean` contain definitions, abstract interfaces,
transports, or conditional composition only. A search over all `9676` Lean
sources in the pinned package cache found no Hille-Yosida or C0-semigroup
generator theorem.

The immutable external candidates remain outside the pinned closure and
receive no proof credit. The bounded audit of `mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667` found only pieces of the forward
resolvent route: no generator density or closedness, full-domain left inverse,
or converse. The audit of TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` likewise found partial,
incompatible substrate rather than either exact package. Nothing was cloned,
fetched, built, integrated, or credited.

Closing the exact root requires a substantial new analytic formalization. The
forward route must prove generator density and closedness, construct the
Laplace/Bochner resolvent, and prove both inverse laws and the `1/a` estimate.
The converse route must construct the Yosida approximants and their exponential
semigroups, establish uniform contraction and strong convergence, then identify
the limiting generator exactly with `A`. Assuming either package, weakening
the equivalence, or replacing the analytic predicates with abstract fields
would add an unproved premise or substitute another theorem and was rejected.

## Scheduler Handoff

The owned path contained `24` integrated unresolved proof-recheck pairs before
this run, but the authoritative DAG still records `attempts: 0` and
`children: []`. This exceeds the rev-5.6 rule requiring a split after five
unresolved execution ticks. The worker may not edit that DAG. The master or
scheduler must reconcile the attempt history and split the proof item into the
frozen dependency-legal child obligations rather than schedule another
whole-root retry.

The direct prerequisite `S56-M-0330-OBLIGATION_TREE` is still only `[_]`, not
master-accepted `[x]`. Consequently this proof item cannot be master-accepted
on this base even if a proof receipt were proposed.

## Validation

All commands ran in this worker clone. Initial status showed only the
automation-provided untracked `Formalizations/Lean/.lake` symlink. Existing
pinned artifacts were reused read-only. Temporary Lean output was created
under `/tmp` and removed. No `lake update`, `lake build`, dependency clone or
fetch, checkout, or other `.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `15` assurance groups and all `1546` uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | `1546` unique targets with ranks `1..1546` passed. |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank `823`; lifecycle `planned`; `theorem_complete=false`. |
| `LEAN_NUM_THREADS=1 timeout --foreground --kill-after=5s 600s python3 Stage1_Instances/THM-M-0330/check_statement.py` | 0 | Exact expression SHA-256 above; all three mutations killed. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | `19` obligations and `40` typed edges passed; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both direction packages remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match over `9676` Lean source files. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 230f719d..HEAD --` proof inputs and pins | 0 | Statement, composition, registry, typed graphs, anchor audit, validation specs, Lake manifest, and toolchain are unchanged. |
| Pinned mathlib and flt-regular `rev-parse HEAD HEAD^{tree}` | 0 | Both resolve exactly to their manifest revisions and recorded trees. |
| `python3 -m json.tool` plus target-specific blocker assertions | 0 | Structured blocker parses; identity, base/tree, `[ ]` state, false completion flags, empty proof/receipt lists, exact cut, prerequisite, retry count, changed paths, and self-test absence pass. |
| Scoped tracked and no-index `git diff --check` checks | 0 | Both new artifacts have no whitespace errors; no-index diff-found exits were handled as expected. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |

The narrow nonmutating Lean replay reused `lake env lean`, the existing pinned
package objects, and a fresh temporary output directory:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-head-b4d23994-slot52.XXXXXX)
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

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree
`32c9eace926573a9981787ae97643e520353c893`.

## Retry Condition

The master or scheduler must first reconcile attempts and split this proof item
into the frozen child obligations. Resume a child only after its dependencies
are accepted and relevant placeholder-free proof bodies, or an immutable
compatible exact Lean 4 proof, enter the pinned closure. Until then, proof-phase
completion and a worker `[_]` receipt would be false.
