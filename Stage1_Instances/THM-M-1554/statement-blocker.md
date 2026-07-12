# THM-M-1554 statement-phase blocker

Item: `S56-M-1554-STATEMENT`  
Base revision: `110eef5926707beba105078ad2163c88ae8bf0e8`

## Verdict

The exact Lean 4 target cannot yet be truthfully frozen or elaborated. The repository's discovery
record supplies only the family name "Backlund transformation", the phrase "a transformation of
integrable systems", an attribution to Albert Backlund, and the year 1876. It gives no proposition,
displayed equations, theorem locator, or reviewed mathematical source. The intake dependency bounds
a possible auto-Backlund preservation/compatibility result but deliberately leaves the equation
and every convention open.

Those omissions are proposition-changing. Backlund transformations can relate different equations
or map solutions of one equation to other solutions of the same equation. Even after selecting the
familiar sine-Gordon specialization, sources use different independent variables, PDE signs and
scales, first-order relations, parameter normalizations, and regularity assumptions. Compatibility
of a prescribed first-order system is also not the same claim as local construction, preservation,
existence, uniqueness, invertibility, permutability, or a global transformation theorem. Choosing
among these without a pinpoint source would substitute an invented nearby theorem for this target.

No canonical expression therefore exists on which to establish minimal imports, an elaborated
expression hash, checked transports, or the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. Defining an opaque `IsBacklundTransform` predicate containing
the desired conclusion would merely hide the missing mathematics and is not an admissible target.

First failed gate: rev-5.6 exact source-statement identification, before Lean elaboration. Machine
debt remains `M4`. There is no canonical declaration, statement acceptance, proof credit, audit
completion, or theorem completion.

## Lean boundary

The pinned Lean environment is available. Repository search found only the underspecified catalogue
records and intake dossier, and a read-only search of pinned mathlib found no declaration matching
`Backlund`, `Baecklund`, `sine-Gordon`, or `integrable system`. This is negative statement-surface
evidence only, not an anchor audit. Running Lean against a manufactured generic predicate or a
silently selected sine-Gordon statement would not validate the exact assigned target.

## Commands and results

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The canonical `.lake` artifacts
were read only. No update, build, clone, fetch, or dependency mutation was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | Passed: 15 assurance groups and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | 0 | Passed: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1554` | 0 | Rank 566, planned, legacy artifacts unaccepted, theorem incomplete |
| repository `rg` search for `Backlund`, `Baecklund`, and the Chinese discovery wording | 0 | Only catalogue metadata and the intake dossier; no exact proposition or Lean declaration |
| pinned-mathlib `rg` search for `Backlund`, `Baecklund`, `sine-Gordon`, and `integrable system` | 0 wrapper | No matches; the inner `rg` returned 1 |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | SHA-256 values `651c8a...b1d2` and `321626...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |

## Retry condition

Preserve an immutable mathematical source and content hash, transcribe the exact theorem and
relevant displayed equations with edition/revision and page/formula locators, audit errata, and
obtain independent approval of every domain, regularity, parameter, convention, and boundary
choice. The statement phase can then encode the actual analytic substrate, minimize imports,
elaborate and fingerprint the expression, check transports, and run all four mutation classes.

The assigned phase is blocked rather than genuinely self-tested, so no
`.stage1-worker-selftest.json` is emitted.
