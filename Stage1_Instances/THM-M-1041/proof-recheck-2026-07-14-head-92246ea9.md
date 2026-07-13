# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Recheck date: 2026-07-14 (`Asia/Shanghai`)

Base revision: `92246ea92c0c44282c05728798bc7c7e4a5a1464`

Base tree: `bd58be98bf3046078c016d44fb4a677ea231cb23`

## Verdict

`blocked`. No placeholder-free body for the exact frozen contraction
Hille--Yosida equivalence exists in the repository or pinned dependency
closure. Neither `ForwardPackage` nor `ConversePackage` is inhabited. The
minimal root cut therefore remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; the first unavailable
converse leaf is `M1041-C-YOSIDA-APPROX`. `root_of_directionPackages` only
checks final composition after callers supply both complete directions. It is
not a proof body for either package or for the root.

This recheck found a stronger external partial candidate than the older anchor
audit recorded. `TauCetiProject/TauCeti` at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` contains sorry-free sources for a
nonnegative-time C0-semigroup API, dense generator domain, Laplace resolvent,
right-inverse identity, and contraction norm bound. Those declarations are
prospective evidence for forward children only. The project uses Lean
`4.32.0-rc1` and mathlib `faaff5e5...`, is not in this repository's pinned Lake
closure, and supplies no generator-closedness theorem, left-resolvent inverse,
Yosida approximation, or converse generation theorem. It was not fetched,
imported, built, or credited. It cannot close either direction package.

The previously audited `mrdouglasny/hille-yosida` main revision
`680e9499...d667` is compatible with this repository's Lean/mathlib pins but
is also outside the dependency closure and still lacks the converse. Its newer
branches likewise leave the generation theorem unproved. No external candidate
therefore supplies the exact root.

The root vector remains `[H2, M4, R4]`, accepted receipt IDs remain empty, and
the execution item remains `[ ]`. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All local checks used the automation-provided pinned `.lake` artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.
The isolated Lean object was created under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Expression SHA-256 `e6e5f0cb...f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | Recorded immutable candidate classifications and fail-closed root decision passed. |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e...b39c42`; root and both packages remain `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reported `[propext, Classical.choice, Quot.sound]`. |
| `git ls-remote` for both external repositories | 0 | Observed immutable heads `680e9499...d667` and `c7e69c3...d94fa`; no fetch or dependency mutation. |
| HTTPS inspection of four Tau Ceti semigroup sources plus scoped prohibited-token scan | 0 | Located the four prospective forward declarations; no `sorry`, `admit`, axiom declaration, `sorryAx`, unsafe declaration, or oracle token. This is source discovery, not a local build. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-14-head-92246ea9.json` | 0 | Current-base blocker record is valid JSON. |
| Scoped prohibited-token scan over owned `*.lean` files | 1 | Expected no-match result. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is correctly absent. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-92246ea9.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=2 LEAN_PATH="$lean_path" \
  "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=2 LEAN_PATH="$tmp:$lean_path" \
  "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Current SHA-256 values are
recorded in the paired JSON artifact.

## Retry condition

Resume after placeholder-free implementations of both frozen direction
packages and their required children become available, or after an immutable
compatible exact Lean 4 proof is integrated into the pinned dependency closure
and passes exact-type, placeholder, axiom, provenance, composition, and trust
checks. This artifact is blocker evidence, not a proof receipt or state-change
request.
