# Anchor audit

Item: `S56-M-0541-ANCHOR_AUDIT`  
Base revision: `b76ec411182f176247ffbf5fa8d421890f54e69c`

## Verdict

No exact repo-local, pinned-mathlib, pinned-external, or credible public Lean 4 closure was found for
`Stage1Instances.THM_M_0541.StatementShape`. The machine classification remains `M3`: the exact
interface elaborates and a strong general square-zero theorem exists, but the target-specific
construction and transport do not.

At immutable mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the best anchor is
`AlgebraicTopology.AlternatingFaceMapComplex.d_squared` in
`Mathlib.AlgebraicTopology.AlternatingFaceMapComplex`. It proves that the alternating sum of face
maps of any simplicial object squares to zero, using a finite-sum cancellation bijection. The same
module packages this as `AlternatingFaceMapComplex.obj` and the functor
`AlgebraicTopology.alternatingFaceMapComplex`.

This is not an exact theorem match. Its input is already a `SimplicialObject C`, while the frozen
root begins with `K : AbstractSimplicialComplex V` and asks for explicit `Finsupp` chain groups and
the basis formula using `Statement.face`. Pinned mathlib's only `SimplicialComplex` module is
`Basic.lean`; it supplies the input structure and face closure but no chain or homology bridge.
`HomologicalComplex.homologyFunctor` is downstream of a constructed chain complex and cannot close
the root either.

The audited `d_squared` body is at lines 73-114 and `obj` packages it at lines 121-123. Scans of the
two relevant source files found no `sorry`, `admit`, `sorryAx`, `axiom`, or `unsafe`. Lean's axiom
report for the candidate construction is `[propext, Classical.choice, Quot.sound]`; these are
ordinary mathlib foundation dependencies, but no trust credit is transferred to the absent exact
wrapper. The source hashes and complete structured candidate ledger are in `anchor-audit.json`.

## External search

Repository-wide searches found no relevant declaration outside this dossier and no match in any
pinned non-mathlib dependency. Public GitHub repository API searches for `simplicial complex lean4`,
`simplicial homology language:Lean`, and `algebraic topology lean4` found no credible exact project.
The grep.app API returned HTTP 429 for both attempted symbol/phrase searches, so that surface is
explicitly incomplete rather than treated as a negative result. No moving dependency was fetched,
and there is consequently no immutable external candidate revision to integrate.

## Remaining cut set

Downstream proof work must construct the free-abelian simplicial object or an equivalent face
system from `K`, identify its categorical faces with `Statement.face` on every basis chain, and
transport the general `d_squared` theorem to the exact `AddMonoidHom` equality. Only then can the
terminal proof and axiom closure of an exact wrapper be audited.

## Validation

All commands ran in the worker clone against the existing pinned Lake environment; none mutated
`.lake`.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0541/AnchorProbe.lean` | 0 | all adjacent declarations elaborated; axiom reports printed |
| `python3 Stage1_Instances/THM-M-0541/check_anchor_audit.py` | 0 | receipt invariants, manifest pin, source hashes, negative exact-match classifications, and probe coverage passed |
| `rg -n '\\bsorry\\b|\\badmit\\b|sorryAx|\\baxiom\\b|unsafe' <two candidate source files>` | 1 | no matches (expected negative scan) |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546 |
| `python3 scripts/stage1_target.py show THM-M-0541` | 0 | rank 598, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-0541` | 0 | no whitespace errors |

This is node-specific, self-tested audit evidence pending master acceptance. It is not proof,
`M0`, `AUDIT-Z`, validation, release, or theorem-completion evidence.
