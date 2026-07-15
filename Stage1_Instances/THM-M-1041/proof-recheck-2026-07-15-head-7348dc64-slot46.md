# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T08:57:23+08:00` (`Asia/Shanghai`)

Base revision: `7348dc646fd6babfe2b82c35b4c03a9ed5921f8e`

Base tree: `ddd6941316b5d4a9d6574d9532212c24de6fe516`

## Verdict

`blocked`. The exact frozen root is the complete real contraction
Hille--Yosida equivalence for every partially defined real-linear operator on
every real Banach space. No placeholder-free proof body for that equivalence
is present in this repository or its pinned Lake dependency closure. Neither
`ForwardPackage` nor `ConversePackage` is inhabited, so the minimal open root
cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` checks only the final composition after a caller
supplies both complete directions. It constructs neither package and is not a
premise-free root proof. `target_iff_expanded` is only definitional transport.

The proof-relevant owned inputs are unchanged. Repository history, duplicate
target `THM-M-0330`, and legacy module `S1_M_234` contain definitions,
abstract proposition fields, transports, or the same conditional architecture,
not a terminal proof of either direction. Pinned mathlib supplies functional
analysis substrate but no Hille--Yosida theorem or strongly continuous
semigroup generator API.

The audited external candidates are also insufficient. The main branch of
`mrdouglasny/hille-yosida` remains at
`680e9499ee866763e737c8d888c1248684ced667`; its prospective forward work lacks
generator closedness and density, the resolvent left inverse, and the converse.
TauCeti remains at `c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`; it is partial,
uses incompatible pins, and likewise supplies no converse. Both projects are
outside the pinned Lake closure. This run queried only remote branch metadata;
neither project was cloned, fetched, built, integrated, or credited.

Closing the root requires new formal proofs of generator closedness and
density, a Laplace/Bochner resolvent with both inverse laws and its contraction
estimate, and the Yosida-approximation semigroup construction with exact
generator identification. Alternatively, an immutable compatible exact proof
must enter the pinned closure and pass exact-type, provenance, placeholder,
axiom, composition, and trust checks. Assuming a direction package, weakening
the equivalence, or replacing the analytic facts with abstract fields would
prove a different theorem and is prohibited.

The item remains `[ ]`; lifecycle remains `planned`; root vector remains
`[H2, M4, R4]`; accepted receipt IDs remain empty. This pair is blocker
evidence, not a proof receipt or item-state request. Because the proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. Initial and final clean-path checks
showed only the automation-provided untracked `Formalizations/Lean/.lake`
symlink to the canonical pinned cache before this evidence pair was added. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.
Lean object output was isolated under `/tmp` and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Isolated `lake env` discovery plus `lean --trust=0 -t0` recipe below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-mathlib topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources. This lexical scan is supporting evidence only. |
| `git ls-remote` for both audited external main branches | 0 | Candidate revisions remain `680e9499...d667` and `c7e69c3c...94fa`; neither is in the pinned closure. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-15-head-7348dc64-slot46.json` | 0 | The structured blocker artifact is valid JSON. |
| `git diff --no-index --check /dev/null <new-artifact>` for each evidence file | 1 | Expected added-file status with no whitespace diagnostics for either file. |

The target statement checker was started but cancelled after 120 seconds under
heavy concurrent Lean load, so it is not counted as a passing command in this
run. It removed its temporary mutation sources when interrupted. The direct
trust-zero replay independently elaborated the unchanged canonical statement;
the frozen expression fingerprint remains
`e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`.

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-7348dc64-slot46.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && timeout 120 lake env which lean)
lean_path=$(cd "$lean_root" && timeout 120 lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    ObligationTree.lean
```

Pinned-mathlib search:

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
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages are available in the pinned closure, or after an
immutable compatible exact Lean 4 proof is pinned/imported and passes
exact-type, provenance, placeholder, axiom, composition, and trust checks.
