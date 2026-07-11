# THM-M-0085 anchor-audit validation

Item: `S56-M-0085-ANCHOR_AUDIT`  
Base revision: `f9413ba75c44c7b473fce84209ab02c65afd10cd`

## Result

Pinned mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains the exact usable
candidate `CategoryTheory.Monad.monadicOfCreatesGSplitCoequalizers` in
`Mathlib.CategoryTheory.Monad.Monadicity`. Given the frozen adjunction and the canonical
`CreatesColimitOfIsSplitPair G` hypothesis, its `eqv` field has exactly
`(Monad.comparison adj).IsEquivalence`. `AnchorAudit.lean` checks that projection directly, so the
audit does not conflate mathlib's packaged `MonadicRightAdjoint G` with an unspecified alternate
adjunction.

The pinned source gives an explicit ordinary definition. It constructs the has, preserves, and
reflects instances for `G`-split pairs and terminates in
`monadicOfHasPreservesReflectsGSplitCoequalizers`. Lean's axiom report for the candidate is
`[propext, Classical.choice, Quot.sound]`; its source has no `sorry`, axiom declaration, unsafe
body, native computation, or external oracle. The Apache-2.0 source is already inside the pinned
Lake closure. The historical `S1_M_140` wrapper is only an alias of this same body and receives no
distinct proof credit.

Bounded external discovery found only mathlib for the exact declaration. Sourcegraph returned
three hits in one mathlib file. GitHub repository metadata searches returned no relevant external
project, while unauthenticated GitHub code search returned HTTP 401 and is recorded as blocked,
not as a negative result. No moving dependency was fetched or installed.

This phase therefore locates an `M0-P` candidate and clears the dependency-integration question.
It does not add the canonical theorem proof, freeze the obligation tree, or claim theorem
completion; those remain owned by later nodes.

## Commands and results

Commands ran on 2026-07-12 in the worker clone. Lean reused the existing pinned `.lake` artifacts.
No update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and all 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-0085` | 0 | rank 140, planned, theorem incomplete |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0085/Statement.lean` | 0 | frozen canonical target re-elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0085/AnchorAudit.lean` | 0 | exact candidate type and `eqv` projection elaborated; axiom report contained only `propext`, `Classical.choice`, `Quot.sound` |
| `python3 Stage1_Instances/THM-M-0085/check_anchor_audit.py` | 0 | schema boundary, manifest pin, installed mathlib HEAD, exact candidate, and source terminal agreed |
| `rg -n 'monadicOfCreatesGSplitCoequalizers|CreatesColimitOfIsSplitPair' Formalizations/Lean/.lake/packages --glob '*.lean'` | 0 | exact constructor in pinned mathlib plus downstream references; no distinct installed proof body |
| Sourcegraph query recorded in `anchor-audit.json` | 0 | three matches, one mathlib repository; response SHA-256 `77636ab18b551983c731b9e459300773feea190a2ef0acd91022be823451eb59` |
| two GitHub repository searches recorded in `anchor-audit.json` | 0 | no relevant external project; complete metadata responses |
| unauthenticated GitHub code search recorded in `anchor-audit.json` | 0 request; HTTP 401 | blocked lane, no absence claim |
| `python3 -m json.tool Stage1_Instances/THM-M-0085/anchor-audit.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-0085 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Handoff boundary

The proof node may define the canonical wrapper by projecting
`(Monad.monadicOfCreatesGSplitCoequalizers adj).eqv`. Before proof credit, it must place that
wrapper in the frozen obligation and provenance graphs and run its own exact-type, axiom, terminal
body, and composition checks. Master acceptance is still required for this audit receipt.
