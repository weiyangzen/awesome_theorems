# THM-M-1552 statement-phase blocker

Item: `S56-M-1552-STATEMENT`  
Base revision: `057a073c6e854b6552236ab330b9de2e388d24ea`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The repository's complete
human statement is only "tau functions of integrable systems". It gives no primary source,
theorem or equation number, hierarchy, time domain, solution class, regularity, normalization, or
conclusion. In particular, it does not decide among existence of a tau function, a Hirota/residue
characterization, a finite-soliton determinant formula, a reconstruction theorem, a Fredholm
determinant identity, or an isomonodromic definition. Those are inequivalent propositions with
different binders, hypotheses, and behavior at zero or constant tau functions, gauge rescalings,
tau zeros, and singular reconstruction charts.

The intake dependency deliberately preserves this ambiguity: its canonical formal module and
declaration are null and its first open task is identification of an immutable primary-source
theorem. Choosing a KP, Toda, KdV, Sato-Grassmannian, Fredholm, or isomonodromic branch here would
therefore broaden or substitute the source wording rather than elaborate it exactly.

The legacy module `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_211.lean` elaborates in the
existing pinned environment, but it is discovery and negative-boundary evidence only. Its
`StatementShape` asserts tau-witness existence for an arbitrary `IntegrableHierarchyModel` whose
Hirota identity, hierarchy compatibility, normalization, reconstruction relation, and three model
premises are unconstrained proposition fields. It neither defines a concrete integrable hierarchy
nor crosswalks those fields to a source theorem. The module's selected KdV determinant branch also
uses an arbitrary matrix-valued function and explicitly leaves the standard soliton matrix and
Hirota/KdV identities for later work. Copying either interface would not produce the exact target.

First failed gate: rev-5.6 exact source-statement identity, before canonical Lean elaboration. The
statement node remains at `M4`. There is no canonical declaration or expression fingerprint,
minimal exact-target import set, checked alternate transport, or meaningful removed-hypothesis,
domain, binder-scope, and boundary mutation suite. No statement acceptance, proof credit, audit
completion, or theorem completion is claimed.

## Required unblock

An accountable reviewer must select an immutable primary source by edition and theorem/equation
and page, record exact wording and errata, and freeze the hierarchy, time variables, solution and
regularity classes, normalization/gauge convention, hypotheses, conclusion, and degenerate-case
policy. A later statement worker can then encode that claim, minimize its pinned imports, print and
hash its elaborated expression, check any alternate encoding, and run the four mutation classes.

## Commands and results

Commands ran in this worker clone on 2026-07-12. The Lean check reused the existing canonical
`.lake` artifacts. No update, build, fetch, clone, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Standard projection passed: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Manifest passed: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1552` | 0 | Rank 211, planned, `hard_mathlib_anchor_and_wrapper`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_211.lean)` | 0 | Legacy abstract boundary module elaborated and printed its checked declarations; this is not exact-statement evidence |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_211.lean` | 0 | SHA-256 values `651c8acc...b1d2`, `321626c8...2d81`, and `b03efcb0...d94d` respectively |
| `rg -n -i 'tau function\|tau函数\|可积系统的tau函数\|Hirota\|Sato Grassmannian\|isomonodromic' . --glob '!Formalizations/Lean/.lake/**' --glob '!Stage1_Instances/THM-M-1552/**'` | 0 | 209 matching lines; target-specific material reduces to terse generated metadata and the unaccepted legacy boundary, with no exact primary-source theorem transcription |
| `rg -n '\\bsorry\\b\|\\baxiom\\b\|placeholder\|fake result' Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_211.lean` | 1 | No prohibited proof device or fake-result marker found (`rg` exit 1 means no match) |
| `git diff --check` | 0 | No whitespace errors in the owned artifact |

The assigned statement phase is blocked rather than genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
