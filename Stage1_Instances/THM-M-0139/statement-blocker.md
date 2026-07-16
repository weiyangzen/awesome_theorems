# THM-M-0139 statement-phase blocker

Item: `S56-M-0139-STATEMENT`  
Base revision: `94009a6bebd743588e09c3b45bfbf18bf9b5c5e3`

## Verdict

The exact-statement gate is blocked, so no canonical Lean declaration, expression fingerprint, or
statement acceptance is claimed. The intake deliberately selects Kazhdan and Lusztig (1979),
Conjecture 1.5 as the intended theorem family while leaving its convention-sensitive formula open
until the primary text is pinned and transcribed. This worker could verify the paper's bibliographic
record, but could not obtain an immutable full-text artifact containing Conjecture 1.5. The DOI and
Crossref record provide title, authors, journal, volume, year, and pages only; the publisher PDF
request returned an HTML access page, and EuDML rejected the automated request.

Without the source text, the dossier cannot truthfully fix the source's Weyl-group parametrization,
Bruhat-order orientation, dot-action and longest-element conventions, the order of the Verma and
simple indices, or the normalization and index order of `P_{x,y}`. Those choices affect whether the
right side is written as `P_{y,x}(1)`, with longest-element transforms, or in an equivalent
character formulation. Choosing one from memory would violate the intake requirement and could
substitute a conventionally related proposition for the exact source claim.

The legacy module `AwesomeTheorems/Stage1/S1_M_055.lean` elaborates, but it is not exact-statement
evidence. Its `KazhdanLusztigPolynomialModel` takes the Bruhat relations, polynomials, and recursion
as structure fields; its representation surface takes category-O axioms and composition
multiplicities as fields; and its `StatementShape` universally asserts a formula over every such
freely supplied datum. In particular, it neither constructs the source objects nor binds them to
the 1979 conventions. Importing that large discovery artifact, or copying its abstract formula into
a new file, would only elaborate a locally invented interface already excluded by the intake.

The pinned mathlib tree contains no occurrence of `Kazhdan`, `Lusztig`, `BGG category`, `Verma
module`, `compositionMultiplicity`, or `VermaMultiplicity`. Thus the existing environment does not
provide a native semantic API from which the missing source choices can be recovered. This is not a
license to encode the conclusion as a `Prop` field or assume the desired equality as data.

## First failed gate

The first failed gate is exact source-statement identification under rev-5.6 section 5.1. Ordered
binders, complete hypotheses, conclusion, degenerate cases, checked alternate transports, and the
four required mutation classes all depend on unresolved source conventions. Machine status remains
`M4`; statement acceptance, audit completion, and theorem completion are false.

Retry only after an immutable copy or independently accepted exact transcription of Conjecture 1.5
is available with a page/formula locator, digest, notation ledger, and errata result. The next run
must transcribe every source hypothesis and convention, implement (or pin) the needed category-O
and Kazhdan-Lusztig interfaces without circular conclusion fields, and then elaborate the exact
target with checked transports to any alternate character formula.

## Earlier discovery commands

The source-access and legacy-discovery commands below ran in an earlier worker clone on 2026-07-12.
They are retained as historical blocker context, not claimed as commands rerun by this handoff.
The current exact self-test commands and exit codes are bound in `statement-receipt.json` and
`.stage1-worker-selftest.json`. Lean validation used the existing pinned Lake artifacts; no
dependency update, fetch, clone, or build was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | standard projection passed: 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | manifest passed: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0139` | 0 | rank 55, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_055.lean` | 0 | legacy abstract discovery module elaborated; no exact-target credit |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_055.lean` | 0 | SHA-256 values `651c8acc...b1d2`, `321626c8...2d81`, and `e1a5e161...83cb` |
| fixed-string searches for `Kazhdan`, `Lusztig`, `BGG category`, `Verma module`, `compositionMultiplicity`, and `VermaMultiplicity` in pinned Mathlib | 0 | each search found zero files; the shell loop itself exited successfully |
| `curl -L --fail --max-time 30 https://eudml.org/doc/142995` | 22 | HTTP 403; no primary-source artifact obtained |
| `curl -L https://api.crossref.org/works/10.1007/BF01390031` | 0 | bibliographic metadata confirmed pages 165-184, but no theorem text or formula was supplied |
| `curl -L https://link.springer.com/content/pdf/10.1007/BF01390031.pdf` | 0 | returned a 229744-byte HTML access page rather than a PDF |

The target-owned semantic validator now self-tests this negative boundary and emits
`phase_accepted=false`. That establishes a truthful worker handoff only; the HEAD contract says a raw
blocked result cannot close the positive statement phase. It does not make the missing canonical
statement, expression fingerprint, transports, or mutations exist.
