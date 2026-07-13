# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-14T02:10:30+08:00`

Base revision: `823dfcd5e231e84436ac3d88948d8e669c168fdb`

Base tree: `a87f5f99350f49ddeb9d7df23dc6e0fe6fe3011f`

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

Pinned mathlib provides the generic
`CategoryTheory.E2CohomologicalSpectralSequence` container and adjacent CW and
singular-homology infrastructure, but no terminal declaration for any of these
four packages. A fresh search of every pinned package returned no match for the
AHSS, generalized-cohomology, exact-couple, or strong-convergence query family.
The repo-local legacy file contains interfaces and audit gates only. In
addition, mathlib's spectral-object file explicitly labels its intended
`spectralSequence`, `homologyData`, and `spectralSequenceHomologyData`
constructions as `TODO`; it does not supply the missing AHSS composition.
That pinned source has SHA-256
`2ce62b9d0a9576bf0e14fc554bb4dd73636ebf30f406f2fe54d8bdcc16b740aa`.

## Exact-Statement Blocker

The literal frozen proposition is under-specified relative to the canonical
mathematical claim. The input fields `pointIsPoint`, `exactnessAxiom`,
`wedgeAxiomOrRepresentability`, `finiteCW`, `exhaustive`, and
`cellAttachments` are proposition-valued data, not required proofs. The output
can select the meanings of `coefficientConvention`, `strongConvergence`, and
`naturalityInSpace`, while `filtrationIsInducedBy` is only the reflexive
equality `K.skeleton = K.skeleton`.

Consequently the literal proposition admits a zero spectral-sequence witness
with zero objects, reflexive isomorphisms, and output-selected `True`
propositions. A prior trust-level-zero scratch probe elaborated that term and
reported only `propext`, `Classical.choice`, and `Quot.sound`. The term remains
deliberately unretained: it constructs no AHSS and consumes none of the frozen
semantic children. Crediting it would violate the exact-statement-fidelity,
child-to-parent composition, and no-fake-result gates.

## Validation

All Lean commands reused the existing pinned `.lake` symlink. No update, build,
dependency clone/fetch, network action, or `.lake` mutation was performed.
Generated Lean output was confined to a temporary directory and removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at M4 with no composition certificate. |
| Isolated pinned Lean recipe below | 0 | `Statement.lean` elaborated at trust level zero and produced a nonempty temporary object; no proof declaration was introduced. |
| `rg -n -i --glob '*.lean' 'Atiyah[- ]?Hirzebruch\|AtiyahHirzebruch\|\bAHSS\b\|generalized (co)?homology\|exact couple\|strong convergence' Formalizations/Lean/.lake/packages` | 1 | Expected no-match result: no terminal candidate was found in any pinned package. |
| The same bounded query over repo-local Lean sources outside this dossier | 0 | Hits were the legacy `S1_M_106.lean` statement/audit surface and an unrelated Adams exact-couple plan, not a terminal AHSS body. |
| `rg -n --pcre2 '^\s*(?:sorry\|admit\|axiom)(?:\s\|$)\|\bsorryAx\b\|^\s*unsafe(?:\s\|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: the owned Lean sources contain no prohibited declaration token. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD^{tree}` | 0 | `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. |
| `sha256sum Formalizations/Lean/lake-manifest.json` | 0 | `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0554
tmp=$(mktemp -d /tmp/thm-m-0554-slot33-statement.XXXXXX)
trap 'rm -rf "$tmp"' EXIT
lean=$(cd "$lean_root" && lake env which lean)
lean_path=$(cd "$lean_root" && lake env printenv LEAN_PATH)
cd "$target"
LEAN_NUM_THREADS=1 LEAN_PATH="$lean_path" timeout 300 "$lean" --trust=0 \
  -R "$target" -o "$tmp/Statement.olean" Statement.lean
test -s "$tmp/Statement.olean"
```

## Reopen Condition

First publish and accept a source-faithful statement and obligation-registry
version 2 which turns the theory/CW facts into inhabited hypotheses and ties
the `E2`, filtration, naturality, and convergence conclusions to the constructed
spectral sequence. Then implement and compose the four root-cut packages
without placeholders. An alternative is an immutable exact compatible Lean 4
AHSS proof that can be pinned, exact-type transported, and checked with complete
provenance and trust closure.

This report is durable blocker evidence only. It does not satisfy
`S56-M-0554-PROOF`, close any obligation, complete the audit or theorem, or
authorize master acceptance. Because the assigned phase is not genuinely
self-tested as complete, `.stage1-worker-selftest.json` remains absent.
