# Anchor audit record

Item: `S56-M-0665-ANCHOR_AUDIT`  
Base revision: `20b8abf35019d24fc944d56d6af62cb098711ee3`

## Frozen target

This audit is against `Stage1Instances.THM_M_0665.PilaWilkie`, expression SHA-256
`da66c715ce12af9ff6dfb55a721665c8240358c0ee547062b3d2fc10c7785944`. It does not
credit the weaker legacy `StatementShape`, an assumed boundary package, or a related target.

## Pinned mathlib and repository

The manifest pins mathlib at `8a178386ffc0f5fef0b77738bb5449d50efeea95` and Lean at
`v4.29.0`. `AnchorAudit.lean` checks the usable statement ingredients: first-order parameter
definability, ring-language definability over `Real`, connected/nontrivial sets, finite-set
cardinality, and real exponentiation. A source search found no Pila-Wilkie declaration, o-minimal
geometry library, or subpolynomial rational-point counting proof in pinned mathlib.

The repo-local `THM-M-0441` and legacy `S1_M_087.lean` artifacts concern a separate target and do
not contain a terminal proof. In particular, their theorem-shaped `subpolynomialBound` is supplied
as data. The current target's exact `Statement.lean` is therefore the only normalized local
candidate, and it is statement-only.

## External Lean 4 candidates

Repository discovery used the GitHub repository API on 2026-07-12. Exact Pila-Wilkie searches
returned no repository. Broader o-minimal searches returned three candidates; immutable source
archives, manifests, toolchains, and matching source families were inspected.

| Candidate and immutable revision | Toolchain / mathlib | Finding | Integration decision |
|---|---|---|---|
| `theominimalist/monotonicity@6e3ee129f0d9cc0d9d6a58cac4fc03bc7b121b30` | no toolchain or manifest | custom o-minimal monotonicity work; 30 `sorry` occurrences and 12 top-level `axiom` declarations; no height, algebraic part, or counting theorem | infeasible: no package boundary, placeholders/axioms, and no exact closure |
| `tonysf/lean-OMIN@fd8b4f3423265d9beb290a08992ad866eb5230e0` | Lean `v4.30.0-rc1`; mathlib `f8770bc8...` | custom `OMinStructure`; exported cell decomposition projects the `cellDecomposition_axiom` structure field; no rational-height or Pila-Wilkie counting declaration | infeasible: incompatible pins and only an assumed supporting interface |
| `KittySaya/Lean-ominimal@4429c2cc75e49a83043175f7a85c4c1bf284c2eb` | Lean `v4.19.0-rc3`; mathlib `44efe040...` | pure dense-order example; five `sorry` occurrences; no real-field counting surface | infeasible: incompatible pins, placeholders, and wrong theorem surface |

No candidate is imported or credited. The downloaded archives were inspection artifacts in `/tmp`
only; no dependency clone, fetch, update, or `.lake` mutation was performed. The search is bounded
and dated, not a claim of global absence.

## Classification

The exact root remains `M3`: the local proposition and its ingredient definitions elaborate, but
no proof body or usable exact external theorem was located. The phase inventory is complete and
self-tested pending master acceptance. Human-source review, obligation expansion, proof, trust
closure, replay, and release all remain open; theorem completion is false.

## Validation

Commands were run on 2026-07-12 (Asia/Shanghai).

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-0665/AnchorAudit.lean` from `Formalizations/Lean` | 0 | all pinned ingredient types elaborated and six declarations printed |
| `lake env lean ../../Stage1_Instances/THM-M-0665/Statement.lean` from `Formalizations/Lean` | 0 | exact frozen target and statement checks re-elaborated |
| `python3 ../../Stage1_Instances/THM-M-0665/check_statement.py` from `Formalizations/Lean` | 0 | exact expression SHA-256 reproduced; all three mutations distinguished |
| scoped `rg` over repository Lean and pinned mathlib | 0 | local statement/boundary and generic ingredients found; no terminal Pila-Wilkie proof declaration |
| six GitHub repository API searches recorded in `anchor-audit.json` | 0 | result counts `0, 0, 2, 1, 0, 0`; all responses complete and content-hashed |
| immutable archive download and source scan for all three candidates | 0 | archive hashes, pins, theorem surfaces, and placeholder/axiom boundaries recorded |
| `python3 -m json.tool Stage1_Instances/THM-M-0665/anchor-audit.json` | 0 | structured audit parsed |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage passed |
| `python3 scripts/stage1_target.py check` | 0 | ordered uniform-L0 manifest passed |
| `python3 scripts/stage1_target.py show THM-M-0665` | 0 | rank 709, planned, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0665 .stage1-worker-selftest.json` | 0 | no whitespace errors |
