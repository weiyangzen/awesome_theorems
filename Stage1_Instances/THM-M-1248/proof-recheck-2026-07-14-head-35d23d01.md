# THM-M-1248 proof-phase recheck at current base

Item: `S56-M-1248-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `35d23d0193cd7c8fccb1d09f22534c6eba066b02`

Base tree: `4325d20b5ec8db888f28fcedc79cc1b7745c0c68`

## Verdict

`blocked`. The existing `Proof.lean` remains a valid placeholder-free partial
formalization: it closes the exact parameter split (`M1248-N-PARAM`) and the
`a = 0` endpoint (`M1248-B-A0`). This retry found no local or pinned body for
the positive weighted endpoint and interior analytic package, so the assigned
proof phase remains `[ ]` and the exact root remains `[H1, M2, R3]`.

The frozen target is not vacuous. For example, `n = 3`, `p = q = 2`, all
weights zero, and `a = 1` admits `r = 6`, while `a = 1 / 2` admits `r = 3`.
These are nontrivial Sobolev and interpolation branches. The real Bochner
integral's value on nonintegrable functions does not discharge the integrable
smooth compactly supported cases. A later statement review should also check
the norm transport in `weightedLp`: its integration variable is a raw
`Fin n -> Real`, so the radial factor is formed before the `WithLp.toLp 2`
conversion used for `u`.

The first unavailable analytic dependency remains `M1248-L-ORIGIN`: no
checked body in the pinned closure establishes the measurability,
integrability, and cutoff/limit facts for all singular radial weights admitted
by the source conditions. This is the first failed graph dependency, not the
whole missing proof: the weighted endpoint also needs the paper's one-dimensional
Hardy cases, radial/nonradial reductions, spherical means, and annular
estimates. Consequently the following obligations remain open:

- `M1248-L-WEIGHTED` and `M1248-B-A1` for the positive weighted endpoint;
- `M1248-L-HOLDER`, `M1248-L-RPOW`, and `M1248-B-INTERIOR` for interpolation;
- `M1248-T-ALL-PARAMS`, the immediate root cut.

`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq` proves an unweighted strict
Sobolev special case. The exact-topic source scan found no inhabitant of the
weighted package. Importing that special case, assuming `CKNAnalyticPackage`,
or adding an axiom would change or hide the theorem and is therefore rejected.

## Validation

All checks ran in this worker clone. Temporary Lean outputs were confined to
`/tmp` and removed by a shell trap. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. No `lake update`,
`lake build`, dependency clone/fetch, network access, or `.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges passed; denominator `a0c3a82c...ceaa11`; root open M3 in the frozen pre-proof graph. |
| isolated trust-zero Lean recipe below | 0 | Exact statement, conditional composition, three partial proof bodies, and anchor audit elaborated. All three proof bodies were reported sorry-free; their axiom reports contained only `propext`, `Classical.choice`, and `Quot.sound`. |
| `python3 -m json.tool Stage1_Instances/THM-M-1248/proof-receipt.json >/dev/null` | 0 | Existing partial receipt parsed. |
| prohibited-token scan over owned Lean files | 1 | Expected no-match result: no `sorry`, `admit`, `sorryAx`, `axiom`, `unsafe`, `implemented_by`, `native_decide`, or `extern` token. |
| exact-topic declaration scan over the repository and pinned mathlib | 0 | Hits were confined to this dossier and unrelated Navier-Stokes CKN dossier/legacy surfaces; no terminal weighted-inequality body was found. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1248
tmp=$(mktemp -d /tmp/thm-m-1248-proof-recheck.XXXXXX)
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

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Exact input hashes and validation
exits are recorded in the adjacent JSON blocker artifact.

## Retry Condition

Resume after placeholder-free local implementations of the singular-weight
boundary package, the exact weighted Sobolev/Hardy endpoint, and the interior
Holder/real-power construction, followed by composition into
`CKNAnalyticPackage`; alternatively, pin an immutable compatible Lean 4 proof
and check an exact transport with complete terminal-body provenance. The
current `M1248-L-WEIGHTED` node will likely require a versioned split before
implementation because the source route exceeds its 100-step planning ceiling.

This current-base record is nonrelease blocker evidence, not a proof receipt.
It does not satisfy `S56-M-1248-PROOF`, propose scheduler state, or claim audit,
validation, release, master, or theorem completion. Because the assigned phase
is not genuinely self-tested complete, `.stage1-worker-selftest.json` remains
absent.
