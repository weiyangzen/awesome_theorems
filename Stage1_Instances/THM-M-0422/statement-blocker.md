# Statement gate blocker

Item: `S56-M-0422-STATEMENT`  
Theorem: `THM-M-0422`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The accepted intake scope is the compound global class field theory claim: global reciprocity for
every finite abelian extension `L/K`, including the Artin-map norm kernel and quotient isomorphism,
together with the existence and inclusion-reversing classification of finite abelian extensions by
open finite-index subgroups of the idele class group. The pinned Lean dependency closure does not
provide the objects and maps needed to express that claim faithfully. In particular, no concrete
global Artin map, idele norm map, norm subgroup, maximal abelian extension, or class-field
correspondence was found.

The historical discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_077.lean` elaborates, but it is not an exact target.
It defines `ClassFieldReciprocityData` with an arbitrary type `Extension`, an arbitrary map from it
to finite abelian extension packages, and an arbitrary `reciprocityKernel`. Its `StatementShape`
then asserts that this user-supplied map is bijective. It neither constructs nor characterizes the
global Artin map, does not state its norm kernel or quotient isomorphism, and does not identify the
classified extensions inside a fixed algebraic closure. The file itself calls this an abstract
boundary and a statement-shape candidate. Crediting it would substitute an abstract interface for
global class field theory.

There is also a concrete object-model defect in that discovery module: it takes ideles to be all
units of mathlib's adele ring with its induced unit topology. Pinned mathlib explicitly notes that
the idele topology is not the induced topology from the adeles. Therefore its quotient topology
cannot silently serve as the canonical topological idele class group needed for the open-subgroup
existence theorem.

Under rev-5.6 sections 2 and 5, missing source-faithful types and unresolved topology conventions
are hard statement blockers. Ordered binders, a normalized exact expression, its hash, checked
alternate transports, and meaningful removed-hypothesis/domain/scope/boundary mutations cannot be
truthfully supplied. The machine state remains `M4`. No unproved declaration, opaque proxy
predicate, abstract witness supplied by the caller, or weaker class-group theorem was introduced.

## Current rev-5.6 handoff

This blocker was rechecked at repository base
`778c2db4855d48868391ea236f702e592067e798` on 2026-07-17 (Asia/Shanghai).
The target-owned structured statement record, boundary probe, empty dependency-reuse ledger,
node receipt, and semantic validator now bind that base. `Statement.lean` elaborates with
`lake env lean --trust=0`; `check_statement.py` returns
`phase_accepted=false` and the first failed gate
`S02-EXACT-TARGET.missing_source_faithful_lean_objects`. The older 2026-07-12 evidence below is
retained only as discovery history and is not the current receipt.

## Historical environment fingerprint

- Repository base revision: `2667c596819609e46936f6b65b03aef6de2db783`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone using only the existing canonical pinned `.lake` artifacts.
No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_077.lean` | 0 | Historical abstract interface and supporting anchors elaborated; no exact terminal target was produced |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `rg -n -i 'GlobalClassField\|global class field\|ArtinReciprocity\|global reciprocity\|IdeleClassGroup\|ray class field' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | No matching global class field theory declaration or concrete idele-class API in pinned mathlib; exit 1 means no matches |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0422` | 0 | Rank 77, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |

## Retry condition

Provide pinned concrete Lean definitions for the correctly topologized idele and idele class
groups, idele norms for finite extensions, global Artin maps, Galois groups in a fixed algebraic
closure, and the finite-abelian-extension/open-subgroup correspondence. Freeze the reciprocity
normalization, quotient topology, equality-versus-isomorphism convention, and inclusion reversal.
The next statement run can then elaborate the intake's reciprocity and existence components as one
source-faithful target, serialize the expression, check alternate formulations, and mutation-test
abelianity, finiteness, openness/index, norm direction, binder scope, and trivial extensions.

Until those conditions are met, statement acceptance and theorem completion are false. At the
historical 2026-07-12 run, no `.stage1-worker-selftest.json` was emitted. The current 2026-07-17
packet described above self-tests this negative boundary only; it does not satisfy or claim the
positive statement completion gate.
