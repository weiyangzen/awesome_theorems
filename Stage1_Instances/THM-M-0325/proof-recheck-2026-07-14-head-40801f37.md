# THM-M-0325 proof recheck at HEAD 40801f37

Item: `S56-M-0325-PROOF`

Recorded: `2026-07-14T02:44:52+08:00`

Base revision: `40801f373a9b0443cc58ff8ec365fb5b75c8b8c3`

## Verdict

`blocked`. The frozen target is the full finite real Grothendieck inequality.
No repo-local or pinned terminal proof body inhabits
`GrothendieckInequalityTarget`. The only root-facing declaration remains
`target_of_proofPackage`, a conditional identity whose premise is definitionally
the exact open target; it supplies no proof credit.

The first unavailable substantive gate is `M0325-K-TRANSFORM`, the universal
real Grothendieck/Krivine transform and its bound. Finite-span and Gram
reductions, correlated random-sign rounding, measurability and integrability,
the pointwise scalar application, the expectation estimate, and final package
assembly also remain open. Pinned mathlib supplies tensor-seminorm and Gaussian
substrate but not the transform or correlated-sign identity. Bounded current
Sourcegraph and GitHub discovery searches found no compatible Lean candidate;
these results do not purport to prove global absence.

Consequently the root remains `[H2, M3, R4]`, the minimal cut remains
`M0325-T-PACKAGE`, and both `root_closed` and `theorem_complete` remain false.
Adding an axiom, assuming the package, or returning the conditional identity
would be a prohibited placeholder or substituted theorem. The proof phase is
not self-tested, so `.stage1-worker-selftest.json` is deliberately absent.

## Exact checks

All Lean validation reused the existing locked artifacts. No `lake update`,
`lake build`, dependency clone/fetch, or dependency write was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-0325` | 0 | Rank 214, planned, legacy artifacts unaccepted, theorem incomplete. |
| `LEAN_NUM_THREADS=1 python3 Stage1_Instances/THM-M-0325/check_statement.py` | 0 | Canonical expression hash matched `b4daa662...cf82`; all four structural mutations were distinguished. |
| `python3 Stage1_Instances/THM-M-0325/check_anchor_audit.py` | 0 | Audit invariants passed at mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `python3 Stage1_Instances/THM-M-0325/check_obligation_tree.py` | 0 | 15 obligations and 33 typed edges passed; denominator `4c41e44f...7703c`; root open M3. |
| Isolated `lean --trust=0 -t0` on copied `Statement.lean`, then `ObligationTree.lean` with the temporary olean and pinned `LEAN_PATH` | 0 | Exact target and conditional composition elaborated; composition axioms were `propext`, `Classical.choice`, and `Quot.sound`; temporary output removed. |
| Isolated `lean --trust=0 -t0` on copied `AnchorAudit.lean` with pinned `LEAN_PATH` | 0 | Pinned tensor anchor types elaborated; comparison uses only the same three axioms. |
| Pinned-source `rg` for Grothendieck/Krivine/random-rounding/correlated-sign terms | 0 | Only historical audit strings and an unrelated Gaussian-polynomial comment; no terminal declaration. |
| Sourcegraph global Lean searches for `"Grothendieck inequality"` and `Krivine`, including archives and forks | 0 | Both completed with `matchCount=0`. |
| GitHub repository search for `Grothendieck inequality Lean` | 0 | `total_count=0`, `incomplete_results=false`. |
| Prohibited-token scan over owned Lean sources | 1 | Expected no-match; no placeholder, axiom declaration, unsafe/oracle, or native-decision shortcut. |
| `git diff --check --no-index /dev/null` on each new recheck artifact | 0 | No whitespace errors. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-0325
tmp=$(mktemp -d /tmp/thm-m-0325-proof-recheck.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target/Statement.lean" "$target/ObligationTree.lean" "$target/AnchorAudit.lean" "$tmp/"
cd "$tmp"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" --trust=0 -t0 -R "$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_PATH="$tmp:$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" --trust=0 -t0 -R "$tmp" "$tmp/ObligationTree.lean"
LEAN_PATH="$lean_path" LEAN_NUM_THREADS=1 timeout 300 "$lean" --trust=0 -t0 -R "$tmp" "$tmp/AnchorAudit.lean"
```

It exited 0 and printed the exact target, the five audited tensor declarations,
and the two axiom reports described above. A first unconstrained invocation of
`python3 Stage1_Instances/THM-M-0325/check_statement.py` exited 1 with
`error: external command 'git' exited with code 128`; the recorded
single-threaded retry exited 0, emitted the expected fingerprint and mutation
list, and left no temporary target artifact.

## Retry boundary

Resume only with an exact placeholder-free implementation of the frozen proof
package, or an immutable compatible Lean 4 terminal body that can be pinned and
exact-type checked. The repeated unchanged root task should instead be split by
the master into the frozen dependency-legal analytic obligations. This blocker
record is not a proof receipt and must not advance the item to `[_]` or `[x]`.
