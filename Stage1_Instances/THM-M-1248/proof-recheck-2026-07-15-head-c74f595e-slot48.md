# THM-M-1248 proof recheck at `c74f595e`

Item: `S56-M-1248-PROOF`  
Date: `2026-07-15` (`Asia/Shanghai`)  
Base revision: `c74f595e99fe574f4619307c859ec20986bb2297`  
Base tree: `b27451453ff7d1e87d296c6634bd270799c666d9`

## Verdict

`blocked`. The exact frozen target remains open. The existing placeholder-free
`Proof.lean` bodies still close only the parameter split (`M1248-N-PARAM`) and
the lower-order `a = 0` endpoint (`M1248-B-A0`). They do not construct
`CKNAnalyticPackage`; the immediate root cut is therefore
`M1248-T-ALL-PARAMS`, and this proof item remains `[ ]`.

The first unavailable analytic dependency is `M1248-L-ORIGIN`: neither this
repository nor pinned mathlib has a checked package for the measurability,
integrability, cutoff, and limiting facts required by the singular radial
weights. Consequently the exact weighted Sobolev/Hardy endpoint, the `a = 1`
branch, and the interior Holder/`Real.rpow` construction remain open. The
nearest pinned Sobolev theorem is unweighted and cannot receive root proof
credit. No exact compatible declaration was found in the authoritative
checkout or the bounded pinned source search.

No definitional shortcut was identified. Bochner integration's value for a
nonintegrable function does not collapse the genuinely integrable cases, and
`Real.rpow` retains its ordinary behavior. The raw Pi-norm/L2 transport in the
frozen encoding is a fidelity issue, not a proof of the proposition.

This is target-scoped blocker evidence, not a positive proof receipt. It does
not satisfy the assigned item or claim audit, validation, release, master, or
theorem completion. Because the proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, network action, or
`.lake` mutation ran. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges passed; denominator `a0c3a82c...ceaa11`; root open M3 and analytic package M4. |
| top-level `cd Formalizations/Lean && lake env which lean` | 1 | Pinned-environment resolution is currently blocked because the shared `flt-regular` checkout has `HEAD` at `refs/heads/.invalid`; no repair or fetch was attempted. |
| isolated trust-zero replay below | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `AnchorAudit.lean` elaborated against the existing pinned mathlib artifacts; the three local proof bodies are sorry-free and report only `propext`, `Classical.choice`, and `Quot.sound`. |
| token-anchored prohibited-construct scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, bodyless `axiom`, `unsafe`, `implemented_by`, `native_decide`, or `extern`. |
| JSON parsing of `proof-receipt.json` and the preceding structured recheck | 0 | Both records parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest correctly absent. |

The successful narrow Lean replay avoided the broken top-level dependency
resolver by invoking `lake env lean` from the already pinned mathlib package;
it did not mutate any dependency:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean/.lake/packages/mathlib
target=$repo_root/Stage1_Instances/THM-M-1248
tmp=$(mktemp -d /tmp/thm-m-1248-slot48-lake-mathlib.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cp "$target"/{Statement,ObligationTree,Proof,AnchorAudit}.lean "$tmp"/
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/AnchorAudit.lean")
```

Pinned versions observed from the existing artifacts were Lean `4.29.0`,
commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Reopen Condition

Implement placeholder-free bodies for the singular-weight boundary package,
the exact weighted Sobolev/Hardy endpoint, and the interior Holder/real-power
construction, then compose them into `CKNAnalyticPackage`; alternatively pin
an immutable compatible Lean 4 terminal proof and validate an exact transport
and complete terminal-body provenance without changing the dependency lock.
