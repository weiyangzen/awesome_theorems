# THM-M-1285 proof-phase recheck at current base

Item: `S56-M-1285-PROOF`

Intent: `prove`

Date: `2026-07-14` (`Asia/Shanghai`)

Base revision: `a86029b30f12acc3537f70ab1c167cc25702c09b`

Base tree: `ab12055e811b574338987391b59b010338c120d2`

## Verdict

`blocked`. This current-base replay confirms that neither the owned source nor pinned mathlib
inhabits `Stage1Instances.THM_M_1285.SchwarzConstructionPackage`. The exact root therefore remains
open at `M3`, with the frozen minimal open root cut `M1285-T-PACKAGE` at `M4`.

`Proof.lean` has genuine, placeholder-free bodies for three profile helpers. They show that a
norm-profile is radial, that an antitone profile is radially nonincreasing, and that a measurable
profile gives a measurable norm composition. `ObligationTree.lean` also has a checked conditional
composition into the exact root. None of these bodies constructs the required profile, and the
composition theorem takes the entire construction package as an unproved premise.

The missing proof is substantive: define the finite positive strict-superlevel distribution,
develop its generalized inverse, realize its values by centered Euclidean-ball radii, construct a
measurable radial witness, and prove exact equality of every positive strict-superlevel volume.
Pinned mathlib supplies supporting measure, monotonicity, inverse-power, and ball-volume APIs but no
terminal Schwarz-rearrangement declaration. No weaker theorem or conditional wrapper was
substituted.

The item remains `[ ]`. Because the assigned proof phase is not self-tested as complete,
`.stage1-worker-selftest.json` is deliberately absent.

## Validation

All checks ran in this worker clone using the automation-provided read-only `.lake` symlink. No
`lake update`, `lake build`, dependency clone/fetch, network access, or `.lake` mutation occurred.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1285` | 0 | Rank 456; planned hard-mathlib lane; legacy artifacts unaccepted; theorem incomplete |
| `python3 Stage1_Instances/THM-M-1285/check_obligation_tree.py` | 0 | 16 obligations and 83 typed edges passed; denominator `6e441bf...32e9c`; root open `M3`, construction package `M4` |
| Temporary-olean Lean recipe below | 0 | `Statement.lean`, conditional composition, and all three profile helpers elaborated against pinned artifacts |
| `rg -n --pcre2 '\\b(?:sorry|admit|axiom)\\b|sorryAx|unsafe|implemented_by|native_decide' Stage1_Instances/THM-M-1285 --glob '*.lean'` | 1, expected | No prohibited construct in owned Lean source |
| `git diff --check -- Stage1_Instances/THM-M-1285` | 0 | No whitespace errors before this packet was added |
| `test ! -e .stage1-worker-selftest.json` | 0 | Completion self-test manifest is absent because the proof phase is blocked |

The narrow Lean replay wrote compiled output only under `/tmp`:

```bash
set -euo pipefail
ROOT=$PWD
TMP=$(mktemp -d /tmp/thm-m-1285-current.XXXXXX)
trap 'rm -rf "$TMP"' EXIT
LEAN_ROOT="$ROOT/Formalizations/Lean"
BASE=$(cd "$LEAN_ROOT" && lake env printenv LEAN_PATH)
LEAN=$(cd "$LEAN_ROOT" && lake env which lean)
cp Stage1_Instances/THM-M-1285/Statement.lean "$TMP/Statement.lean"
cp Stage1_Instances/THM-M-1285/ObligationTree.lean "$TMP/ObligationTree.lean"
cp Stage1_Instances/THM-M-1285/Proof.lean "$TMP/Proof.lean"
cd "$TMP"
LEAN_NUM_THREADS=1 LEAN_PATH="$BASE" timeout 180 "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/Statement.olean" "$TMP/Statement.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout 180 "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/ObligationTree.olean" "$TMP/ObligationTree.lean"
LEAN_NUM_THREADS=1 LEAN_PATH="$TMP:$BASE" timeout 180 "$LEAN" --trust=0 -t0 -R "$TMP" \
  -o "$TMP/Proof.olean" "$TMP/Proof.lean"
```

The conditional composition and three profile-helper `#print axioms` reports were each exactly
`[propext, Classical.choice, Quot.sound]`.
Pinned environment: Lean `4.29.0`, commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`; mathlib
`8a178386ffc0f5fef0b77738bb5449d50efeea95`; `lake-manifest.json` SHA-256
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Retry condition

Implement the frozen distribution/generalized-inverse/centered-ball route through
`M1285-T-PACKAGE`, including measurable witness construction and exact positive strict-superlevel
equimeasurability, or pin an immutable exact Lean 4 terminal body and validate its statement,
license, dependencies, placeholders, axioms, and wrapper.

This is proof-phase blocker evidence, not a proof receipt. It does not satisfy the assigned proof
item or claim audit completion, validation, release, master acceptance, or theorem completion.
