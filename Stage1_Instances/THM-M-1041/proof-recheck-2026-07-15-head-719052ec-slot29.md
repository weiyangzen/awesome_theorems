# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T14:36:19+08:00` (`Asia/Shanghai`)

Base revision: `719052ec5fae5190f38e013d646fd7461d29be5d`

Base tree: `a8de041884ae39d41031493cb436b3e4a66bbfa0`

## Verdict

`blocked`. The frozen target is the full real contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof body for the target exists in the
repository or pinned dependency closure. Neither `ForwardPackage` nor
`ConversePackage` is inhabited, so the minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only conditional composition after a caller
supplies both complete directions. `target_iff_expanded` is only a
definitional transport. Neither declaration supplies a proof body for the
exact root.

The frozen statement, obligation architecture, audit input, and pins are
unchanged since the latest target-changing commit. Repository history,
duplicate target `THM-M-0330`, and legacy module `S1_M_234` contain
definitions, abstract interfaces, transports, or the same conditional
architecture, not either direction package. A fresh search across every
pinned package source found no Hille--Yosida theorem or strongly continuous
semigroup generator API.

The audited external candidates do not close the root.
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667` supplies prospective forward
resolvent pieces but no generator closedness or density, no resolvent left
inverse, and no converse. TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` remains partial and uses
incompatible pins. The separately observed Spectra Yosida development proves
Stone's theorem for self-adjoint operators on complex Hilbert spaces, not the
frozen theorem for arbitrary real Banach-space contraction generators. None
is in the pinned closure, and no dependency was cloned, fetched, built,
integrated, or credited.

Closing the root requires new formal proofs of generator closedness and
density, a Laplace/Bochner resolvent with both inverse laws and its norm
estimate, and the Yosida-approximation semigroup construction with exact
generator identification. Alternatively, an immutable compatible exact proof
must enter the pinned dependency closure. Assuming a direction package,
weakening the equivalence, or replacing analytic predicates with abstract
fields would add an unproved premise or prove a different theorem.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; accepted receipt IDs stay empty. This pair is blocker
evidence, not a proof receipt or state-change request. Because the proof phase
is incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The initial owned path was clean; the
only untracked entry was the automation-provided `Formalizations/Lean/.lake`
symlink to the canonical pinned cache. No `lake update`, `lake build`,
dependency clone/fetch, or `.lake` mutation ran. Direct Lean output was
isolated under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both directions remain `M4`. |
| Direct pinned `lake env lean --trust=0 -t0` replay below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration in any pinned source. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources. This lexical scan is supporting evidence only. |
| `git diff --quiet db0c2980 HEAD -- <proof-relevant inputs>` | 0 | Frozen statement, architecture, audit input, manifest, and toolchain are unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent, as required for the incomplete phase. |

Exact narrow Lean replay, run from the repository root with `lake env lean`
from the pinned mathlib checkout:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
mathlib=$lean_root/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-719052ec-slot29.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean_path="$lean_root/.lake/build/lib/lean:$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean"
for d in "$lean_root"/.lake/packages/*/.lake/build/lib/lean; do
  lean_path="$lean_path:$d"
done
cd "$mathlib"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
    "$target/ObligationTree.lean"
```

The replay ran from `2026-07-15T14:30:02+08:00` through
`2026-07-15T14:30:24+08:00`. Both commands exited 0. The temporary
`Statement.olean` SHA-256 was
`e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`.

Pinned-package search:

```bash
rg -n -i \
  'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator|ContractionSemigroup' \
  Formalizations/Lean/.lake/packages --glob '*.lean'
```

Scoped prohibited-token scan:

```bash
rg -n -i \
  '\b(sorry|admit|sorryAx|unsafe|oracle)\b|(^|[^A-Za-z])(axiom|opaque)[[:space:]]' \
  Stage1_Instances/THM-M-1041 --glob '*.lean'
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages are available in the pinned closure, or after an
immutable compatible exact Lean 4 proof is pinned/imported and passes
exact-type, provenance, placeholder, axiom, composition, and trust checks.
