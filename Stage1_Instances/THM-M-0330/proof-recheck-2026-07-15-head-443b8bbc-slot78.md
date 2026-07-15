# THM-M-0330 proof-phase recheck at current base

Item: `S56-M-0330-PROOF`

Intent: `prove`

Recorded at: `2026-07-15T11:40:20+08:00` (`Asia/Shanghai`)

Base revision: `443b8bbc23bf35a1e7a4bb7b3183073f76bbee2b`

Base tree: `c5771c47c12b80aba613e6d844570f83b39ded6d`

## Verdict

`blocked`. The frozen target is the complete contraction Hille--Yosida
equivalence for every partially defined real-linear operator on every real
Banach space. No placeholder-free proof of this exact target is present in
the repository or pinned dependency closure. Neither `ForwardPackage` nor
`ConversePackage` is inhabited, so the minimal open root cut remains:

```text
M0330-B-FORWARD
M0330-B-CONVERSE
```

The first unavailable forward leaf is `M0330-L-FWD-DENSE`; independently, the
first unavailable converse construction is `M0330-C-YOSIDA`.
`root_of_direction_packages` kernel-checks only the final composition after a
caller supplies both complete directions. It constructs neither direction
and is not a premise-free proof. `target_iff_expanded` is only a definitional
transport.

The proof-relevant owned sources are unchanged. All five commits in target
history, duplicate target `THM-M-1041`, and legacy module `S1_M_234` contain
definitions, abstract interfaces, transports, or conditional composition,
not a substantive direction package. A source search over every package in
the pinned cache found no Hille--Yosida theorem or strongly continuous
semigroup generator API.

The audited external candidate `mrdouglasny/hille-yosida` remains at
`680e9499ee866763e737c8d888c1248684ced667`. Its prospective forward work does
not supply generator density or closedness, the left inverse over the entire
domain, or the converse. Its real-time bundled semigroup and generated-domain
API would also require substantive transports to the frozen `NNReal` and
`LinearPMap` definitions. TauCeti main is
`c7e69c3c3e65039f6f25fc20a04ce52bb58d94fa`; it likewise does not supply the
exact two packages and uses incompatible pins. Both remain outside the pinned
Lake closure. This run queried only remote branch metadata; neither project
was cloned, fetched, built, integrated, or credited.

Closing the root requires new formal proofs of generator density and
closedness, a Laplace/Bochner resolvent with both inverse laws and its
contraction estimate, and the Yosida-approximation semigroup construction with
exact generator identification. Alternatively, an immutable compatible exact
proof must enter the pinned closure and pass exact-type, provenance,
placeholder, axiom, composition, and trust checks. Assuming either direction
package, weakening the equivalence, or replacing the analytic facts with
abstract fields would prove a different theorem and is prohibited.

The item remains `[ ]`; lifecycle remains `planned`; the frozen graph's root
vector remains `[H3, M4, R4]`; and accepted receipt IDs remain empty. The older
intake projection still says `[H1, M4, R4]`; this proof worker does not rewrite
that separate projection. This pair is blocker evidence, not a proof receipt
or item-state request. Because the proof phase is incomplete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All commands ran in this worker clone. Initial status showed only the
automation-provided `Formalizations/Lean/.lake` symlink before this evidence
pair was added. No `lake update`, `lake build`, dependency clone/fetch, or
`.lake` mutation ran. Lean object output was isolated under `/tmp` and removed
on exit.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0330` | 0 | Rank 823; lifecycle `planned`; `theorem_complete=false`. |
| `python3 Stage1_Instances/THM-M-0330/check_statement.py` | 1 | Root Lake environment could not resolve `HEAD` in `.lake/packages/flt-regular`; no fetch, repair, or other `.lake` mutation was attempted. |
| `python3 Stage1_Instances/THM-M-0330/check_anchor_audit.py` | 0 | `anchor audit invariant check: ok` |
| `python3 Stage1_Instances/THM-M-0330/check_obligation_tree.py` | 0 | 19 obligations and 40 typed edges passed; denominator `f173d7dfb3e01916776f2e78183615c1d439b1041e1918c14a1dd719032ea29a`; root and both direction packages remain `M4`. |
| Isolated trust-level-zero `lake env lean` recipe below | 0 | The unchanged exact statement and conditional composition elaborated; `root_of_direction_packages` reports `[propext, Classical.choice, Quot.sound]`. |
| Pinned-package topical search below | 1 | Expected no-match: no terminal Hille--Yosida or semigroup-generator declaration. |
| Scoped prohibited-token scan below | 1 | Expected no-match in owned Lean sources. This lexical scan is supporting evidence only and makes no parser-aware or transitive provenance claim. |
| `git ls-remote` for the two external main branches | 0 | Candidate revisions are `680e9499...d667` and `c7e69c3c...94fa`; neither is in the pinned closure. |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent. |

The standard statement mutation checker failed before invoking Lean because
the automation-provided shared `flt-regular` checkout has no resolvable
`HEAD`. Worker rules prohibit fetching or repairing that cache. The smallest
nonmutating fallback therefore used the pinned Lean executable and existing
root-package objects while still invoking it through `lake env`:

```bash
set -euo pipefail
repo=$PWD
mathlib_root=$repo/Formalizations/Lean/.lake/packages/mathlib
target=$repo/Stage1_Instances/THM-M-0330
tmp=$(mktemp -d /tmp/thm-m-0330-proof-lake-env-head-443b8bbc-slot78.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lp=$(printf '%s:' \
  "$repo/Formalizations/Lean/.lake/packages/Cli/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/batteries/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/Qq/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/aesop/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/proofwidgets/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/importGraph/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/LeanSearchClient/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/plausible/.lake/build/lib/lean" \
  "$repo/Formalizations/Lean/.lake/packages/mathlib/.lake/build/lib/lean" \
  "$HOME/.elan/toolchains/leanprover--lean4---v4.29.0/lib/lean")
cd "$mathlib_root"
LEAN_NUM_THREADS=1 LEAN_PATH="$lp" \
  timeout --foreground 600 lake env lean --trust=0 -t0 --root="$target" \
    -o "$tmp/Statement.olean" "$target/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lp" \
  timeout --foreground 600 lake env lean --trust=0 -t0 --root="$target" \
    "$target/ObligationTree.lean"
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
  Stage1_Instances/THM-M-0330 --glob '*.lean'
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
The pinned `flt-regular` artifact must also be restored before the standard
statement mutation checker can replay.
