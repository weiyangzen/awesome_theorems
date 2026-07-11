# Anchor-audit validation record

Item: `S56-M-0086-ANCHOR_AUDIT`  
Base revision: `94e3ff8d01686341332e0fbae530f51b5cdb5a6f`

## Result

The pinned mathlib snapshot contains exact terminal declarations for all three branches of the
frozen target. `CategoryTheory.Abelian.freyd_mitchell` exactly matches the embedding branch, while
`has_injective_coseparator` and `has_projective_separator` exactly match the two generator branches.
`AnchorAudit.lean` checks their types and composes them to the fully unfolded canonical target. The
four observed axiom reports are `propext`, `Classical.choice`, and `Quot.sound`; no custom axiom,
placeholder, unsafe declaration, or oracle boundary was found in the inspected terminal sources.

The candidates are immutable and already dependency-legal: the clean installed mathlib checkout,
Lake manifest, and audit ledger agree on commit `8a178386ffc0f5fef0b77738bb5449d50efeea95`
and tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b`. The source files and legacy wrapper are
content-hashed in `anchor-audit.json`. No `.lake` artifact was changed.

Bounded external discovery found no distinct Lean 4 implementation. Sourcegraph returned nine
matches, all in mathlib4 at indexed commit `12b4b4adf73c3bf0917409bb4b9dd4c8b96f4e8f`; two GitHub
repository searches returned complete zero-result responses. These dated, hashed searches are not
a claim of global absence.

The root is classified `M1`, not `M0`: the exact pinned family and adapter feasibility are checked,
but the proof phase must install the canonical `CanonicalStatement` wrapper after freezing the
obligation registry. Full dependency/body provenance, trust closure, hermetic replay, and accepted
receipts also remain open.

## Commands and results

All commands ran in this worker clone on 2026-07-12. Lean used only the existing pinned Lake
environment; no update, build, fetch, or clone command was run.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0086/AnchorAudit.lean` | 0 | three exact candidates and their composition elaborated; four axiom reports printed |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0086/Statement.lean` | 0 | frozen canonical target, checked transport, and four expected mutation failures re-elaborated |
| `python3 Stage1_Instances/THM-M-0086/check_anchor_audit.py` | 0 | manifest/checkout pins, clean tree, source hashes, declaration needles, and M1 boundary agreed |
| `rg -n 'freyd_mitchell\|has_injective_coseparator\|has_projective_separator' Formalizations/Lean/.lake/packages/mathlib/Mathlib -g '*.lean'` | 0 | exact terminal definitions and downstream uses inventoried in pinned source |
| Sourcegraph public code query serialized in `anchor-audit.json` | 0 | 9 matches, all mathlib4; response SHA-256 `a047eaa6...f57818` |
| two GitHub repository API queries serialized in `anchor-audit.json` | 0 | both complete with `total_count=0`; response SHA-256 `08c082fd...2600b2` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets in ranks 1 through 1546 passed |
| `python3 scripts/stage1_target.py show THM-M-0086` | 0 | rank 134, planned, rework required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0086 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Status boundary

This is a self-tested anchor-audit node pending master acceptance. It neither updates the generated
checklist nor claims full audit or theorem completion. The next gate is the frozen obligation tree;
the proof-phase wrapper and validation/release evidence remain mandatory.
