# THM-M-1041 proof recheck at `b73dae2e`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Base revision: `b73dae2e6741a0be1f316d748a37f487a671cca4`

Base tree: `d582d50d420e2a27b4fb21ed0abea58cee03184f`

Recorded: 2026-07-15 20:50:01 +08:00

## Verdict

`blocked`; no state change.

The frozen target is the full real Banach-space contraction Hille--Yosida
equivalence, `Stage1Instances.THM_M_1041.HilleYosidaContractionTarget`, with
expression SHA-256
`e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`.
A premise-free root proof must inhabit both `ForwardPackage` and
`ConversePackage`. The existing `root_of_directionPackages` only composes
those two arguments; it constructs neither package and receives no root proof
credit.

The proof-relevant inputs and pins are unchanged from the latest integrated
target recheck based at `f976b9b21418bfda4bc815ba2a7238e932666231`.
Fresh structural checks and a direct trust-level-zero Lean replay pass, but
they continue to report the root and both direction packages at `M4`. A fresh
search of every pinned package source returns no Hille--Yosida theorem or
strongly-continuous-semigroup generator API.

The minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`. Closing
the exact target requires new proofs of generator closedness and density; a
Laplace/Bochner resolvent with both inverse laws and its contraction estimate;
and the Yosida approximants, limiting semigroup, semigroup laws, strong
continuity, contraction, and exact generator identification. The audited
external candidates are outside the pinned dependency closure and incomplete
for this root. Assuming a direction package, weakening the equivalence, or
moving the missing analysis into abstract fields is prohibited.

The item remains `[ ]`; lifecycle remains `planned`; the root vector remains
`[H2, M4, R4]`; no proof body, closed obligation, composition certificate, or
accepted receipt was added. `audit_complete` and `theorem_complete` remain
false. This is blocker evidence, not a proof receipt or state request. Because
the assigned proof phase is incomplete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All commands ran in this worker clone. Initial status showed only the
automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned cache. No `lake update`, `lake build`, dependency clone or
fetch, or `.lake` mutation ran. Lean object output was isolated under `/tmp`
and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 above; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both packages remain `M4`. |
| Direct pinned `lean --trust=0 -t0` replay | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical `rg` search | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token `rg` scan | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet f976b9b2^..HEAD -- <proof-relevant inputs>` | 0 | Frozen proof inputs and pins are unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-b73dae2e.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout --foreground 600 \
  "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout --foreground 600 \
  "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of every child needed for both
frozen direction packages are available in the pinned closure, or after an
immutable compatible exact Lean 4 proof is pinned/imported and passes
exact-type, provenance, placeholder, axiom, composition, and trust checks.
