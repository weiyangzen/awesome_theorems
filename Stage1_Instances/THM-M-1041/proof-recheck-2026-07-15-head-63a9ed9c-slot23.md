# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T12:58:43+08:00` (`Asia/Shanghai`)

Base revision: `63a9ed9c4aae594da31423142b0658129d5452a7`

Base tree: `7bee4fac4489bad36fd615a023df13bb294d1781`

## Verdict

`blocked`. The frozen root is the complete real contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof body for this equivalence is present
in the repository or the pinned Lake dependency closure. Neither
`ForwardPackage` nor `ConversePackage` is inhabited, so the minimal open root
cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` is only checked conditional composition after a
caller supplies both complete directions. `target_iff_expanded` is only
definitional transport. Neither closes a substantive proof obligation.

The proof-relevant owned inputs are byte-identical to the last integrated
recheck. Repository history, duplicate target `THM-M-0330`, and legacy module
`S1_M_234` contain definitions, abstract fields, transports, or the same
conditional architecture, not either direction package. A source search over
every package in the pinned cache found no Hille--Yosida theorem or strongly
continuous semigroup generator API.

The already audited external candidates remain insufficient. The immutable
revision `680e9499ee866763e737c8d888c1248684ced667` of
`mrdouglasny/hille-yosida` provides partial forward resolvent infrastructure,
but no proof of generator closedness or density, no resolvent left inverse,
and no converse. Its generation module is scaffolding rather than a proof.
The `jagg-ix/HilleYosida` fork adds no closure, and TauCeti revision
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa` is partial and toolchain
incompatible. All candidates are outside the pinned dependency closure. No
dependency was cloned, fetched, built, integrated, or credited during this
run. A live remote query was attempted but timed out without output, so this
run makes no claim that branch heads changed or remained fixed.

Closing the exact root requires new formal proofs of generator closedness and
density, a Laplace/Bochner resolvent with both inverse laws and its contraction
estimate, and the Yosida-approximation semigroup construction with exact
generator identification. Alternatively, an immutable compatible exact proof
must enter the pinned closure and pass exact-type, provenance, placeholder,
axiom, composition, and trust checks. Assuming a direction package, weakening
the equivalence, or replacing the analytic definitions with abstract fields
would prove a different theorem and is prohibited.

The item remains `[ ]`; lifecycle remains `planned`; root vector remains
`[H2, M4, R4]`; accepted receipt IDs remain empty. This pair is blocker
evidence, not a proof receipt or item-state request. Because the proof phase is
incomplete, `.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The initial owned path was clean, with
only the automation-provided untracked `Formalizations/Lean/.lake` symlink to
the canonical pinned cache. No `lake update`, `lake build`, dependency clone or
fetch, or `.lake` mutation ran. Lean object output was isolated under `/tmp`
and removed on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 1 | The helper could not resolve `HEAD` in the automation-provided incomplete `flt-regular` cache. No dependency repair or fetch was attempted. The direct narrow Lean replay below independently elaborated the unchanged exact statement. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain `M4`. |
| Direct pinned `lean --trust=0 -t0` replay below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration in any pinned package source. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources. This lexical scan is supporting evidence only. |
| `git diff --quiet e813a541... HEAD -- <proof-relevant inputs>` | 0 | Statement, obligation architecture, audit input, manifest, and toolchain files are unchanged since the last integrated recheck. |
| `git ls-remote https://github.com/mrdouglasny/hille-yosida.git refs/heads/main` | 130 | Timed out without output and was interrupted; no remote-state claim or proof credit is based on it. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-15-head-63a9ed9c-slot23.json` | 0 | The structured blocker artifact is valid JSON. |
| `test ! -e .stage1-worker-selftest.json` | 0 | The completion self-test manifest is absent, as required for the incomplete phase. |
| `git diff --check -- Stage1_Instances/THM-M-1041` plus added-file `git diff --no-index --check` checks | 0 / 1 | No whitespace diagnostics; exit 1 from each no-index invocation is the expected added-file status. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-63a9ed9c-slot23.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
mathlib=$lean_root/.lake/packages/mathlib
lean=$(cd "$mathlib" && lake env which lean)
lake_path=$(cd "$mathlib" && lake env printenv LEAN_PATH)
cache_path=$(find "$lean_root/.lake/packages" -type d \
  -path '*/.lake/build/lib/lean' -print | sort | paste -sd:)
lean_path="$cache_path:$lake_path:$lean_root/.lake/build/lib/lean"
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" \
  timeout --foreground 600 "$lean" --trust=0 -t0 --root="$target" \
    ObligationTree.lean
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
