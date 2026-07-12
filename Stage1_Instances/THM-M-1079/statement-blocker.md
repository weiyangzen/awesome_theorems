# Exact-statement gate: blocked

Item: `S56-M-1079-STATEMENT`  
Base revision: `ec625affaba626d33138848b34fb76da0bf247cf`

## Decision

The exact Lean 4 target cannot be truthfully selected from the repository source. The complete
entry in `Docs/researches/math_theorems.md` names "martingale difference sequence" and states only
"properties of martingale difference sequences" (`鞅差序列的性质`). `Docs/Stage0_Blueprint.md`
copies that phrase and explicitly leaves the definitions, hypotheses, proof, dependencies,
equivalent formulations, and formal artifact unspecified. Neither record identifies a source,
edition, result, page, formula, or particular property.

This ambiguity changes the proposition rather than merely its notation. At minimum it leaves open
whether the root is:

- the definition/one-step conditional-mean-zero condition;
- the theorem that partial sums of such differences form a martingale;
- the converse theorem that successive martingale increments have conditional mean zero;
- an orthogonality or variance identity requiring square integrability; or
- a convergence or concentration result requiring additional hypotheses.

It also leaves the codomain, probability or finite-measure assumptions, adaptation and
integrability hypotheses, filtration indexing convention, initial value, and empty-sum boundary
undetermined. These alternatives are not definitionally equal and are not interchangeable by an
unrecorded transport. Choosing the familiar partial-sum characterization would therefore invent a
theorem rather than elaborate the exact source claim. This phase fails at exact human-claim
identity, before minimal imports, binder order, an elaborated-expression hash, or statement
mutations can be accepted.

## Pinned Lean discovery boundary

The pinned mathlib snapshot does provide relevant vocabulary and candidates. In
`Mathlib/Probability/Martingale/Basic.lean`, `MeasureTheory.Martingale` is a strongly adapted
process satisfying all-time conditional-expectation equalities, and
`martingale_of_condExp_sub_eq_zero_nat` derives a martingale from integrability, adaptation, and
zero conditional expectations of successive increments. In
`Mathlib/Probability/Martingale/Centering.lean`, `martingalePart_eq_sum` expresses the martingale
part as a sum of centered increments and `martingale_martingalePart` proves that process is a
martingale.

Those declarations show that candidate formulations are expressible in the pinned Lean
environment. They do not select which candidate the vague repository phrase denotes, and none is
accepted here as the canonical target, an exact transport, or proof credit. Consequently no
`Statement.lean` is created: an elaborating candidate would not satisfy the assigned exact-target
deliverable.

## Required unblock

An accountable source review must pin an inspectable primary or authoritative source and record
the exact edition, theorem or definition number, page, wording, assumptions, convention, and
applicable errata. It must select the property and settle the codomain, measure-space assumptions,
filtration indices, adaptation/integrability conditions, almost-everywhere equality, and boundary
cases. A later statement run can then encode that exact proposition, minimize pinned imports,
print and hash the elaborated expression, check any alternate encoding by a typed transport, and
mutation-test its hypotheses, domains, binder scope, and boundaries.

## Narrow validation evidence

Commands were run in this worker clone on 2026-07-12 (Asia/Shanghai). Lean inspection used the
existing `.lake` link to canonical pinned artifacts. No dependency update, build, clone, or fetch
was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1079` | 0 | rank 521, planned, `L0/rework_required`, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n "def Martingale|martingale_of_condExp_sub_eq_zero_nat" Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Martingale/Basic.lean` | 0 | located the pinned definition at line 53 and candidate theorem at line 475 |
| `rg -n "martingalePart_eq_sum|martingale_martingalePart" Formalizations/Lean/.lake/packages/mathlib/Mathlib/Probability/Martingale/Centering.lean` | 0 | located candidate declarations at lines 73 and 87 (plus references) |
| `sha256sum Docs/researches/math_theorems.md Docs/Stage0_Blueprint.md Docs/Stage1_Targets_rev-5.6.json Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | source `bdde11af...a29`; Stage0 `ab92a43f...b65f`; target manifest `02eec284...ab2c`; toolchain `651c8acc...b1d2`; Lake manifest `321626c8...2d81` |
| `git diff --check -- Stage1_Instances/THM-M-1079` | 0 | no output |

First failed gate: exact source-statement identity. The root remains `[H1, M4, R3]`; no canonical
Lean expression, statement acceptance, audit completion, theorem completion, or downstream node
credit is claimed. Because the assigned statement phase is blocked rather than genuinely
self-tested to completion, no `.stage1-worker-selftest.json` is emitted.
