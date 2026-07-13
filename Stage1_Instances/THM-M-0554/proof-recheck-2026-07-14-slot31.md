# THM-M-0554 proof-phase recheck: blocked

Item: `S56-M-0554-PROOF`

Attempt: `2026-07-14T01:33:20+08:00`

Base revision: `3bb4cb3ae15dff8b48c93242019edec3bf858e48`

Base tree: `8e911f5a101bd92eb0951794fa0d9a3c0c3a2ddc`

## Verdict

`blocked`. No genuine Atiyah-Hirzebruch spectral-sequence proof body was
implemented or found in the pinned dependency closure. The exact root remains
`M4`; this attempt adds no proof receipt and proposes no state change.

The frozen immediate root cut is unchanged:

- `M0554-X-GENCOH`: generalized-cohomology pair, excision, and wedge infrastructure;
- `M0554-C-EXACT-COUPLE`: the skeletal-filtration exact-couple construction;
- `M0554-C-E2-MODEL`: the cellular-cohomology `E2` identification;
- `M0554-L-STRONG`: strong convergence for the finite skeletal filtration.

Pinned mathlib provides the generic
`CategoryTheory.E2CohomologicalSpectralSequence` container and adjacent CW and
singular-homology infrastructure, but no terminal declaration for any of these
four packages. A fresh bounded search of the pinned sources returned no match
for the AHSS, generalized-cohomology, exact-couple, or strong-convergence query
family. The repo-local legacy file contains interfaces, audit gates, and
statement shapes only; it explicitly records that no terminal AHSS proof is
integrated.

## Rejected Literal Inhabitant

The frozen Lean proposition can be inhabited without proving the intended
theorem. A disposable `/tmp/M0554Explore.lean` probe used
`HomologicalComplex.zero` for every page, zero objects for the filtration and
stable page, reflexive isomorphisms, and output-selected `True` propositions.
It ignored the proposition-valued input fields
`pointIsPoint`, `exactnessAxiom`, `wedgeAxiomOrRepresentability`, `finiteCW`,
`exhaustive`, and `cellAttachments`. The probe elaborated at trust level zero;
`#print axioms` reported only `propext`, `Classical.choice`, and `Quot.sound`.

That term is deliberately not retained or credited. It constructs no AHSS and
does not consume any of the frozen semantic children. Accepting it would
violate the exact-statement-fidelity, child-to-parent composition, and
no-fake-result gates. In particular, successful kernel elaboration of the
literal proposition does not cure its mismatch with the canonical mathematical
claim and frozen registry.

## Validation

All commands used the existing pinned `.lake` symlink. No update, build,
dependency clone/fetch, network action, or `.lake` mutation was performed.
Generated Lean objects stayed in temporary directories and were removed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-0554` | 0 | Rank 106; lifecycle `planned`; baseline `L0/rework_required`; theorem incomplete. |
| `python3 Stage1_Instances/THM-M-0554/check_obligation_tree.py` | 0 | 32 obligations and 91 typed edges passed; denominator `3c72072a...8048b`; root remains open at M4 with no composition certificate. |
| Isolated pinned Lean recipe below | 0 | `Statement.lean` elaborated at trust level zero, then the disposable literal probe elaborated; its axiom report was `[propext, Classical.choice, Quot.sound]`. |
| `rg -n -i 'Atiyah[- ]?Hirzebruch|AtiyahHirzebruch|\bAHSS\b|generalized (co)?homology|exact couple|strong convergence' .lake/packages/mathlib/Mathlib --glob '*.lean'` from `Formalizations/Lean` | 1 | Expected no-match result: no terminal pinned mathlib candidate was found for this query family. |
| `rg -n -i 'Atiyah[- ]?Hirzebruch|AtiyahHirzebruch|\bAHSS\b|generalized (co)?homology|exact couple|strong convergence' AwesomeTheorems ../../Stage1_Instances --glob '*.lean' --glob '!THM-M-0554/**'` from `Formalizations/Lean` | 0 | Hits were the legacy `S1_M_106.lean` statement/audit surface and the frozen dossier, not a terminal proof body. |
| `rg -n --pcre2 '^\s*(?:sorry|admit|axiom)(?:\s|$)|\bsorryAx\b|^\s*unsafe(?:\s|$)' Stage1_Instances/THM-M-0554 --glob '*.lean'` | 1 | Expected no-match result: the owned Lean sources contain no prohibited declaration token. |
| `lake env lean --version` from `Formalizations/Lean` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release. |
| `git -C .lake/packages/mathlib rev-parse HEAD` from `Formalizations/Lean` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`. |
| `test ! -e .stage1-worker-selftest.json` | 0 | No completion self-test manifest exists. |

The isolated Lean recipe was:

```bash
set -euo pipefail
repo_root=$PWD
lean_root=$repo_root/Formalizations/Lean
target=$repo_root/Stage1_Instances/THM-M-0554
tmp=$(mktemp -d /tmp/thm-m-0554-slot31-probe.XXXXXX)
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
