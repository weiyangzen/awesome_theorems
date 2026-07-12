# Anchor-audit validation record

Item: `S56-M-1171-ANCHOR_AUDIT`  
Base revision: `31b7ab5b3902c4a80878c2007218f90566a8b85c`

## Result

The exact repo-local artifact is a proposition definition without a proof body. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` contains checked second-derivative symmetry,
iterated-derivative, Laplacian, Schwartz-space, and `eLpNorm` infrastructure. The probes in
`AnchorAudit.lean` elaborate those declarations, but the pinned source has no Calderon-Zygmund or
Riesz-transform terminal result and none of the probes bounds a Hessian by a Laplacian in `L^p`.

The public search found a substantive related project,
`fpvandoorn/carleson@fdcce451b494680b1fd5534236a71d9b258860b2`. Its
`czOperator_weak_1_1` proves a weak `(1,1)` estimate for a project-specific truncated singular
integral. It is not the exact strong `L^p`, `1 < p < infinity`, Hessian-by-Laplacian target. The
project also pins Lean `4.30.0-rc2` and mathlib `1a4917...`, outside the local dependency closure.
Its immutable module was source-audited, not imported or granted kernel proof credit.

The exact root therefore remains `M4`. This is a completed bounded anchor audit, not theorem
completion and not a claim that no further Lean candidate exists.

## Commands and results

Commands ran on 2026-07-12. Lean used only the existing pinned `.lake` artifacts; no update, fetch,
clone, dependency build, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1171/AnchorAudit.lean` | 0 | Six pinned mathlib support declarations elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1171/Statement.lean` | 0 | Exact canonical proposition and checked definitional transport re-elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the manifest pin |
| `rg -n -i 'calder[oó]n\|zygmund\|riesz transform\|hessian\|laplacian.*eLpNorm' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only derivative/Laplacian infrastructure and unrelated prose hits; no exact or singular-integral terminal candidate |
| Sourcegraph search for Calderon-Zygmund spellings and `RieszTransform` in Lean | 0 | 18 matches in carleson, Seed-Prover, and DeGiorgi; response SHA-256 `d5846c...4b53` |
| GitHub REST repository search for `Calderon-Zygmund Lean` | 0 | Zero complete repository results; response SHA-256 `08c082...2600` |
| GitHub REST code search for `Calderon-Zygmund language:Lean` | 0 | HTTP 401 authentication blocker; response SHA-256 `b7dbd1...e29e` |
| Immutable raw inspection of `fpvandoorn/carleson@fdcce451.../WeakCalderonZygmund.lean` | 0 | `czOperator_weak_1_1` located; source SHA-256 `2c4fe4...9495`; no `sorry` or `axiom` token in that module |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546-target coverage valid |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets at uniform L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1171` | 0 | rank 372, planned, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1171/anchor-audit.json` | 0 | Audit artifact is valid JSON |

## Open integration gate

Future proof work must supply the fundamental-solution or Riesz-transform representation, strong
`L^p` boundedness, componentwise assembly into the Hessian operator norm, and exact transports to
the frozen target. Any external result requires immutable dependency and license review,
transitive placeholder and axiom inspection, and successful local elaboration before proof credit.
