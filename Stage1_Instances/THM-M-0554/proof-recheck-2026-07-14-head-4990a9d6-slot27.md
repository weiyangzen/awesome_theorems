# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-14T03:37:37+08:00`

Base revision: `4990a9d6fa09beb7747e6822c6543c6123ca7504`

Base tree: `b74497bc09c004757aa3974f3bb0622d77e20106`

## Verdict

`blocked`. No genuine Atiyah-Hirzebruch spectral-sequence proof body was
implemented or found in the pinned dependency closure. The exact root remains
`M4`; this attempt adds no proof receipt, composition certificate, debt-vector
change, or state transition.

The immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies generic spectral-sequence, CW-complex, and singular-
homology substrate, but no terminal declaration for a root-cut package. A
current-head search of every pinned package returned no match for the AHSS,
generalized-cohomology, exact-couple, or strong-convergence query family.
Mathlib's spectral-object source still documents its intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructors as `TODO`.

## First Failed Gate

The exact-statement-fidelity gate fails before a proof can be credited. In
`Statement.lean`, `pointIsPoint`, `exactnessAxiom`,
`wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`, and
`cellAttachments` are proposition-valued data rather than required proofs.
The output selects the meanings of `coefficientConvention`,
`strongConvergence`, and `naturalityInSpace`, while
`filtrationIsInducedBy` is only `K.skeleton = K.skeleton`.

Consequently the literal proposition admits a zero spectral-sequence witness
using zero objects, reflexive isomorphisms, and output-selected `True`
propositions. A fresh disposable trust-level-zero probe elaborated that term
and reported only `propext`, `Classical.choice`, and `Quot.sound`. Its source
SHA-256 was `4bf0ca67...a0f4b`; it was removed and is not credited because it
constructs no AHSS and consumes none of the frozen semantic children.
Accepting it would violate the exact-statement-fidelity, no-fake-result, and
checked child-to-parent composition gates.

Predecessor authority is also unresolved. The global obligation-tree item is
only provisional (`[_]`), while `instance.json` still has a null canonical
formal module, expression, expression hash, and environment fingerprint with
status `open_statement_phase`. Its intake `task-dag.json` is `frozen=false`,
leaves `STMT`, `SOURCE`, and `TREE` open, and marks `PROOF` as
`blocked_by_predecessors`. A proof-only worker cannot silently reconcile or
replace those authorities.

## Validation

All Lean commands reused the automation-provided symlink to the canonical
pinned `.lake` artifacts. No update, build, dependency clone/fetch, network
action, or `.lake` mutation was performed. Generated Lean output stayed in a
temporary directory and was removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains M4 without a composition certificate. |
| Isolated pinned `lake env lean` trust-level-zero recipe below | 0 | `Statement.lean` elaborated with Lean 4.29.0; temporary `Statement.olean` was 429072 bytes and was removed. |
| Trust-level-zero disposable literal-witness probe | 0 | Source SHA-256 `4bf0ca67...a0f4b`; the probe elaborated and reported axioms `[propext, Classical.choice, Quot.sound]`, confirming the statement defect. It was removed and is not proof evidence. |
| `rg -n -i --glob '*.lean' 'Atiyah[-_ ]?Hirzebruch|AtiyahHirzebruch|\\bAHSS\\b|generalized[ _-]*(co)?homology|exact[ _-]*couple|strong[ _-]*convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned proof candidate was found. |
| The same query over repo-local Lean sources outside this dossier | 0 | Hits were the legacy `S1_M_106.lean` interfaces and audit gates plus unrelated plans, not a terminal AHSS proof body. |
| `rg -n --pcre2 '^\\s*(?:sorry|admit|axiom)(?:\\s|$)|\\bsorryAx\\b|^\\s*unsafe(?:\\s|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: no prohibited declaration token occurs in the owned Lean sources. |
| Pinned toolchain, mathlib revision/tree, and manifest checks | 0 | Lean 4.29.0 commit `98dc76e...16740`; mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`; manifest SHA-256 `321626c8...2d81`. |
| Spectral-object source hash and `TODO` scan | 0 | SHA-256 `2ce62b9d...740aa`; the intended constructors remain documented `TODO`. |
| `python3 -m json.tool Stage1_Instances/THM-M-0554/proof-recheck-2026-07-14-head-4990a9d6-slot27.json` | 0 | The structured blocker record parses. |
| `git diff --check -- Stage1_Instances/THM-M-0554 .stage1-worker-selftest.json` | 0 | No whitespace errors. |
| `git diff --no-index --check /dev/null <new-artifact>` for each new artifact | 1 | Expected content-difference status, with no whitespace diagnostics. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No self-test manifest was written for this blocked phase. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0554
tmp=$(mktemp -d /tmp/thm-m-0554-slot27.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
```

## Retry Condition

First publish and master-accept a source-faithful corrected statement,
reconcile the instance and task authority, and issue obligation-registry
version 2. Then implement and compose the four root-cut packages without
placeholders. An alternative is an immutable exact compatible Lean 4 AHSS
proof that can be pinned, exact-type transported, and checked with complete
provenance, trust, and composition closure.

This artifact is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close an obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
