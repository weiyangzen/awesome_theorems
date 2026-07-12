# Exact-statement gate: blocked

Item: `S56-M-0326-STATEMENT`  
Theorem: `THM-M-0326`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The intake's human root is “every nuclear locally convex topological vector space over the real or
complex scalars has the approximation property,” where approximation means compact-convergence of
finite-rank continuous endomorphisms to the identity. The repository does not yet supply the source
pinpoint needed to determine the exact separation and completeness assumptions or scalar
conventions. More decisively for this phase, pinned mathlib has no definition of Grothendieck
nuclearity for locally convex spaces and no canonical approximation-property predicate. Therefore
there is no source-faithful Lean proposition to elaborate and fingerprint.

The legacy declaration
`AwesomeTheorems.Stage1.S1_M_215.StatementShape` does not repair this failure. It quantifies over a
**complete normed** space and assumes the custom `NuclearNormedSpace`, defined as an explicit
summable rank-one decomposition of the identity. Its hypotheses structure also carries an arbitrary
proposition named `approximationTopologyCompatible` together with a proof of that proposition.
Those choices are not a checked encoding of general nuclear locally convex spaces and add a Banach
space restriction absent from the intake claim. Treating that declaration as canonical would
substitute a normed surrogate for the requested theorem, which rev-5.6 forbids.

`StatementProbe.lean` checks the closest independent substrate types using only
`Mathlib.Topology.Algebra.Module.LocallyConvex` and
`Mathlib.Topology.Algebra.Module.StrongTopology`: `LocallyConvexSpace`, `CompactConvergenceCLM`,
and the compact/uniform-convergence characterization elaborate. This does not connect nuclearity to
the approximation property and receives no statement or proof credit.

Consequently the ordered canonical binders and assumptions, normalized target expression,
expression hash, checked transports, and meaningful removed-hypothesis/domain/scope/boundary
mutations cannot truthfully be produced. The exact-statement state remains `M4`. No `sorry`, axiom,
opaque proxy predicate, placeholder, legacy surrogate, or finite-dimensional substitute was added.

## Environment fingerprint

- Repository base revision: `388f85443db876842b04fb42b0e5a952f22f66d9`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `98d468bc8a786f8416a7a7b5d0933e4fe20a15a4605627b786b41fe6a2a15113`.

## Validation evidence

Commands ran in this worker clone using only the existing pinned `.lake` artifacts. No update,
build, clone, or fetch command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0326/StatementProbe.lean` | 0 | `LocallyConvexSpace`, `CompactConvergenceCLM`, and `UniformConvergenceCLM.tendsto_iff_tendstoUniformlyOn` elaborated |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_215.lean` | 0 | Legacy normed surrogate elaborated; its printed `StatementShape` is only a `Prop` name and its supporting declarations expose the custom boundary described above |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'NuclearSpace\|nuclear space\|ApproximationProperty\|approximation property\|Grothendieck.*approxim' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 0 | Only an unrelated prose occurrence of “linear approximation property”; no matching nuclear-space or approximation-property declaration |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0326` | 0 | Rank 215, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

Supply an immutable primary-source theorem/page and assumptions, then add or pin a Lean object model
for Grothendieck nuclear locally convex spaces and its finite-rank compact-convergence approximation
property. The next statement run can then freeze the exact real/complex binders, separation and
completeness conditions, elaborate and serialize the target, and execute the required mutations.

Until those conditions hold, statement acceptance and theorem completion are false. Because the
assigned phase is not self-tested to its completion gate, no `.stage1-worker-selftest.json` is
emitted.
