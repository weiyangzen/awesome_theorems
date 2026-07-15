# THM-M-1241 proof-phase recheck at current base

Item: `S56-M-1241-PROOF`

Recheck time: `2026-07-15T07:53:56+08:00` (`Asia/Shanghai`)

Base revision: `e46e0735d0940bb558acaf027d8386de2579f55d`

Base tree: `9f03ecc77e82eda1f0ea3f0f4b08d1d7419ce0cf`

## Verdict

`blocked`. No placeholder-free local body or immutable pinned dependency inhabits either terminal
package required by the exact frozen proposition
`Stage1Instances.THM_M_1241.GagliardoNirenbergTarget`. The assigned proof phase therefore remains
incomplete, the root vector remains `[H2, M3, R4]`, and no worker self-test manifest is warranted.

The unchanged minimal root cut is:

- `M1241-T-FINITE`: the arbitrary finite-`q`, finite-`r` interpolation package;
- `M1241-T-ENDPOINT`: every complementary case where `q` or `r` is infinite.

`root_of_finite_and_endpoint_packages` checks the exhaustive split and yields the exact root, but
both analytic packages are premises. It constructs neither and cannot receive root proof credit.
`Proof.lean` checks the degenerate output-exponent case `p = 0`; registry v1 contains no node for
that fragment, so it closes no frozen obligation.

Pinned mathlib exposes five nearby theorems in
`Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean`. They prove first-order Sobolev bounds for
compactly or boundedly supported functions. They do not cover arbitrary `m` and `j`, the two powered
norm factors, all finite exponents, the integer-critical branch, infinity endpoints, or Nirenberg's
zero-order exceptional hypothesis. Repository exact-topic search and comparison across the current
worker clones found no additional compatible body. Wrapping a nearby theorem as either terminal
package would substitute a strict special case for the exact target.

## Narrow validation

All commands ran inside this worker clone. The automation-provided `Formalizations/Lean/.lake`
symlink reused the canonical pinned artifacts read-only. Lean outputs were isolated under `/tmp`
and removed. No `lake update`, `lake build`, dependency clone/fetch, network request, or `.lake`
mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | The 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422, lifecycle `planned`, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828...864991e`; root M3 and both terminal packages M4. |
| isolated trust-zero Lean recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated; the composer and all three partial declarations report only `propext`, `Classical.choice`, and `Quot.sound`, and the partial declarations report sorry-free. |
| `rg -n --pcre2 '\b(?:sorry\|admit\|axiom)\b\|sorryAx\|\bunsafe\b\|implemented_by\|native_decide\|\bextern\b' Stage1_Instances/THM-M-1241 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct occurs in the owned Lean sources. |
| exact-topic search over the repository and locally pinned Lean packages | 0 | Matches reduce to this dossier, adjacent audit surfaces, and the strict first-order Sobolev module; neither terminal package has an inhabitant. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | The pinned mathlib checkout was not modified. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-e46e0735.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$lean_path" \
  lake env lean --trust=0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$tmp:$lean_path" \
  lake env lean --trust=0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_PATH="$tmp:$lean_path" \
  lake env lean --trust=0 Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Provide placeholder-free Lean implementations, or an immutable compatible dependency, for both
frozen terminal packages and their analytic supports, with exact-type transports, terminal-body
provenance, and node-scoped trust checks. A conditional assumption, the uncredited `p = 0`
fragment, a weaker Sobolev theorem, an axiom, or a placeholder is not a substitute.

This current-base recheck is nonrelease blocker evidence. It does not satisfy
`S56-M-1241-PROOF`, change scheduler state, or claim audit completion, theorem completion,
validation, release, or master acceptance. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` is intentionally absent.
