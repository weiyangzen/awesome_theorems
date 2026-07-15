# THM-M-1241 proof-phase recheck at current base

Item: `S56-M-1241-PROOF`

Recheck time: `2026-07-15T11:47:58+08:00` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. No placeholder-free local body or immutable pinned dependency inhabits either terminal
package required by the exact frozen proposition
`Stage1Instances.THM_M_1241.GagliardoNirenbergTarget`. The proof phase remains incomplete, the root
vector remains `[H2, M3, R4]`, and no worker self-test manifest is warranted.

The unchanged minimal root cut is:

- `M1241-T-FINITE`: arbitrary finite-`q`, finite-`r` interpolation;
- `M1241-T-ENDPOINT`: every complementary case where `q` or `r` is infinite.

`root_of_finite_and_endpoint_packages` checks the exact exhaustive composition, but both packages
are premises and it constructs neither. `Proof.lean` checks only the degenerate output-exponent
case `p = 0`; registry v1 assigns that fragment no obligation, so it closes no frozen node.
`M1241-B-ZERO` instead denotes the source's exceptional `j = 0` endpoint branch.

Pinned mathlib exposes five nearby first-order compact- or bounded-support Sobolev estimates in
`Mathlib/Analysis/FunctionalSpaces/SobolevInequality.lean`. They do not cover arbitrary `m` and
`j`, the powered two-norm interpolation product, all finite exponents, the integer-critical branch,
infinity endpoints, or the exact zero-order exceptional hypothesis. Using one as either terminal
package would substitute a strict special case for the frozen theorem.

All worker clones currently contain the same `Proof.lean` body (SHA-256
`b4703ca1b688f9160edfabdff02e4c759f0bb3ec48fe2092811b56d048c03653`); no newer exact body is
available in the automation clones.

## Narrow validation

All commands ran inside this worker clone. The automation-provided `Formalizations/Lean/.lake`
symlink reused canonical artifacts without updating, building, fetching, cloning, or otherwise
mutating them. Lean outputs were isolated under `/tmp` and removed.

The canonical shared `flt-regular` package directory is presently incomplete: its `HEAD` points to
`refs/heads/.invalid`, it has no worktree, and it does not contain the manifest-pinned commit
`56161b6eb5281fbfe9c38f2bcec0f429ebc11a27`. Consequently, deriving the complete environment with
`cd Formalizations/Lean && lake env printenv LEAN_PATH` fails. The scoped replay instead constructed
`LEAN_PATH` only from the already present root and package build-library directories, then invoked
the required `lake env lean` from the target directory. This is useful nonrelease evidence for the
three existing modules, not proof-phase completion and not a pinned-environment integrity claim.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and exactly 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets, ranks 1 through 1546, all L0/rework-required. |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | Rank 422, lifecycle `planned`, theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1241/check_obligation_tree.py` | 0 | 15 obligations and 31 typed edges passed; denominator `d2173828...864991e`; root M3 and both terminal packages M4. |
| scoped trust-zero `lake env lean` recipe below | 0 | `Statement.lean`, `ObligationTree.lean`, and `Proof.lean` elaborated; the composer and all three partial declarations report only `propext`, `Classical.choice`, and `Quot.sound`; all partial declarations report sorry-free. |
| `python3 Stage1_Instances/THM-M-1241/check_statement.py` | 1 | Environment blocker: Lake could not resolve the incomplete shared `flt-regular` checkout's `HEAD`; no dependency repair or fetch was attempted. |
| `rg -n --pcre2 '\b(?:sorry|admit|axiom)\b|sorryAx|\bunsafe\b|implemented_by|native_decide|\bextern\b' Stage1_Instances/THM-M-1241 --glob '*.lean'` | 1 | Expected no-match result: no prohibited proof device occurs in the owned Lean sources. |
| exact terminal-package inhabitant scan over repository Lean sources | 1 | Expected no-match result: neither frozen terminal package has a proof body. |
| `git -C Formalizations/Lean/.lake/packages/mathlib diff --quiet` | 0 | The pinned mathlib checkout was not modified. |
| `git diff --check -- Stage1_Instances/THM-M-1241` | 0 | No whitespace errors before this artifact was added. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest deliberately absent. |

The successful Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1241
tmp=$(mktemp -d /tmp/thm-m-1241-slot50-current.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean"
while IFS= read -r d; do
  lean_path="$lean_path:$repo_root/$d"
done < <(find Formalizations/Lean/.lake/packages \
  -path '*/.lake/build/lib/lean' -type d -print | sort)
cd "$target"
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 -o "$tmp/ObligationTree.olean" ObligationTree.lean
ELAN_TOOLCHAIN=leanprover/lean4:v4.29.0 LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 lake env lean --trust=0 -t0 Proof.lean
```

Pinned identities observed for the usable portion of the environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake `5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry condition

Provide placeholder-free Lean implementations, or an immutable compatible dependency, for both
frozen terminal packages and their analytic supports, with exact-type transports, terminal-body
provenance, and node-scoped trust checks. Restore the manifest-pinned `flt-regular` artifact through
the scheduler's canonical cache-provisioning lane before rerunning full environment-derived checks;
workers must not fetch or repair `.lake`.

A conditional assumption, the uncredited `p = 0` fragment, a weaker Sobolev theorem, an axiom, or a
placeholder is not a substitute. This current-base artifact is nonrelease blocker evidence. It does
not satisfy `S56-M-1241-PROOF`, change scheduler state, or claim audit completion, theorem completion,
validation, release, or master acceptance. Because the assigned phase is not genuinely complete,
`.stage1-worker-selftest.json` is intentionally absent.
