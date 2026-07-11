# Statement-phase blocker

Item: `S56-M-0555-STATEMENT`  
Base revision: `fc26d2ed7eff8e887bc324aa491c32151b48cd7a`

## Verdict

The exact Lean 4 target cannot truthfully be frozen from the currently accepted intake material.
The repository metadata supplies only the phrase "homology spectral sequence of a fibration". The
intake explicitly leaves unresolved the fibration model, coefficient/local-system data,
connectivity and monodromy hypotheses, indexing convention, convergence claim, and abutment
filtration. These are semantic parts of the theorem rather than encoding details. Selecting them
without a primary-source theorem/page and assumption crosswalk would broaden or substitute the
claim, contrary to the rev-5.6 exact-statement gate.

Accordingly, this phase is blocked at the source-statement freeze. No canonical declaration,
expression fingerprint, mutation suite, or minimal-import claim is emitted, and no statement node
completion is claimed. Retry requires a stable primary-source edition plus the exact numbered
result/page range and a resolved crosswalk for all choices listed in `scope-map.md`.

## Legacy candidate check

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_111.lean` is discovery input only. It defines
`StatementShape` using opaque proposition fields for being a Serre fibration, identifying the
fiber, the E2-page assertion, naturality, convergence, and abutment. Consequently it assumes the
mathematical content that the target is meant to state and cannot establish exact statement
identity. Its six direct imports are therefore not accepted as the target's minimal pinned import
set. The file does elaborate in the existing pinned environment, which confirms only that the
legacy interface is syntactically and type-correct.

The existing `.lake` path is a symlink to the canonical pinned artifacts. It was used read-only;
no dependency update, build, clone, or fetch was run.

## Commands and results

Commands ran in this worker clone. Lean commands ran from `Formalizations/Lean`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`; 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`; 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0555` | 0 | rank 111; planned; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `lake env lean AwesomeTheorems/Stage1/S1_M_111.lean` | 0 | legacy opaque-interface candidate elaborated with no output |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum lean-toolchain lake-manifest.json AwesomeTheorems/Stage1/S1_M_111.lean` | 0 | `651c8a...1d2`, `321626...2d81`, `4b4d51...95fb` |
| `rg -n 'SerreFibration\|Serre.*spectral\|serre.*spectral\|isSerreFibration' .lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | one prose mention of Hochschild-Serre; no matching topological Serre-fibration declaration found |

This blocker is statement-only evidence. It does not advance anchor audit, proof, validation,
release, audit completion, or theorem completion. Because the assigned statement phase did not
pass, no `.stage1-worker-selftest.json` is created.
