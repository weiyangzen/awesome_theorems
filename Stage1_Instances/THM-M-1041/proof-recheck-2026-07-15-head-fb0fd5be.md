# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T05:31:38+08:00` (`Asia/Shanghai`)

Base revision: `fb0fd5be494d0813177dbdc959ec911d69a72015`

Base tree: `f6d39faae5fb024a71ee786e7a6b017d335841cd`

## Verdict

`blocked`. The exact frozen target is the full contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof body for that target exists in the
repository or pinned dependency closure. Neither `ForwardPackage` nor
`ConversePackage` is inhabited, so the minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only the final composition after a caller
supplies both complete directions. It is not a proof body for either package
or for the premise-free root. `target_iff_expanded` is only a definitional
transport between two parenthesizations of the same proposition.

Repository history, the duplicate `THM-M-0330` target, and the legacy
`S1_M_234` module contain only the same conditional architecture or abstract
interfaces. Pinned mathlib has `LinearPMap`, topology, integration, and
bounded-operator substrate but no Hille--Yosida theorem or strongly continuous
semigroup generator API. Generic resolvent theorems for bounded elements of a
unital algebra do not apply to the frozen unbounded `LinearPMap` target.

The audited external projects are not closure candidates for this phase.
`mrdouglasny/hille-yosida` at
`680e9499ee866763e737c8d888c1248684ced667` lies outside the pinned Lake
closure and supplies only prospective forward resolvent pieces. TauCeti at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` also lies outside the closure,
uses incompatible Lean/mathlib pins, and still lacks generator closedness,
the left inverse, Yosida approximation, and the converse generation theorem.
Neither project was fetched, built, integrated, or credited.

No shortcut through the statement exists. The right-neighborhood filter on
`NNReal` is nontrivial and normed-space limits are unique, so `IsGenerator` is
not vacuous. The identity semigroup with the zero generator is only a
consistent special case. The two resolvent inverse laws and norm estimate are
substantive. Assuming either direction package, weakening the equivalence, or
replacing its analytic predicates with abstract fields would add an unproved
premise or substitute another theorem.

Closing the root requires new formal proofs of generator closedness and
density, the Laplace/Bochner resolvent with both inverse laws and its norm
estimate, and the Yosida-approximation semigroup construction with exact
generator identification. Alternatively, an immutable compatible exact proof
must enter the pinned dependency closure and pass the exact-type, provenance,
placeholder, axiom, composition, and trust gates.

The item remains `[ ]`, lifecycle remains `planned`, the root vector remains
`[H2, M4, R4]`, and accepted receipt IDs remain empty. This is blocker
evidence, not a proof receipt or state-change request. Because the proof phase
is not genuinely self-tested as complete, `.stage1-worker-selftest.json` is
deliberately absent.

## Validation

All commands ran in the worker clone against the automation-provided pinned
`.lake` artifacts. No `lake update`, `lake build`, dependency clone/fetch, or
dependency mutation ran. The shared canonical cache and dirty symlink make
these nonrelease checks. Lean object output was isolated under `/tmp` and
removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations were killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok`. |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and conditional composition elaborated with no errors. `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-mathlib topical search below | 1 | Expected no-match result: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match result: no `sorry`, `admit`, `sorryAx`, unsafe/oracle shortcut, axiom declaration, or opaque declaration in owned Lean sources. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is correctly absent. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-fb0fd5be.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=2 LEAN_PATH="$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=2 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned-mathlib topical search:

```bash
rg -n -i \
  'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator|ContractionSemigroup' \
  Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'
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
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Exact source and dependency
input hashes are recorded in the paired JSON artifact.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages are available in the pinned closure, or after an
immutable compatible exact Lean 4 proof is pinned/imported and passes
exact-type, provenance, placeholder, axiom, composition, and trust checks.
