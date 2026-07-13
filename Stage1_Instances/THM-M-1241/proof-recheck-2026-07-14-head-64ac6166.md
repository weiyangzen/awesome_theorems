# THM-M-1241 proof-phase recheck at current base

Item: `S56-M-1241-PROOF`

Recheck date: 2026-07-14 (Asia/Shanghai)

Base revision: `64ac616628d97140f9ca64eff0298e51d7f4e9ff`

Base tree: `9ef0acd5b747e34cacb82c6f21fce1e1380e0cf2`

## Verdict

`blocked`. No eligible proof body was found for either terminal package required by the exact
frozen proposition `Stage1Instances.THM_M_1241.GagliardoNirenbergTarget`. No proof source was
added, the root remains `[H2, M3, R4]`, and the assigned proof item remains `[ ]`.

The immediate root cut set is unchanged:

- `M1241-T-FINITE`, the Gagliardo-Nirenberg inequality for arbitrary finite `q` and `r`;
- `M1241-T-ENDPOINT`, every complementary case where `q` or `r` is infinite.

`root_of_finite_and_endpoint_packages` kernel-checks the exhaustive split and returns the exact
root, but both packages are premises. It does not construct either one. Treating this conditional
composition as root closure would hide the entire analytic theorem behind assumptions.

Pinned mathlib's five nearby declarations in
`Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean` are genuine first-order Sobolev
inequalities for compactly or boundedly supported functions. None proves arbitrary derivative
orders `m,j`, the product of powered `L^r` and `L^q` norms, every finite exponent, the
integer-critical branch, infinity endpoints, or the exact zero-order exceptional hypothesis.
Consequently no exact wrapper can inhabit either frozen package.

The target is not vacuous and no elementary proof or counterexample was found. The missing
explicit hypothesis `1 <= p` admits some `p = 0` cases because `reciprocalExponent 0 = 0`; those
cases are trivial since mathlib defines `eLpNorm _ 0 _ = 0`. They do not trivialize the required
positive finite-exponent family or the `p = infinity` endpoint cases.

## Validation

All checks ran in this worker clone. Lean outputs were confined to `/tmp` and removed by a shell
trap. The automation-provided untracked `Formalizations/Lean/.lake` symlink was reused read-only.
No `lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation ran.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422; planned; hard-mathlib lane; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828...864991e`; root open at M3, both terminal packages M4. |
| isolated trust-zero Lean recipe below | 0 | Exact statement, conditional composition, and all five pinned anchors elaborated; the printed declarations report only `propext`, `Classical.choice`, and `Quot.sound`. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1241 --glob '*.lean'` | 1 | Expected no-match result: no prohibited construct in the owned Lean sources. |
| scoped exact-topic declaration search over the repository and pinned packages | 0 | Only this statement/composition, adjacent audit surfaces, and strict first-order Sobolev special cases were found; neither terminal package has an inhabitant. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-proof-recheck-full.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_PATH="$lean_path" "$lean" --trust=0 -o "$tmp/Statement.olean" Statement.lean
LEAN_PATH="$tmp:$lean_path" "$lean" --trust=0 ObligationTree.lean
LEAN_PATH="$lean_path" "$lean" --trust=0 AnchorAudit.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Exact input hashes are recorded in the adjacent
JSON blocker artifact.

## Retry Condition

Resume after placeholder-free implementations of both frozen terminal packages and their analytic
supports, or after an immutable compatible Lean dependency supplies exact terminal bodies that can
be pinned, transported, and checked locally. A conditional premise, weaker Sobolev special case,
axiom, placeholder, or altered endpoint statement is not an acceptable substitute.

This is fresh negative proof evidence, not a proof receipt. It does not satisfy
`S56-M-1241-PROOF` or support audit completion, theorem completion, validation, release, or master
acceptance. Because the assigned phase is not genuinely self-tested complete,
`.stage1-worker-selftest.json` remains absent.
