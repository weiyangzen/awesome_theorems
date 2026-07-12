# Intake validation record

Base revision: `8ac609b6e17629674e5bb3f43384178e23cf0da8`.

Commands were run from the worker clone on 2026-07-12. The pre-existing untracked
`Formalizations/Lean/.lake` link/artifact was not modified. No dependency update, fetch, clone, or
build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1..1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0573` | 0 | rank 619, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`; environment availability only, not theorem elaboration |
| Crossref lookups for DOI `10.2307/1970716` and `10.2307/1970717` | 0 | returned the recorded titles, authors, journal, volume/issue, May 1968 date, and starting pages 531 and 546 |
| `rg -ni 'equivariant.*index\|index.*equivariant\|Atiyah.*Segal\|GIndex\|gIndex' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | only an unrelated explanatory use of "equivariant" was returned; this is a scoped discovery search, not a complete anchor audit |

This node introduces no Lean declaration because an exact mathematical proposition has not been
selected. Accordingly, no kernel theorem, expression hash, axiom result, or proof closure is
claimed. JSON syntax, scoped dossier invariants, forbidden-proof-escape search, and whitespace are
validated in the final self-test recorded by the worker manifest.

Known downstream failures: exact source theorem/page and errata inspection, attribution review,
canonical statement selection, Lean elaboration and mutation tests, anchor audit, obligation
registry, proof, hermetic replay, and independent review remain open. They prevent downstream and
theorem-completion claims but do not invalidate this fail-closed planned intake.
