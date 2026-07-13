# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Recheck date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `a86029b30f12acc3537f70ab1c167cc25702c09b`

Base tree: `ab12055e811b574338987391b59b010338c120d2`

## Verdict

`blocked`. No placeholder-free proof body for the exact frozen contraction
Hille--Yosida equivalence exists in the repository or pinned dependency
closure. Neither `ForwardPackage` nor `ConversePackage` is inhabited, so the
minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only final composition after callers supply
both complete directions. It is not a proof body for either package or the
root.

Pinned mathlib contains the `LinearPMap`, bounded-operator, topology, and
integration substrate, but no strongly continuous semigroup generator API or
terminal Hille--Yosida theorem. The repository search found only the legacy
`S1_M_234.lean` abstract interface and the duplicate frozen target
`THM-M-0330`; neither contains the required proof bodies.

The external recheck found no exact import candidate. The compatible
`mrdouglasny/hille-yosida` revision
`680e9499ee866763e737c8d888c1248684ced667` remains outside the pinned Lake
closure and supplies prospective forward resolvent pieces only. Its
`Future/GenerationTheorem.lean` explicitly leaves generator density and the
converse as commented former axioms; it has no proof of generator closedness,
the left inverse, or generation. `TauCetiProject/TauCeti` at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` adds prospective forward density
and resolvent pieces, but uses incompatible Lean/mathlib pins and still lacks
generator closedness, the left inverse, Yosida approximation, and converse
generation. Neither candidate was fetched, integrated, built, or credited.

Closing the exact target requires new formal proofs of generator closedness
and density, a Laplace/Bochner resolvent with both inverse laws and its norm
estimate, and a Yosida-approximation semigroup construction with exact
generator identification. Assuming either direction package, weakening the
equivalence, or replacing the analytic predicates by abstract fields would be
an unproved premise or substituted theorem and was rejected.

The root vector remains `[H2, M4, R4]`, accepted receipt IDs remain empty, and
the execution item remains `[ ]`. Because the assigned proof phase is not
genuinely self-tested as complete, `.stage1-worker-selftest.json` is absent.

## Validation

All commands ran in this worker clone using the automation-provided pinned
artifacts. No `lake update`, `lake build`, dependency clone/fetch, or
dependency mutation ran. Lean object output was isolated under `/tmp` and
removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed. |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required`. |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | Recorded immutable candidate classifications and fail-closed root decision passed. |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Isolated `lake env lean --trust=0 -t0` recipe below | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reported `[propext, Classical.choice, Quot.sound]`. |
| `rg -n -i 'Hille.?Yosida\|HilleYosida\|Yosida\|strongly continuous semigroup\|C.?0 semigroup\|infinitesimal generator\|ContractingSemigroup' Formalizations/Lean/.lake/packages --glob '*.lean'` | 1 | Expected no-match result: no relevant declaration in the pinned package closure. |
| `git ls-remote --heads` for both recorded external candidates plus immutable GitHub source inspection | 0 | Re-observed the recorded revisions and their partial scope; no dependency fetch or mutation. |
| Scoped prohibited-token scan over owned `*.lean` files | 1 | Expected no-match result: no `sorry`, `admit`, axiom declaration, `sorryAx`, unsafe declaration, or oracle token. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is correctly absent. |

Exact narrow Lean recipe, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-a86029b3.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=2 LEAN_PATH="$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=2 LEAN_PATH="$tmp:$lean_path" \
  timeout 300 "$lean" --trust=0 -t0 ObligationTree.lean
```

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`. Current input SHA-256 values
are recorded in the paired JSON artifact.

## Retry condition

Resume after placeholder-free implementations of both frozen direction
packages and all their required children become available, or after an
immutable compatible exact Lean 4 proof is integrated into the pinned
dependency closure and passes exact-type, placeholder, axiom, provenance,
composition, and trust checks. This artifact is blocker evidence, not a proof
receipt or state-change request.
