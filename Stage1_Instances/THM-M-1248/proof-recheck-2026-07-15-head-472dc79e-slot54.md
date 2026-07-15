# THM-M-1248 proof recheck at `472dc79e` (slot54)

Item: `S56-M-1248-PROOF`

Intent: `prove`

Recheck date: `2026-07-15T15:12:46+08:00`

Base revision: `472dc79eb4d406a6707691193fbe3ab58d0f0cc4`

Base tree: `881d873727dc80435119839b8e60e9e9c2cfb208`

## Verdict

`blocked`. No premise-free proof body was implemented or found for the exact
root `Stage1Instances.THM_M_1248.CaffarelliKohnNirenbergTarget`. The proof
item remains `[ ]`, lifecycle remains `planned`, and no theorem-completion
claim is made.

The three placeholder-free declarations already in `Proof.lean` prove only
the parameter split (`M1248-N-PARAM`) and lower-order `a = 0` endpoint
(`M1248-B-A0`). The declaration in `ObligationTree.lean` is conditional
composition: it consumes, but does not construct, `CKNAnalyticPackage`.
Consequently the immediate machine root cut remains `M1248-T-ALL-PARAMS`.

The earliest hard acceptance blocker is exact source-to-formal statement
identity. The integrals in `weightedLp` and `weightedDerivativeLp` quantify
over raw `Fin n -> Real`, so their radial factor uses that type's Pi/sup norm,
while `u` and `fderiv` are evaluated after `WithLp.toLp 2` in Euclidean/L2
space. The primary CKN theorem uses Euclidean radius. No checked equality,
implication, or equivalence transports this mixed encoding to the source
claim. This fidelity defect is not a proof shortcut for the frozen proposition.

Even after statement repair, the first absent analytic body in the frozen
route is `M1248-L-ORIGIN`: neither the repository nor pinned mathlib supplies
the required singular-weight measurability, integrability, cutoff, and limit
package. The positive weighted endpoint, interior Holder/real-power
interpolation, `CKNAnalyticPackage`, and the exact root therefore remain open.
The closest pinned result is an unweighted Sobolev inequality and receives no
root proof credit. A repository and pinned-source scan found no newer exact
terminal body; the similarly named THM-M-1228 files concern Navier-Stokes
partial regularity and are unrelated.

Because the assigned proof phase is not complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks ran inside this worker clone. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch/checkout, or `.lake` mutation ran.
Temporary Lean outputs were confined to `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed 15 assurance groups and all 1546 uniform-L0 Lean 4 targets. |
| `python3 scripts/stage1_target.py check` | 0 | Passed 1546 unique targets at ranks 1 through 1546. |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428; `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | Passed 18 obligations and 43 typed edges; denominator `a0c3a82c...ceaa11`; root open M3 and analytic package M4. |
| isolated trust-zero Lean recipe below | 0 | All four modules elaborated. The conditional composer and the three partial proof bodies reported only `propext`, `Classical.choice`, and `Quot.sound`; all three partial bodies were sorry-free. |
| token-anchored prohibited-construct scan over owned Lean files | 1 expected | No `sorry`, `admit`, `sorryAx`, bodyless `axiom`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token was found. |
| exact-topic scan outside this dossier over repository and pinned-mathlib Lean sources | 0 | Hits were unrelated THM-M-1228/Navier-Stokes surfaces; no exact weighted-interpolation body was found. |
| JSON parsing of `proof-receipt.json` and all prior proof-recheck records | 0 | All six existing proof JSON records parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest correctly absent. |

The narrow replay was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1248
tmp=$(mktemp -d /tmp/thm-m-1248-slot54-proof.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target"/{Statement,ObligationTree,Proof,AnchorAudit}.lean "$tmp"/
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/Statement.olean" "$tmp/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" "$tmp/Proof.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 -t0 \
  --root="$tmp" "$tmp/AnchorAudit.lean"
```

The four output hashes exactly matched the preceding current-base replay:
`c3854d68...ee54a`, `dfcb3a8f...2b45c`, `09f72a9e...4521`, and
`0588d62b...1bbfd`. Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`; flt-regular
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`, tree
`32c9eace926573a9981787ae97643e520353c893`.

## Reopen Condition

First reopen statement identity and consistently encode Euclidean radial
weights or provide a checked exact transport, then version and re-freeze the
statement fingerprint, registry, typed graphs, and dependent evidence. Split
the oversized analytic route into exact Lean signatures and substantive
`<=100`-step leaves; implement the singular-origin facts, weighted endpoint,
and interior bridges without placeholders; then construct
`CKNAnalyticPackage` without premises and compose the exact root. An immutable,
compatible pinned terminal proof with complete provenance would be an
alternative.

This is current-base, target-scoped, nonrelease blocker evidence. It does not
satisfy `S56-M-1248-PROOF`, change scheduler state, close the root, or claim
audit, validation, release, receipt acceptance, master acceptance, or theorem
completion.
