# THM-M-1248 proof-phase recheck at `5c85fccb`

Item: `S56-M-1248-PROOF`

Recheck date: 2026-07-15 (Asia/Shanghai)

Base revision: `5c85fccbb71a5ac8b4a5d95413a0f36af5e04294`

Base tree: `f80ad746fe4c15d869994cc47c3f10b881d89dd5`

## Verdict

`blocked`. The current placeholder-free bodies in `Proof.lean` prove only the
parameter split (`M1248-N-PARAM`) and the lower-order `a = 0` endpoint
(`M1248-B-A0`). They do not construct `CKNAnalyticPackage` or inhabit
`CaffarelliKohnNirenbergTarget`. The theorem in `ObligationTree.lean` merely
consumes `CKNAnalyticPackage` as an explicit premise, so the immediate machine
root cut remains `M1248-T-ALL-PARAMS` and the exact root remains open `M3` in
the frozen authoritative graph.

The earliest hard acceptance blocker is statement identity. In `weightedLp`
and `weightedDerivativeLp`, the integration variable has raw type
`Fin n -> Real`; consequently the radial factor `norm x` uses the Pi/sup norm,
while `u` and `fderiv` are evaluated after `WithLp.toLp 2 x` in Euclidean/L2
space. The primary CKN statement uses Euclidean radius, and no checked
source-to-formal equality, implication, or equivalence transport is recorded.
This mismatch is a fidelity defect, not a shortcut that proves the frozen
proposition.

Even after statement repair, the first missing analytic body in the frozen
route is `M1248-L-ORIGIN`: neither this repository nor the pinned mathlib
closure supplies the singular radial-weight measurability, integrability,
cutoff, and limit package. Hence the weighted Sobolev/Hardy endpoint, the
positive `a = 1` branch, and the interior Holder/real-power construction remain
open. The closest pinned Sobolev theorem is unweighted and receives no proof
credit.

The historical partial receipt is not proof-node acceptance evidence: it has a
stale base, declares `root_closed=false` and `proof_phase_complete=false`, and
does not meet the current content-addressed structured-recipe contract. The
frozen typed graph also retains planned formal targets and empty evidence for
the two partial obligations; under conflict the weaker graph state is kept.

This is target-scoped nonrelease blocker evidence. It does not satisfy
`S56-M-1248-PROOF`, propose `[_]` or `[x]`, or claim audit, validation, release,
master, or theorem completion. Because the assigned phase is not genuinely
complete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

No `lake update`, `lake build`, dependency clone/fetch/checkout, network
action, or `.lake` mutation ran. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. Temporary Lean files
were isolated below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges passed; denominator `a0c3a82c...ceaa11`; root open M3 and analytic package M4. |
| isolated trust-zero `lake env lean` replay below | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `AnchorAudit.lean` elaborated. The three partial bodies were sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| token-anchored prohibited-construct scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, bodyless `axiom`, `unsafe`, `implemented_by`, `native_decide`, or `extern`. |
| JSON parsing of the historical proof receipt and prior proof rechecks | 0 | Every structured record parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest correctly absent. |

The narrow replay used the ordinary top-level pinned Lake environment:

```bash
set -uo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1248
tmp=$(mktemp -d /tmp/thm-m-1248-slot11-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target"/{Statement,ObligationTree,Proof,AnchorAudit}.lean "$tmp"/
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/Statement.olean" \
  "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" \
  --trust=0 -t0 --root="$tmp" -o "$tmp/ObligationTree.olean" \
  "$tmp/ObligationTree.lean"
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/Proof.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/AnchorAudit.lean")
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Exact source and output hashes
are preserved in the adjacent JSON blocker artifact.

## Retry Condition

First reopen the statement phase and either encode Euclidean radial weights
consistently or add a checked exact transport, then version and re-freeze the
expression fingerprint, obligation registry, typed graphs, and dependent
receipts. The scheduler must also split the oversized weighted analytic work,
which has now received more than five unresolved proof attempts, into exact
signatures and substantive `<=100`-step leaves. Those children must implement
the singular-origin boundary facts, weighted endpoint, and interior bridges
before a premise-free `CKNAnalyticPackage` and exact root can be composed.
