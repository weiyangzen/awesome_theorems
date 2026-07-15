# THM-M-1248 proof recheck at `cc8afe07`

Item: `S56-M-1248-PROOF`  
Date: `2026-07-15` (`Asia/Shanghai`)  
Base revision: `cc8afe076b125cde06f870d92e10040c76924568`  
Base tree: `1f8c1b01a1ec6c271c5ad7f4dbd9538d81ff58a5`

## Verdict

`blocked`. Current-base proof search and trust-zero replay confirm that the
exact frozen target remains open. The placeholder-free declarations already
in `Proof.lean` close only the parameter split (`M1248-N-PARAM`) and lower-order
`a = 0` endpoint (`M1248-B-A0`). `ObligationTree.lean` proves the public target
only from the explicit premise `CKNAnalyticPackage`; it does not construct that
package. The immediate root cut is therefore `M1248-T-ALL-PARAMS`, and this
proof item remains `[ ]`.

The first unavailable analytic dependency is `M1248-L-ORIGIN`: neither this
repository nor the pinned dependency closure has a checked package for the
measurability, integrability, cutoff, and limiting facts required by the
singular radial weights. Consequently the exact weighted Sobolev/Hardy
endpoint, the positive `a = 1` branch, and the interior Holder/`Real.rpow`
construction remain open. The closest pinned theorem,
`MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq`, is unweighted and cannot
receive root proof credit.

The target is not vacuous: the admissible region includes the ordinary
three-dimensional Sobolev tuple `n = 3`, `p = q = 2`, zero weights, `a = 1`,
`r = 6`, as well as an interior tuple with `a = 1/2` and `r = 3`. Bochner
integration's nonintegrable fallback cannot discharge the genuinely
integrable compactly supported smooth cases, and `Real.rpow` does not collapse
them. The raw Pi-norm/L2 radial-norm mismatch in the frozen encoding remains a
statement-fidelity issue, not a proof shortcut.

This record is target-scoped blocker evidence, not a positive proof receipt.
It does not satisfy the assigned item or claim audit, validation, release,
master acceptance, or theorem completion. Because the proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

No `lake update`, `lake build`, dependency clone/fetch, network action, or
`.lake` mutation ran. The automation-provided untracked
`Formalizations/Lean/.lake` symlink was reused read-only. Temporary Lean
outputs were written only below `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, passed. |
| `python3 scripts/stage1_target.py show THM-M-1248` | 0 | Rank 428; lifecycle `planned`; L0/rework-required; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1248/check_obligation_tree.py` | 0 | 18 obligations and 43 typed edges passed; denominator `a0c3a82c...ceaa11`; root open M3 and analytic package M4 in the frozen graph. |
| top-level pinned Lake environment resolver under a 30-second timeout | 124 | Resolution timed out without output because the shared `flt-regular` checkout has no resolvable `HEAD`; no repair or fetch was attempted. |
| isolated trust-zero replay below | 0 | `Statement.lean`, `ObligationTree.lean`, `Proof.lean`, and `AnchorAudit.lean` elaborated against existing pinned artifacts. The three local proof bodies were sorry-free and reported only `propext`, `Classical.choice`, and `Quot.sound`. |
| exact-topic repository and pinned-package scan | 0 | Hits were confined to this dossier, unrelated Navier-Stokes CKN surfaces, and metadata; no exact terminal proof body was found. |
| token-anchored prohibited-construct scan over owned Lean files | 1 | Expected no-match exit: no `sorry`, `admit`, `sorryAx`, bodyless `axiom`, `unsafe`, `implemented_by`, `native_decide`, or `extern`. |
| JSON parsing of the existing partial receipt and all four proof rechecks | 0 | Every structured record parsed. |
| `git diff --check -- Stage1_Instances/THM-M-1248` | 0 | No scoped whitespace errors. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest correctly absent. |

The successful narrow replay still invoked `lake env lean`, as required, from
the already pinned mathlib package. Because its nested Lake manifest resolves
dependencies relative to nonexistent nested build directories, the command
received an explicit `LEAN_PATH` made only from existing pinned package build
directories:

```bash
set -uo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean/.lake/packages/mathlib
target=$repo_root/Stage1_Instances/THM-M-1248
tmp=$(mktemp -d /tmp/thm-m-1248-slot45-trust-zero.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
manual_lean_path=$(find "$repo_root/Formalizations/Lean/.lake/packages" \
  -path '*/.lake/build/lib/lean' -type d -print | LC_ALL=C sort | paste -sd:):\
"$repo_root/Formalizations/Lean/.lake/build/lib/lean:\
$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
cp "$target"/{Statement,ObligationTree,Proof,AnchorAudit}.lean "$tmp"/
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$manual_lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Statement.olean" "$tmp/Statement.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$manual_lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/ObligationTree.olean" "$tmp/ObligationTree.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$manual_lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  -o "$tmp/Proof.olean" "$tmp/Proof.lean")
(cd "$lean_root" && LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$manual_lean_path" \
  timeout 300 lake env lean --trust=0 -t0 --root="$tmp" \
  "$tmp/AnchorAudit.lean")
```

Pinned versions observed from the existing artifacts were Lean `4.29.0`,
commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, and mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Version and split `M1248-L-WEIGHTED` as required by the 100-step ceiling, then
implement placeholder-free singular-weight boundary facts, one-dimensional
Hardy cases, radial/nonradial reductions, spherical-mean and annular
estimates, the weighted endpoint, and the Holder/real-power interior
construction; finally compose them into `CKNAnalyticPackage`. Alternatively,
pin an immutable compatible Lean 4 terminal proof and validate its exact
transport and complete provenance without changing the dependency lock.
