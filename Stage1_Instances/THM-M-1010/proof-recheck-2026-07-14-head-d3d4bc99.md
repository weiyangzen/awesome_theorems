# THM-M-1010 proof recheck at `d3d4bc99`

Item: `S56-M-1010-PROOF`

Intent: `prove`

Recheck date: `2026-07-14T04:02:52+08:00`

Base revision: `d3d4bc991fae237427b8ac391bbe701dca8f2af2`

Base tree: `51d54892f625b3b42e3b0c2c6b3c8e173c4ad166`

## Verdict

`blocked`. No eligible proof body was implemented or found for the exact root
`Stage1Instances.THM_M_1010.Target`. The root vector remains
`[H1, M3, R3]`, and the proof item remains `[ ]`.

The repo-local declarations remain substantive but nonterminal:

- `ObligationTree.target_of_couplingPackage` is exact checked composition from
  an assumed `CouplingPackage S`; it does not construct that package.
- `representation_of_constant_laws` and `target_for_constant_sequence` prove
  the constant-law boundary case only.

The first unavailable construction package is `M1010-N-PARTITIONS`; the
corresponding root-blocking construction gate is `M1010-C-COUPLING`. The
checked dependency closure supplies
small measurable partitions, Portmanteau mass convergence at null frontiers,
one-law realization on the unit interval, product probability spaces, and
a.e.-convergent subsequence extraction from an already common-space
convergence-in-measure hypothesis. It does not supply refining null-boundary
partitions together with a compatible interval coupling for all prescribed
laws. Independent one-law or product realizations have the correct marginals
but no convergence relation, while the subsequence theorem neither creates
the coupling nor proves convergence of the full prescribed sequence.

The pinned source tree still contains no Skorokhod- or Skorohod-named
declaration. The immutable external candidate recorded in the later owned
recheck is restricted to `Real` and has body `by sorry`; it is both a
statement mismatch and an ineligible placeholder. A Borel equivalence with a
real subset cannot repair this: it need not preserve the Polish topology and
thus does not transport the required pointwise topological convergence.

The frozen remaining root cut set is `M1010-N-PARTITIONS`,
`M1010-C-INTERVAL`, `M1010-L-MEASURABLE`, `M1010-L-LAWS`, and
`M1010-L-AE-STABILIZE`. Closing those leaves discharges the internal
`M1010-L-METRIC-CONVERGENCE` and `M1010-C-COUPLING` nodes; the already checked
`M1010-T-ASSEMBLE` composer then closes `M1010-ROOT`.

Because the requested positive proof phase is not complete, no proof receipt
or `.stage1-worker-selftest.json` is emitted. The retry condition is a
placeholder-free implementation of those frozen packages, or discovery of an
immutable exact Polish-space Lean 4 proof that can be pinned, provenance
audited, and checked in the current dependency closure.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned artifacts was reused read-only. No `lake update`, `lake
build`, dependency clone/fetch, or `.lake` mutation was performed. No network
result was used as accepted evidence. Lean outputs were isolated under `/tmp`
and removed by trap.

| Command | Exit | Exact result |
|---|---:|---|
| `git rev-parse HEAD HEAD^{tree}; git status --short --untracked-files=all` | 0 | Base `d3d4bc991fae237427b8ac391bbe701dca8f2af2`, tree `51d54892f625b3b42e3b0c2c6b3c8e173c4ad166`; only the automation-provided `.lake` symlink was untracked before this recheck. |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1010` | 0 | Rank 290; hard mathlib anchor/wrapper lane; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 -B Stage1_Instances/THM-M-1010/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `8cf08f66...16016`; conditional composition reported only `propext`, `Classical.choice`, and `Quot.sound`; root explicitly remains open at `M3`. |
| Isolated pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated. The conditional composer and both constant-law declarations report exactly `propext`, `Classical.choice`, and `Quot.sound`. Log hashes: empty statement `e3b0c442...b855`, obligation `cbee87b9...9abb`, proof `940c65d9...9673`. Temporary object hashes: statement `2675f2bc...3df`, obligation `a11e8641...ca7`. |
| Prohibited-construct scan over `Stage1_Instances/THM-M-1010/*.lean` (exact executable command below) | 1 | Expected no-match: no scanned prohibited construct occurs in owned Lean sources. |
| `rg -ni 'skorokhod\|skorohod' Formalizations/Lean/.lake/packages --glob '*.lean' --glob '*.md' --glob '*.tex'` | 1 | Expected no-match in the complete pinned package source tree. |
| `cd Formalizations/Lean && lake env lean --version && lake --version; git -C .lake/packages/mathlib rev-parse HEAD HEAD^{tree}; git -C .lake/packages/mathlib status --porcelain` | 0 | Lean 4.29.0 commit `98dc76e3...fab16740`; Lake `5.0.0-src+98dc76e`; mathlib revision `8a178386...ea95`, tree `bdc39a31...c2b`, clean worktree. |
| `python3 -m json.tool Stage1_Instances/THM-M-1010/proof-recheck-2026-07-14-head-d3d4bc99.json` | 0 | The fresh structured blocker parses as JSON. |
| `git diff --no-index --check /dev/null <each fresh blocker artifact>` | 1 expected each | Both fresh files differ from `/dev/null`; empty diagnostic output confirms no whitespace errors. |
| `git diff --check -- Stage1_Instances/THM-M-1010 .stage1-worker-selftest.json` plus explicit expected-exit handling for the two no-index checks | 0 | No tracked-diff whitespace diagnostic; the no-index checks cover the fresh untracked artifacts. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent because the proof phase is blocked. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo="$PWD"
target="$repo/Stage1_Instances/THM-M-1010"
lean_root="$repo/Formalizations/Lean"
tmp=$(mktemp -d /tmp/thm-m-1010-proof-replay.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/Stage1_Instances/THM-M-1010"
lean_bin=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 180 "$lean_bin" --trust=0 -t0 \
  -R "$repo" -o "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$target/Statement.lean" >"$tmp/statement.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean_bin" --trust=0 -t0 \
  -R "$repo" -o "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean" \
  "$target/ObligationTree.lean" >"$tmp/obligation.log" 2>&1
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 180 "$lean_bin" --trust=0 -t0 \
  -R "$repo" "$target/Proof.lean" >"$tmp/proof.log" 2>&1
sha256sum "$tmp/statement.log" "$tmp/obligation.log" "$tmp/proof.log" \
  "$tmp/Stage1_Instances/THM-M-1010/Statement.olean" \
  "$tmp/Stage1_Instances/THM-M-1010/ObligationTree.olean"
```

Exact prohibited-construct scan:

```bash
rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide|^[[:space:]]*(?:constant|opaque|extern|external)[[:space:]]' \
  Stage1_Instances/THM-M-1010 --glob '*.lean'
```

This is current-base nonrelease blocker evidence. It is not a proof receipt,
does not satisfy `S56-M-1010-PROOF`, changes no scheduler state, and claims no
audit completion, theorem completion, validation, release, or master
acceptance.
