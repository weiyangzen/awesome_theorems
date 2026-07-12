# Anchor-audit validation record

Item: `S56-M-1161-ANCHOR_AUDIT`  
Base revision: `54743c8a753017ec2ce50ffebf85facec9112b95`

## Verdict

The exact repo-local target is a proposition definition without a proof body. Pinned mathlib at
`8a178386ffc0f5fef0b77738bb5449d50efeea95` provides a genuine compact-operator
eigenvalue-or-resolvent alternative and adjoint orthogonality identities. The checked wrapper in
`AnchorAudit.lean` confirms the closest terminal mathlib type, but that type does not mention the
integral realization, the `lambda = 0` case, or the canonical target's full adjoint solvability
equivalence.

The public search found one distinct external project:
`facebookresearch/atlas-lean@34ffed396f376454c1a9b297f3fd74c5c801fb50`. Its
`fredholm_alternative_full` uses the same Lean and mathlib revisions, but assumes a self-adjoint
compact operator and concludes a narrower range/kernel statement. It therefore cannot substitute
for this target. Its source file also has admitted declarations elsewhere, so it was inventoried
but neither imported nor credited as trusted closure.

The exact root remains `M4`. This is a completed bounded anchor audit, not proof completion and not
a claim that no further Lean candidate exists.

## Commands and results

Commands ran on 2026-07-12. Lean used only the existing pinned `.lake` artifacts; no update, fetch,
clone, or dependency build was performed.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1161/AnchorAudit.lean` | 0 | Seven pinned declarations and the typed mathlib wrapper elaborated |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1161/FredholmIntegralEquationStatement.lean` | 0 | Exact canonical proposition re-elaborated |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95`, equal to the manifest pin |
| `rg -n -i 'fredholm|hasEigenvalue_or_mem_resolventSet|orthogonal_range' ...` | 0 | Located pinned mathlib anchors and repo-local wrappers; no exact integral-equation proof declaration located |
| `curl ... sourcegraph.com/.api/search/stream ...` | 0 | 12 matches in mathlib4 and atlas-lean; response SHA-256 `5b6939dd64e4328dfbfe7c686b4c8220c9a7b8797ddc7ee24b9ae7523a77e955` |
| `curl ... api.github.com/search/repositories?q=fredholm+lean+theorem` | 0 | Zero complete repository results; response SHA-256 `08c082fdf7ca87ba911a2aabb0f0cf2d3e482a6feeaac9713e4578c20b2600b2` |
| `curl ... api.github.com/search/code?q=fredholm+language:Lean` | 0 | Captured HTTP 401 authentication blocker; response SHA-256 `b7dbd173f33b19650f61b1c528737e2037cf768d90076fdfce5d32541765e29e` |
| `curl ... raw.githubusercontent.com/facebookresearch/atlas-lean/34ffed.../SpectralTheory.lean` | 0 | Immutable candidate source SHA-256 `f61ca2778c4dd72488a79a9adc0282575246ed13e862a30dd551764a3cd2ce5c` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | rev-5.6 standard and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique ordered targets passed |
| `python3 scripts/stage1_target.py show THM-M-1161` | 0 | rank 364, planned, rework required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1161/anchor-audit.json >/dev/null` | 0 | Audit artifact is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1161 .stage1-worker-selftest.json` | 0 | No whitespace errors |

## Open integration gate

The proof phase must establish the operator/integral transport, scalar cases, compact-perturbation
closed range, adjoint compatibility, and both alternative branches. An external candidate may be
credited only after exact-type comparison, immutable dependency and license review, placeholder and
axiom inspection, and a successful local import or checked wrapper.
