# Statement gate blocker

Item: `S56-M-0314-STATEMENT`  
Base revision: `fc8e70dc8b3df070bf824de575d4a369542a621f`

## First failed gate

The exact-source statement gate is blocked. The only repository claim is the Chinese phrase
`紧自伴算子的谱分解` ("spectral decomposition of compact self-adjoint operators") in
`Docs/researches/math_theorems.md`; Stage0 explicitly leaves definitions, assumptions, equivalent
forms, axioms, proof path, and formal artifacts unspecified. No primary-source title, immutable
edition, theorem number, page, quotation, or errata record identifies the intended proposition.

Consequently, selecting a canonical target would invent at least the scalar field, the precise
decomposition encoding, and whether finite multiplicity is part of the root. This is a hard stop
under the rev-5.6 freeze-target rules, not permission to substitute a nearby mathlib theorem.

## Lean evidence for the ambiguity

`StatementCandidateProbe.lean` uses the single direct import
`Mathlib.Analysis.InnerProductSpace.Spectrum` and elaborates two nonidentical candidate
propositions over an arbitrary `RCLike` scalar field and complete Hilbert space:

1. `CompleteEigenspaceSpanTarget` says the orthogonal complement of the supremum of all
   eigenspaces is bottom.
2. `CompleteEigenspaceSpanWithFiniteMultiplicityTarget` additionally requires every nonzero
   eigenspace to be finite-dimensional.

Pinned mathlib exports declarations supporting both clauses. Their availability does not decide
which source proposition the repository intended. An orthonormal eigenbasis, convergent expansion,
or spectrum-enumeration formulation would make further materially different choices.

## Commands and results

Commands ran in this worker clone. Lean used the existing pinned `.lake` environment read-only; no
update, build, fetch, or clone command was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0314` | 0 | rank 816, planned, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0314/StatementCandidateProbe.lean)` | 0 | both candidate propositions and both pinned declaration types elaborated and printed |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `rg -n '\b(sorry\|admit)\b\|^[[:space:]]*axiom\b' Stage1_Instances/THM-M-0314 -g '*.lean'` | 1 | expected no-match exit; no prohibited placeholder or axiom |
| `git diff --check -- Stage1_Instances/THM-M-0314` | 0 | no whitespace errors |

## Unblock condition and status boundary

Supply and independently inspect an immutable primary or authoritative source passage that fixes
the exact claim, including field, space hypotheses, ordered binders, self-adjointness convention,
decomposition encoding, zero eigenspace, multiplicity, convergence, and degenerate cases. The
statement node can then freeze that proposition, elaborate it, record an expression hash, add
checked transports, and mutation-test its boundary.

No canonical Lean target, statement receipt, proof credit, `H0`, `M0`, `R0`, audit completion, or
theorem completion is claimed. The assigned statement phase is not complete, so no root
`.stage1-worker-selftest.json` is written.
