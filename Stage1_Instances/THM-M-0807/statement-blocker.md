# Exact-statement gate: blocked

Item: `S56-M-0807-STATEMENT`  
Theorem: `THM-M-0807`  
Base revision: `9b651a1d3f6c41876f66c5933991b6cbaceeb70d`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is the title "analytic determinacy" and the gloss "determinacy of
analytic games". It gives no primary-source edition, theorem/page, definitions, or assumptions.
The accepted intake accordingly records a familiar Gale-Stewart formulation only as a provisional
candidate and leaves the canonical claim null.

The missing information changes the proposition rather than merely its Lean spelling. In
particular, the metadata does not fix:

- the move alphabet, length, turn convention, legal positions, or strategy/compatibility semantics;
- Baire space versus Cantor space and the checked transport between those game encodings;
- boldface versus lightface analyticity, allowed real parameters, or the projection/tree coding;
- which player owns the payoff and the exact quantifier order in "determined";
- the ambient foundational theory and every large-cardinal or determinacy hypothesis;
- whether the intended root is the analytic-determinacy principle itself or a conditional theorem
  deriving it from a named foundation hypothesis.

Selecting any one of these alternatives would invent missing mathematics. In particular, silently
stating unconditional determinacy for every analytic payoff, assuming the target determinacy
principle, proving only Borel determinacy, or adding an arbitrary strong premise would respectively
broaden, circularize, weaken, or substitute the source claim. Consequently there is no canonical
human statement from which to choose minimal imports, serialize an elaborated kernel expression,
compile alternate-form transports, or run the required removed-hypothesis, changed-domain,
binder-scope, and boundary mutations. The section 5.1 statement gate fails at exact source identity.

Machine state remains `M4`; statement acceptance, audit completion, and theorem completion are
false. No theorem declaration, axiom, placeholder, or convenient proxy was added.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports
`Mathlib.SetTheory.Descriptive.Tree` and
`Mathlib.MeasureTheory.Constructions.Polish.Basic`. It re-elaborates five descriptive-set-theory
types, including `MeasureTheory.AnalyticSet`; this establishes only that some encoding ingredients
exist. A narrow search of pinned mathlib found no declaration for analytic determinacy,
Gale-Stewart games, winning strategies, or determined games. Neither the probe nor the no-match
search establishes a canonical target or a proof.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The `lean-toolchain` SHA-256 is
`651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`; the
`lake-manifest.json` SHA-256 is
`321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`. The existing `.lake`
artifacts were used read-only; no update, build, clone, fetch, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0807` | 0 | rank 810, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision recorded above |
| repository `rg` search for the theorem ID, Chinese/English label, and gloss | 0 | found only underspecified metadata and the intake dossier; no source-frozen proposition |
| pinned-mathlib `rg` search for analytic determinacy, analytic games, Gale-Stewart, winning strategies, and determined games | 1 | no matching game-determinacy declaration (`rg` exit 1 means no match) |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0807/IntakeProbe.lean` | 0 | five pinned descriptive-set-theory substrate checks elaborated |
| `rg -n '\\b(sorry\|admit)\\b\|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0807 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom in target Lean source |

## Retry condition

An accountable source review must preserve and hash an immutable primary-source edition, select
and transcribe one exact theorem with its incorporated definitions, dispose of errata, and obtain
independent approval. It must freeze all game, analytic-pointclass, parameter, coding, quantifier,
and foundation choices listed above. A later statement run can then encode that same claim, minimize
its pinned imports, fingerprint the elaborated expression, check alternate encodings, and execute
all four mutation classes.

This is the first failed gate, not completion of the statement node or any later phase. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
