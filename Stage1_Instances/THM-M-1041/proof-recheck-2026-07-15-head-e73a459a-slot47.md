# THM-M-1041 proof recheck at `e73a459a`

Item: `S56-M-1041-PROOF`

Intent: `prove`

Base revision: `e73a459aa33f8b656019c9c36e3d5dfc84dffc30`

Base tree: `81105927f8e46d0076dd20433240ecf0fd185cea`

Recorded: 2026-07-15 18:35:37 +08:00

## Verdict

`blocked`; no state change.

The exact frozen target is the real Banach-space contraction Hille--Yosida
equivalence in `Statement.lean`, expression SHA-256
`e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`.
A proof must inhabit both `ForwardPackage` and `ConversePackage` from
`ObligationTree.lean`. The existing theorem `root_of_directionPackages` only
composes those packages after receiving them as premises; it constructs
neither one.

No placeholder-free body for either direction package exists in the
repository or pinned Lake dependency closure. The minimal root cut remains
`{M1041-F-ASSEMBLE, M1041-C-ASSEMBLE}`. The first unavailable forward leaf is
`M1041-F-CLOSED`, generator closedness for the frozen `IsGenerator`
definition. Independently, the first unavailable converse construction is
`M1041-C-YOSIDA-APPROX`. All fourteen substantive direction obligations remain
without terminal bodies.

The frozen proof inputs and dependency pins are byte-identical to their last
target-changing revision, `76c08cb569093ff0ea02564e80dced5284ebd59d`.
Repository history, duplicate target `THM-M-0330`, and legacy module
`S1_M_234.lean` contain definitions, abstract interfaces, transports, or
conditional composition only. A source search across all 9676 Lean files in
the existing pinned package cache found no Hille--Yosida theorem or strongly
continuous-semigroup generator API.

Additional kernel-checked sanity probes found no inconsistency or vacuity.
The right-neighborhood filter at zero on `NNReal` is nontrivial, normed-space
limits are unique, and the generator relation fixes graph values rather than
accepting arbitrary ones. The identity semigroup with the full-domain zero
operator and resolvent `a^-1 * id` supplies a consistent nonzero-space special
case. That witness does not prove the universal theorem over every Banach
space and operator.

The immutable external candidates still do not supply the exact root.
`mrdouglasny/hille-yosida` at `680e9499...d667` contains partial forward
Laplace-resolvent work but omits generator closedness and density, the left
inverse, and the converse; it is outside the pinned closure. TauCeti at
`c7e69c3...d94fa` is also outside the closure, uses incompatible pins, and is
incomplete. The separately observed Spectra Yosida development is a
placeholder-free Stone-theorem route for self-adjoint operators on complex
Hilbert spaces, unitary real-time groups, and off-real-axis resolvents. It
cannot type-preservingly close any frozen arbitrary-real-Banach contraction
obligation and uses Lean 4.31.0-rc1 with mathlib `40f05009...`, not the pinned
environment. No external dependency was cloned, fetched, built, integrated,
or credited.

Closing the exact target requires new formal analysis: generator closedness
and density; the Laplace/Bochner resolvent with both inverse laws and its
contraction estimate; and the real-Banach Yosida approximation, limiting
semigroup, laws, continuity, contraction, and exact generator identification.
Assuming either direction package, weakening the equivalence, or replacing
the analytic definitions with abstract fields would add an unproved premise
or prove a substituted theorem.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; accepted receipt IDs stay empty; and `audit_complete` and
`theorem_complete` stay false. This pair is blocker evidence, not a proof
receipt. Because the assigned proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. The owned path was initially clean; the
only pre-existing untracked path was the automation-provided
`Formalizations/Lean/.lake` symlink to canonical pinned artifacts. No
`lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation ran.
Direct Lean output and sanity probes were isolated under `/tmp` and removed or
left outside the repository.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both packages remain `M4`. |
| Direct pinned `lean --trust=0 -t0` replay below | 0 | Exact statement and conditional composition elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`; temporary `Statement.olean` SHA-256 `e2a26c6ee6807a3deaeb3c3cdc46e1802e989fba1e463a7ca46712689748caca`. |
| Pinned-package topical search below | 1 | Expected no-match over 9676 Lean source files: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources; supporting lexical evidence only. |
| `git diff --quiet 76c08cb5 HEAD -- <proof-relevant inputs>` | 0 | Frozen statement, composition, registry, typed graphs, audit, validation specs, manifest, and toolchain are unchanged. |
| Three pinned `/tmp` sanity modules | 0 | Nontrivial right filter and limit uniqueness, generator behavior, resolvent bijectivity, and the zero-operator/identity-semigroup consistency witness elaborated under `--trust=0 -t0`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is incomplete. |

Exact narrow Lean replay:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-slot47.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && env -u LEAN_PATH lake env which lean)
lean_path=$(cd "$lean_root" && env -u LEAN_PATH lake env printenv LEAN_PATH)
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
