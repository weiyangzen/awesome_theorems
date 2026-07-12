# THM-M-1558 statement-phase blocker

Item: `S56-M-1558-STATEMENT`  
Base revision: `509bacaa61c3669c81276814a33094f8f7280f78`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The repository gives only
the name "Ablowitz-Kaup-Newell-Segur system" and the phrase "a unified framework for integrable
systems". Neither is a proposition: they fix no quantifiers, hypotheses, operator formulas, flow,
reduction, or conclusion. The accepted intake deliberately leaves those choices open.

The candidate 1974 AKNS paper recorded at intake has not been pinned to an independently reviewed
equation, theorem, or page in a fixed edition. In particular, the dossier does not determine the
independent-variable domains, scalar field, matrix size, spectral-parameter domain, spatial and
time operators (including sign conventions), differentiability and boundary assumptions, the
meaning of compatibility, coefficient-comparison conditions, or which member or reduction of the
AKNS hierarchy is intended. Selecting one concrete flow or replacing the phrase by the universal
claim that all integrable systems are AKNS systems would materially narrow or broaden the source
record rather than normalize it.

The only nearby repository Lean module, `AwesomeTheorems/Stage1/S1_M_210.lean`, elaborates in the
pinned environment but belongs to `THM-M-1551` (zero-curvature representation). It models
derivatives as arbitrary linear endomorphisms of an abstract Lie algebra and its checked wrapper
derives `ZeroCurvature` from `LaxCompatibilityEquation` after those predicates are defined as
algebraic rearrangements. It contains no AKNS operator, spectral problem, coefficient evolution,
named hierarchy flow, or checked source-to-AKNS bridge. It is therefore negative boundary evidence,
not an exact target or an import that can legitimately complete this statement node.

First failed gate: rev-5.6 section 5 exact human-claim and source-statement identification, before
the Lean 4 statement gate in section 5.1. The node remains open at `M4`: no canonical declaration,
normalized-expression fingerprint, minimal exact-target import, checked alternate encoding, or
four-class mutation suite can be produced without inventing missing mathematics. Retry only after
an accountable source decision pins one exact AKNS result and freezes all conventions, hypotheses,
and degenerate cases above. No statement acceptance, proof credit, audit completion, or theorem
completion is claimed.

## Commands and results

All commands ran in this worker clone. The Lean check reused the canonical pinned `.lake` artifacts.
No update, build, fetch, clone, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1558` | 0 | Rank 570, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_210.lean` | 0 | Nearby abstract zero-curvature module elaborated; it does not elaborate an exact AKNS target |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_210.lean` | 0 | SHA-256 values `651c8a...b1d2`, `321626...2d81`, and `bb147a...a8b` respectively |
| `rg -n -i 'AKNS\|Ablowitz\|Kaup\|Newell\|Segur' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1558/**'` | 0 | Found metadata, neighboring dossiers, and the generic zero-curvature material; no reviewed exact AKNS theorem transcription or Lean target |

No `.stage1-worker-selftest.json` is emitted because the assigned statement phase is blocked rather
than genuinely self-tested.
