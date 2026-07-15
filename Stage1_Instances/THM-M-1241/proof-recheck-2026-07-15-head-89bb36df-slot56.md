# THM-M-1241 proof-phase recheck at current base

Item: `S56-M-1241-PROOF`

Recheck time: `2026-07-15T09:15:46+08:00` (`Asia/Shanghai`)

Base revision: `89bb36df208fff9659fdeac0e10edeea0248e711`

Base tree: `02e87afb7859de6cf58c19f6cb64715c2e7d7513`

## Verdict

`blocked`. No placeholder-free local body or immutable pinned dependency inhabits either terminal
package required by the exact frozen proposition
`Stage1Instances.THM_M_1241.GagliardoNirenbergTarget`. The assigned proof phase remains incomplete,
the root vector remains `[H2, M3, R4]`, and no worker self-test manifest is warranted.

The unchanged minimal root cut is:

- `M1241-T-FINITE`: the arbitrary finite-`q`, finite-`r` interpolation package;
- `M1241-T-ENDPOINT`: every complementary case where `q` or `r` is infinite.

`root_of_finite_and_endpoint_packages` is an exact checked composition, but both packages are
premises. It constructs neither and therefore cannot receive root proof credit. `Proof.lean`
checks the degenerate output-exponent case `p = 0`; registry v1 contains no node for that fragment,
so it closes no frozen obligation. `M1241-B-ZERO` is instead Nirenberg's exceptional `j = 0`
endpoint branch.

Pinned mathlib exposes five nearby first-order compact- or bounded-support Sobolev estimates in
`Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean`. The exact wrapper-able version is
already used by the distinct target `THM-M-1245`. It does not provide arbitrary `m` and `j`, the
two powered norm factors, all finite exponents, the integer-critical branch, infinity endpoints,
or the exact zero-order exceptional hypothesis required here. Reusing it as either terminal
package would substitute a strict special case for the frozen target.

## Narrow validation

All commands ran inside this worker clone. The automation-provided `Formalizations/Lean/.lake`
symlink reused the canonical pinned artifacts read-only. Lean outputs were isolated under `/tmp`
and removed. No `lake update`, `lake build`, dependency clone/fetch, network request, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422, lifecycle `planned`, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828...864991e`; root M3 and both terminal packages M4. |
| isolated trust-zero Lean recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated; the composer and all three partial declarations report only `propext`, `Classical.choice`, and `Quot.sound`; all partial declarations report sorry-free. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|\\bunsafe\\b|implemented_by|native_decide|\\bextern\\b' Stage1_Instances/THM-M-1241 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct occurs in the owned Lean sources. |
| exact package-inhabitant scan over repository Lean sources | 1 | Expected no-match result: neither `FiniteExponentPackage` nor `InfiniteEndpointPackage` has a proof body. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | The pinned mathlib checkout was not modified. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-89bb36df-slot56-t0.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Provide placeholder-free Lean implementations, or an immutable compatible dependency, for both
frozen terminal packages and their analytic supports, with exact-type transports, terminal-body
provenance, and node-scoped trust checks. A conditional assumption, the uncredited `p = 0`
fragment, the weaker `THM-M-1245` Sobolev theorem, an axiom, or a placeholder is not a substitute.

This current-base recheck is nonrelease blocker evidence. It does not satisfy
`S56-M-1241-PROOF`, change scheduler state, or claim audit completion, theorem completion,
validation, release, or master acceptance. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` is intentionally absent.
