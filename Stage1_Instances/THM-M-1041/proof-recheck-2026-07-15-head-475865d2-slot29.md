# THM-M-1041 proof-phase recheck at `475865d2`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded: `2026-07-15T23:21:24+08:00`

Base revision: `475865d2b8e950de525943da03cfc25ae9b14214`

Base tree: `e57db7a6052a6a249d701144f0ca4a21bec5c613`

## Verdict

`blocked`; no state change. No eligible proof body was implemented or found for
the exact root `Stage1Instances.THM_M_1041.HilleYosidaContractionTarget`.
The item remains `[ ]`, lifecycle remains `planned`, the root vector remains
`[H2, M4, R4]`, and neither audit completion nor theorem completion is claimed.

The frozen target is the full real Banach-space contraction Hille--Yosida
equivalence. A premise-free proof must inhabit both `ForwardPackage` and
`ConversePackage`. The checked `root_of_directionPackages` theorem only
composes those packages when supplied as arguments; it constructs neither and
receives no root proof credit. The minimal open root cut remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first unavailable forward leaf is `M1041-F-CLOSED`; independently, the
first unavailable converse construction is `M1041-C-YOSIDA-APPROX`. Closing
the exact target requires new proofs of generator closedness and density; a
Laplace/Bochner resolvent with both inverse laws and its contraction estimate;
and Yosida approximants, a limiting semigroup, semigroup laws, strong
continuity, contraction, and exact generator identification.

Frozen proof inputs and pins are byte-identical to their target-changing state
at `76c08cb569093ff0ea02564e80dced5284ebd59d`. Repository history, duplicate
`THM-M-0330`, and legacy `S1_M_234` contain definitions, abstract interfaces,
transports, or conditional composition only. A fresh search of all 9,676 Lean
sources in the pinned package cache found no Hille--Yosida or strongly
continuous semigroup generator declaration. The audited external candidates
remain outside the pinned closure and incomplete for the exact root; none was
fetched, built, integrated, or credited.

No simplifying inconsistency or vacuity was found. The right-neighborhood
filter at zero on `NNReal` is nontrivial, so `IsGenerator` remains substantive.
The identity semigroup and full-domain zero operator satisfy both sides in a
checked sanity example, so they give a consistent special case rather than the
universally quantified theorem. Assuming a direction package,
weakening the equivalence, or replacing the analytic predicates with abstract
fields would introduce an unproved premise or substitute another theorem.

There were 44 prior dated unresolved proof JSON records before this recheck.
This exceeds the mandatory five-tick split threshold in blueprint section
10.2. The master should accept or repair the obligation-tree prerequisite and
split this oversized proof item into dependency-legal children for the
fourteen frozen packages. This worker did not edit the authoritative DAG or
generated checklist.

## Validation

The automation-provided untracked `Formalizations/Lean/.lake` symlink to the
canonical pinned cache was reused read-only. No `lake update`, `lake build`,
dependency clone/fetch/checkout, or `.lake` mutation was performed. Lean
object output was isolated under `/tmp` and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234 remains `planned`, L0/rework-required, and `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | Passed 21 obligations and 56 typed edges; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both direction packages remain M4. |
| Direct pinned `lake env lean --trust=0 -t0` replay below | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reported `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` SHA-256 was `e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`. |
| `(cd Formalizations/Lean && lake env lean --trust=0 -t0 /tmp/THMM1041Vacuity.lean)` | 0 | Scratch-only zero-operator sanity example elaborated; output contained three `unnecessarySimpa` linter warnings and no errors. The temporary source SHA-256 was `bcafef4607415c927174b562e39708cdfbd88620a2d47a9515dcb76492328925`; it created no repository file or object. |
| Pinned-package topical scan below | 1 expected | No match among 9,676 pinned Lean source files. |
| Scoped prohibited-token scan below | 1 expected | No prohibited proof-device token in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 76c08cb5...59d HEAD -- <proof inputs and pins>` | 0 | Statement, composition, registry, graphs, audit, validation specs, Lake manifest, and toolchain are unchanged. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest was absent because the proof phase is incomplete. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-475865d2-slot29.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
base_lean_path=$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)
cd "$lean_root"
LEAN_NUM_THREADS=1 timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
  -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$base_lean_path" \
  timeout --foreground --kill-after=10s 600 \
  lake env lean --trust=0 -t0 --root="$target" \
  "$target/ObligationTree.lean"
```

The replay ran from `2026-07-15T23:18:35+08:00` through
`2026-07-15T23:18:41+08:00`.

Pinned-package search:

```bash
rg --no-ignore -n -i \
  'Hille.?Yosida|HilleYosida|Yosida|strongly continuous semigroup|C.?0 semigroup|infinitesimal generator|ContractionSemigroup|ContractingSemigroup' \
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

The master should accept or repair the obligation-tree prerequisite and split
this proof item into dependency-legal children for the fourteen frozen
packages. Then implement them without placeholders. The alternative is an
immutable compatible exact Lean 4 proof already in the pinned closure that
passes exact-type, provenance, placeholder, axiom, composition, and trust
checks.

This is fresh current-base, warm-cache, nonrelease blocker evidence only. It
does not satisfy `S56-M-1041-PROOF`, change scheduler state, close either
direction package or the root, or claim audit completion, theorem completion,
validation, release, receipt acceptance, or master acceptance. Because the
proof phase is not genuinely complete, `.stage1-worker-selftest.json` is
deliberately absent.
