# THM-M-1041 proof-phase recheck at current base

Item: `S56-M-1041-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T06:52:13+08:00` (`Asia/Shanghai`)

Base revision: `3d3099d0d4002093cf89da97132bdf954605810b`

Base tree: `17ea0daeddceb9742a5df33c247d624d2842c520`

## Verdict

`blocked`. The exact frozen root is the full real contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof body for that equivalence is present
in this repository or its pinned Lake dependency closure. Neither
`ForwardPackage` nor `ConversePackage` is inhabited, so the minimal root cut
remains:

```text
M1041-F-ASSEMBLE
M1041-C-ASSEMBLE
```

The first missing forward leaf is `M1041-F-CLOSED`; independently, the first
missing converse construction is `M1041-C-YOSIDA-APPROX`.
`root_of_directionPackages` is only a checked composition after a caller
supplies both complete directions. It proves neither direction.
`target_iff_expanded` is only a definitional statement transport.

The duplicate target `THM-M-0330`, legacy module `S1_M_234`, and repository
history contain the same statement architecture or abstract interfaces, not a
terminal proof. Pinned mathlib supplies functional-analysis substrate but has
no Hille--Yosida theorem or strongly continuous semigroup generator API.

The audited commit-pinned external candidates are unchanged. The main branch of
`mrdouglasny/hille-yosida` is still
`680e9499ee866763e737c8d888c1248684ced667`; it supplies only prospective
forward resolvent pieces. Its former generation and density axioms are
commented out, and no converse theorem body exists. TauCeti remains at
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`; it is partial and uses
incompatible pins. Both projects are outside the pinned Lake closure. They
were not cloned, fetched, built, integrated, or credited.

Closing the exact root requires new formal analysis: generator closedness and
density; construction of the Laplace/Bochner resolvent with both inverse laws
and its norm estimate; and the Yosida approximation, limiting semigroup,
semigroup laws, strong continuity, contraction, and exact generator
identification. Assuming either package, weakening the equivalence, or moving
these facts into abstract fields would add an unproved premise or substitute a
different theorem.

The item stays `[ ]`; lifecycle stays `planned`; the root vector stays
`[H2, M4, R4]`; and accepted receipt IDs stay empty. This artifact is blocker
evidence, not a proof receipt or state request. Because the proof phase is not
self-tested as complete, `.stage1-worker-selftest.json` is deliberately
absent.

## Validation

All commands ran in this worker clone. Initial `git status --short` showed only
the automation-provided `Formalizations/Lean/.lake` symlink to the canonical
pinned cache. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation ran. Direct Lean output was written under `/tmp` and removed;
the statement checker also removed its temporary mutation sources on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1041` | 0 | Rank 234; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-1041/check_statement.py` | 0 | Exact expression SHA-256 `e6e5f0cbc4d61e4b3ac869fe7b01d4e0d28e3c558c1dea897c29871891f7768d`; all three structural mutations killed. |
| `python3 Stage1_Instances/THM-M-1041/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-1041/check_obligation_tree.py` | 0 | 21 obligations and 56 typed edges passed; denominator `b9ebe90e50ff8cf0a0979d0e155ad58c2918a48cc3236e22f76fac67a6b39c42`; root and both directions remain `M4`. |
| Isolated `lake env` discovery plus `lean --trust=0 -t0` recipe below | 0 | `Statement.lean` and conditional `ObligationTree.lean` elaborated; `root_of_directionPackages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-mathlib topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match: no `sorry`, `admit`, `sorryAx`, unsafe/oracle shortcut, `axiom`, or `opaque` declaration in owned Lean sources. |
| `git ls-remote` for each audited external main branch | 0 | Candidate commits remain `680e9499...d667` and `c7e69c3c...94fa`; neither is in the pinned closure. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |
| `python3 -m json.tool Stage1_Instances/THM-M-1041/proof-recheck-2026-07-15-head-3d3099d0.json` | 0 | The paired structured blocker artifact is valid JSON. |
| `git diff --no-index --check /dev/null <new-artifact>` for each evidence file | 1 | Expected added-file diff status with no whitespace diagnostics for either artifact. |

Exact narrow Lean replay, run from the repository root:

```bash
set -euo pipefail
repo=$PWD
lean_root=$repo/Formalizations/Lean
target=$repo/Stage1_Instances/THM-M-1041
tmp=$(mktemp -d /tmp/thm-m-1041-proof-head-3d3099d0.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
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

The JSON syntax check does not assert a separately published schema validator;
the structured blocker record is fail-closed evidence only.

Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; Lake
`5.0.0-src+98dc76e`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`.

## Retry Condition

Resume after placeholder-free implementations of all children needed for both
frozen direction packages are in the pinned closure, or after an immutable
compatible exact Lean 4 proof is pinned/imported and passes exact-type,
provenance, placeholder, axiom, composition, and trust checks.
