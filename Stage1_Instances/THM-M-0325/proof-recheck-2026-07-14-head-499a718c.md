# THM-M-0325 proof recheck at HEAD 499a718c

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-14T03:12:00+08:00`

Base revision: `499a718cc7926abaf61e9721fe0d7485059403e6`

## Verdict

`blocked`. The frozen target is the full finite real Grothendieck inequality.
No repo-local or pinned terminal proof body inhabits
`GrothendieckInequalityTarget`. The root remains `[H2, M3, R4]`, its minimal
open cut remains `M0325-T-PACKAGE`, and no obligation is newly closed.

`ObligationTree.lean` defines `GrothendieckProofPackage` to be the exact target
and proves only `target_of_proofPackage package := package`. This is a checked
conditional identity, not a construction of the package. Returning it,
postulating the package, or assuming an analytic child would substitute an
unproved premise for the requested theorem.

Pinned mathlib contains Gram matrices, multivariate Gaussian infrastructure,
arcsine analysis, and projective/injective tensor-seminorm substrate. It does
not contain the correlated Gaussian-sign identity, the real Krivine transform
and universal bound, or a terminal Grothendieck theorem. The first substantive
failed gate is therefore `M0325-K-TRANSFORM`. The finite-span and Gram
reductions, random rounding, measurability and integrability, scalar-bound
application, expectation estimate, and final package also remain open.

This proof phase is not complete. The item stays `[ ]`; no proof receipt,
audit completion, validation completion, release, or theorem completion is
claimed. In accordance with the worker rule, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, network request, or
dependency mutation was run. The automation-provided `.lake` symlink was
treated as read-only. Its `flt-regular` checkout is incomplete: `git rev-parse
HEAD` exits 128, and `lake env lean` therefore stops before target elaboration.
This missing pinned artifact is recorded rather than fetched.

The narrow target files were additionally replayed with the installed pinned
Lean 4.29.0 binary and the already-present pinned `.olean` search paths. The
temporary source and `Statement.olean` lived under `/tmp` and were removed.
That direct replay does not repair the broken Lake workspace or constitute
release evidence.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | All 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214; lifecycle `planned`; legacy artifacts unaccepted; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Structured source hashes and pinned mathlib revision passed. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open `M3`. |
| `LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0325/check_statement.py` | 1 | Lake stopped because pinned package `flt-regular` could not resolve `HEAD`; no fetch or repair was attempted. |
| Isolated direct `lean --trust=0 -t0` recipe below | 0 | Exact statement, conditional composition, and five anchor types elaborated. Both axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. |
| Scoped pinned-source search for Grothendieck/Krivine/random-rounding/correlated-sign terms | 0 | Only audit strings and an unrelated Gaussian-polynomial comment; no terminal candidate declaration. |
| Scoped prohibited-token scan over owned Lean sources | 1 | Expected no-match; no `sorry`, `admit`, `sorryAx`, axiom declaration, unsafe, opaque, extern, implementation override, or native-decision shortcut. |
| `python3 -m json.tool Stage1_Instances/THM-M-0325/proof-recheck-2026-07-14-head-499a718c.json` | 0 | Current-base blocker artifact parsed successfully. |
| `git diff --check -- Stage1_Instances/THM-M-0325 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The direct replay recipe was:

```bash
set -euo pipefail
repo_root=$PWD
target=$repo_root/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-direct.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=/home/sansha-2/.elan/toolchains/leanprover--lean4---v4.29.0/bin/lean
lean_path=$repo_root/Formalizations/Lean/.lake/build/lib/lean
for d in "$repo_root"/Formalizations/Lean/.lake/packages/*/.lake/build/lib/lean; do
  lean_path="$lean_path:$d"
done
cp "$target/Statement.lean" "$target/ObligationTree.lean" \
  "$target/AnchorAudit.lean" "$tmp/"
cd "$tmp"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 600 "$lean" --trust=0 -t0 \
  -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 600 "$lean" --trust=0 -t0 \
  -R "$tmp" "$tmp/ObligationTree.lean"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 600 "$lean" --trust=0 -t0 \
  -R "$tmp" "$tmp/AnchorAudit.lean"
```

## Retry Condition

Resume only after an exact placeholder-free implementation of the frozen proof
package, or an immutable compatible Lean 4 terminal body that can be pinned and
exact-type checked. The integration lane must also restore the already-pinned
`flt-regular` artifact before `lake env lean` can replay the workspace. This
blocker record is not a proof receipt and must not advance the item to `[_]` or
`[x]`.
