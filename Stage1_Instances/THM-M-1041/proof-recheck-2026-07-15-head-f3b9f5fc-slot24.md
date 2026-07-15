# THM-M-1041 proof recheck at `f3b9f5fc`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Base revision: `f3b9f5fc99b4675558801fcc47f610b046eb5d14`

Base tree: `5a074129aa628a1d735fc06a68164a056f1d62be`

Recorded: 2026-07-15 17:08:13 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target remains
`Stage1Instances.THM_M_1041.HilleYosidaContractionTarget`, expression SHA-256
`e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`.
It is the real Banach-space contraction Hille--Yosida equivalence, not a
statement interface or a conditional theorem.

No placeholder-free proof body for either frozen direction package exists in
the repository or pinned dependency closure. `ObligationTree.lean` contains
only the checked conditional composition
`root_of_directionPackages : ForwardPackage -> ConversePackage ->
HilleYosidaContractionTarget`; it constructs neither premise. The minimal open
root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse leaf is `M1041-C-YOSIDA-APPROX`. Closing the root
requires new formal analysis for generator closedness and density; construction
of the Laplace/Bochner resolvent with both inverse laws and its contraction
bound; and construction of the Yosida approximants and limiting semigroup with
laws, strong continuity, contraction, and exact generator identification.

The frozen statement, obligation architecture, audit input, graph, validation
specification, manifest, and toolchain are byte-identical to their state at
commit `76c08cb569093ff0ea02564e80dced5284ebd59d`. A fresh source search across
all 9676 Lean files in the pinned package cache found no Hille--Yosida theorem
or strongly-continuous-semigroup generator API. Repository history, duplicate
target `THM-M-0330`, and legacy module `S1_M_234.lean` contain only definitions,
abstract interfaces, transports, or conditional composition.

The live `mrdouglasny/hille-yosida` main revision remains
`680e9499ee866763e737c8d888c1248684ced667`. Its checked source confirms that
`Future/GenerationTheorem.lean` has only scaffolding and a trivial example;
the former density and generation axioms are commented out. Its main semigroup
module supplies prospective forward resolvent work but not generator
closedness or density, the full left inverse, or the converse. The project is
outside the pinned Lake closure and was neither fetched nor credited.
`TauCetiProject/TauCeti` remains at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`, uses Lean 4.32.0-rc1 and mathlib
`faaff5e5590ad6b6878f66d30a33ded94cd97cf6`, and is likewise not a compatible
exact proof in the pinned closure.

Assuming either direction package, weakening the equivalence, or replacing
the analytic definitions with abstract proposition fields would add an
unproved premise or prove a substituted theorem, so those routes were
rejected. The item stays `[ ]`; lifecycle stays `planned`; the root vector
stays `[H2, M4, R4]`; accepted receipt IDs stay empty; and `audit_complete` and
`theorem_complete` stay false. This pair is blocker evidence, not a proof
receipt. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The owned path was initially clean; the
only pre-existing untracked path was the automation-provided
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.
Direct Lean output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Direct pinned `lean --trust=0 -t0` replay below | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` SHA-256 was `e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`. |
| Pinned-package topical search below | 1 | Expected no-match among 9676 Lean files: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 76c08cb5 HEAD -- <proof-relevant inputs>` | 0 | Frozen statement, architecture, audit input, graph, validation specs, Lake manifest, and toolchain are unchanged. |
| `git ls-remote <both audited remotes> refs/heads/main` | 0 | Revisions remain `680e9499...d667` and `c7e69c3c...94fa`; neither project was fetched or integrated. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-f3b9f5fc-slot24.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground --kill-after=10s 600 \
  "$lean" --trust=0 -t0 --root="$target" ObligationTree.lean
```

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
