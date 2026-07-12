# Exact-statement gate: blocked

Item: `S56-M-0691-STATEMENT`  
Theorem: `THM-M-0691`  
Base revision: `6d9089613f4343925b2ff1ec1a221f0575a93b5f`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical wording is "a lower bound on the proof length of the pigeonhole principle".
That identifies the result family associated with Haken's resolution lower bound, but it does not
state a proposition.

In particular, the record does not fix the pigeonhole CNF family and parameter range, variable and
initial-clause conventions, resolution inference rules, tree-like or DAG-like derivations, the
meaning of proof "length", an explicit lower-bound function and constants, a parameter threshold,
or small-parameter cases. These choices alter the domains, ordered binders, hypotheses, and
conclusion. Substituting ordinary pigeonhole unsatisfiability, an abstract assumed
`ResolutionProof` predicate, or a familiar exponential-bound formulation would invent missing
mathematics.

The intake names Armin Haken's 1985 paper *The intractability of resolution* only as an uninspected
bibliographic candidate. It does not preserve an immutable edition, identify a pinpoint theorem or
display, transcribe incorporated definitions, resolve errata, or provide independent source review.
Consequently there is no canonical expression to fingerprint and no sound removed-hypothesis,
changed-domain, binder-scope, or boundary mutation to test. The rev-5.6 section 5.1 gate therefore
fails before proof evidence may be inspected. Machine state remains `M4`; statement acceptance and
theorem completion are false.

## Pinned Lean boundary

The existing `IntakeProbe.lean` imports generic finite-cardinality support and checks `Fin`,
`Finset`, `Fintype.card`, `Fintype.card_fin`, `Finset.univ`, and `Finset.card_univ`. It re-elaborates
successfully, showing that the pinned Lean environment is usable. A narrow pinned-mathlib search
found combinatorial pigeonhole APIs, but no Haken resolution lower-bound declaration or
theorem-specific resolution-proof encoding. The probe is not the canonical target and receives no
statement or proof credit.

The environment is Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. Existing canonical `.lake` artifacts were used
read-only; no update, build, fetch, clone, or dependency mutation was run.

## Validation evidence

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0691` | 0 | rank 732, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0 at the commit above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | hashes `651c8a...1d2` and `321626...d81`, recorded in the JSON blocker |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision above |
| repository `rg` search for the theorem ID, Chinese/English names, gloss, and paper title | 0 | only underspecified metadata and the intake's candidate citation were found; no exact proposition |
| pinned-mathlib `rg` search for Haken, resolution proofs, pigeonhole resolution, LRAT, and pigeonhole APIs | 0 | generic pigeonhole APIs were found, but no theorem-specific resolution lower-bound target |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0691/IntakeProbe.lean` | 0 | all six generic finite-indexing/cardinality API checks elaborated |
| `rg -n '\\b(sorry|admit)\\b|^[[:space:]]*axiom\\b' Stage1_Instances/THM-M-0691 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom found |
| `python3 -m json.tool Stage1_Instances/THM-M-0691/statement-blocker.json` | 0 | blocker JSON is syntactically valid |
| `git diff --check -- Stage1_Instances/THM-M-0691` | 0 | no whitespace errors |

## Retry condition

An accountable source reviewer must preserve and hash an immutable primary-source edition, select
and transcribe the exact statement and incorporated definitions, dispose of errata, and
independently approve the source mapping. A later statement worker can then encode the same claim,
minimize its pinned imports, serialize and hash the elaborated expression, check alternate
transports, and run all four required mutation classes.

This is the first failed gate, not completion of the statement node or any later node. The assigned
phase is not genuinely self-tested, so no `.stage1-worker-selftest.json` is emitted.
