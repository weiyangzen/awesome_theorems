# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-14T02:29:00+08:00`

Base revision: `ffea62ba1a7c0b0f84d70fd07f87d3eef57fe330`

Base tree: `4662e08d189bd534919775f750c6909591aeafcb`

## Verdict

`blocked`. No genuine Atiyah-Hirzebruch spectral-sequence proof body was
implemented or found in the pinned dependency closure. The exact root remains
`M4`; this attempt adds no proof receipt, composition certificate, or state
transition.

The frozen immediate root cut remains:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib supplies the generic
`CategoryTheory.E2CohomologicalSpectralSequence` container and adjacent CW and
singular-homology infrastructure, but no terminal declaration for any root-cut
package. A fresh search of every pinned package returned no match for the
AHSS, generalized-cohomology, exact-couple, or strong-convergence query family.
The repo-local legacy file contains interfaces and audit gates only. Mathlib's
spectral-object file also marks its intended `spectralSequence`, `homologyData`,
and `spectralSequenceHomologyData` constructions as `TODO`; its SHA-256 is
`2ce62b9d0a9576bf0e14fc554bb4dd73636ebf30f406f2fe54d8bdcc16b740aa`.

## Exact-Statement Blocker

The literal frozen proposition is under-specified relative to the canonical
mathematical claim. The input fields `pointIsPoint`, `exactnessAxiom`,
`wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`, and
`cellAttachments` are proposition-valued data, not required proofs. The output
can select the meanings of `coefficientConvention`, `strongConvergence`, and
`naturalityInSpace`, while `filtrationIsInducedBy` is only the reflexive
equality `K.skeleton = K.skeleton`.

Consequently, the literal proposition admits a zero spectral-sequence witness
with zero objects, reflexive isomorphisms, and output-selected `True`
propositions. A disposable trust-level-zero probe elaborated that term and
reported only `propext`, `Classical.choice`, and `Quot.sound`. The term was not
retained or credited: it constructs no AHSS and consumes none of the frozen
semantic children. Accepting it would violate the exact-statement-fidelity,
child-to-parent composition, and no-fake-result gates.

There is also an unresolved predecessor-authority mismatch. `instance.json`
still records a null canonical module, declaration/expression, expression
hash, and environment fingerprint with status `open_statement_phase`, while
`statement.json` separately records provisional elaboration. A proof-only
worker cannot silently repair or override that authoritative intake surface.

## Validation

All commands used the existing pinned `.lake` symlink. No update, build,
dependency clone/fetch, network action, or `.lake` mutation was performed.
Generated Lean objects stayed in temporary directories and were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains M4 with no composition certificate. |
| Isolated pinned Lean recipe below | 0 | `Statement.lean` and the disposable literal probe elaborated at trust level zero; the probe's axiom report was `[propext, Classical.choice, Quot.sound]`. |
| `rg -n -i --glob '*.lean' 'Atiyah[-_ ]?Hirzebruch|AtiyahHirzebruch|\bAHSS\b|generalized[ _-]*(co)?homology|exact[ _-]*couple|strong[ _-]*convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no pinned proof candidate was found. |
| The same query over repo-local Lean sources outside this dossier | 0 | Hits were legacy statement/audit surfaces and unrelated proof plans, not a terminal AHSS proof body. |
| Prohibited-token scan over owned `*.lean` sources | 1 | Expected no-match result: no `sorry`, `admit`, `axiom`, `sorryAx`, or `unsafe` declaration token. |
| Pinned revision and manifest checks | 0 | mathlib `8a178386...ea95`, tree `bdc39a31...1c2b`, manifest SHA-256 `321626c8...2d81`. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0554
tmp=$(mktemp -d /tmp/thm-m-0554-current.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
LEAN_NUM_THREADS=1 LEAN_PATH="$tmp:$lean_path" timeout 300 "$lean" --trust=0 \
  /tmp/M0554Explore.lean
```

The rejected probe source SHA-256 was
`4bf0ca6751da1058cdd8c057d5db51f1c0672538f9b9648b1ef515201bfa0f4b`.

## Reopen Condition

First publish and master-accept a source-faithful statement, reconcile the
instance authority, and issue obligation-registry version 2. Then implement
and compose the four root-cut packages without placeholders. An alternative
is an immutable exact compatible Lean 4 AHSS proof that can be pinned,
exact-type transported, and checked with complete provenance and trust closure.

This report is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close any obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
