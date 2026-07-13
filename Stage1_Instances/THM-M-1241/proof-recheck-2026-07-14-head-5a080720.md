# THM-M-1241 partial proof execution at current base

Item: `S56-M-1241-PROOF`

Run date: 2026-07-14 (`Asia/Shanghai`)

Base revision: `5a080720059200b542aa35ee17a748b3251fe8d0`

Base tree: `d7029aa7599db39fbcc55e968a4fe70376143f27`

## Verdict

`blocked`, with genuine but nonclosing proof progress. `Proof.lean` adds three unconditional,
placeholder-free declarations for the degenerate output exponent `p = 0`. Mathlib defines
`eLpNorm _ 0 _ = 0`, so the finite supremum `derivativeLpNorm j 0 u` vanishes and the exact
`ParameterConclusion n m j q r 0 a` follows uniformly with `C = 1`. The third declaration checks
that `reciprocalExponent p = 0` means exactly `p = 0` or `p = infinity`.

These declarations do not prove the classical analytic content. Registry v1 contains no separate
`p = 0` node, so this work closes no frozen obligation and does not change the recorded root vector
`[H2, M3, R4]`. The immediate root cut remains:

- `M1241-T-FINITE`, the exact package for arbitrary finite `q` and `r`;
- `M1241-T-ENDPOINT`, every complementary case where `q` or `r` is infinite.

The checked theorem `root_of_finite_and_endpoint_packages` consumes both packages and constructs
neither. Pinned mathlib's five nearby declarations are first-order compact- or bounded-support
Sobolev inequalities. They do not supply arbitrary `m,j`, two powered norms, the critical branch,
infinity endpoints, or the exact zero-order exceptional hypothesis.

## Narrow validation

All commands ran in this worker clone using the automation-provided symlink to existing canonical
pinned Lake artifacts. Lean outputs were isolated under `/tmp` and removed. No `lake update`,
`lake build`, dependency clone/fetch, network action, or `.lake` mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; planned; hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828...864991e`; root open at M3 with both packages M4. |
| isolated trust-zero Lean recipe below | 0 | Statement, conditional tree, and all three partial declarations elaborated; each declaration is sorry-free and reports only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|\\bunsafe\\b|implemented_by|native_decide|\\bextern\\b' Stage1_Instances/THM-M-1241 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct in the owned Lean sources. |
| scoped exact-topic search over repository and pinned packages | 0 | Only this dossier, historical audit surfaces, and strict Sobolev special cases were found; neither package has an inhabitant. |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/proof-partial-receipt.json` | 0 | Partial receipt is valid JSON. |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/proof-recheck-2026-07-14-head-5a080720.json` | 0 | Current-base blocker record is valid JSON. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-proof-final.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 Proof.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Resume after placeholder-free implementations of both frozen terminal packages and their analytic
supports, or after an immutable compatible Lean dependency supplies exact terminal bodies that can
be pinned, transported, and checked locally. A conditional premise, the uncredited `p = 0`
fragment, a weaker Sobolev case, an axiom, or a placeholder is not a substitute.

This is nonrelease partial-proof and blocker evidence. It does not satisfy the assigned proof item
or support validation, release, audit completion, theorem completion, scheduler state, or master
acceptance. Because the proof phase is incomplete, `.stage1-worker-selftest.json` remains absent.
