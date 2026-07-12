# Statement-phase blocker

Item: `S56-M-1525-STATEMENT`

Base revision: `33a031b5238cc674b8e1073106bff2685c6bbbc4`

## Verdict

The exact Lean 4 target cannot yet be selected or elaborated without inventing mathematical
content that the repository source does not supply. The metadata source at
`Docs/researches/physics_theorems.md:8333` identifies the time-dependent Schrodinger equation only
by the formula

```text
i hbar partial_t psi = H psi
```

and says that it describes time evolution of a quantum state. This is an equation/law with free
semantic parameters, not a closed theorem. The more general record at
`Docs/researches/math_theorems.md:11136` says only "the fundamental equation of quantum mechanics."
Neither record fixes the state space, Hamiltonian representation and domain, time dependence,
regularity or derivative notion, value and positivity of `hbar`, initial datum, or whether the
claim is merely the equation, existence, uniqueness, unitary evolution, norm conservation, or
energy conservation.

The intake deliberately leaves those same choices open. In particular, its canonical claim is
conditional on "source-selected" self-adjointness, domain, initial-condition, and conservation
hypotheses, while `scope-map.md` assigns selection of those data to this phase. No exact primary
statement has since been added. Therefore there is no authoritative proposition against which a
Lean expression, ordered binders, mutation tests, or checked transports could be certified.

The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_193.lean` cannot resolve the identity
gate. It models the Hamiltonian as a bounded continuous linear map, packages the derivative in an
interface, and assumes unitary generation and spectral compatibility as bare proposition fields.
Its own module documentation says `StatementShape` is only a proposition-level boundary, not the
terminal Schrodinger theorem. Adopting it would silently substitute a bounded contract for the
intake's expected densely defined self-adjoint Hamiltonian. Conversely, selecting Stone's theorem,
a PDE well-posedness theorem, or a tautological restatement of a newly defined equation would
broaden or replace the source claim.

Accordingly, this node emits no `.lean` target, expression fingerprint, import-minimality claim,
statement receipt, or worker self-test manifest. The intake remains `M4`; no proof or theorem
completion is claimed. Its prerequisite intake is also only worker-provisional (`[_]`) and has not
received the required master acceptance.

## First failed gate and retry condition

The first failed gate is rev-5.6 exact-statement identity. Retry after the source/intake authority
selects one closed theorem and freezes all of the following:

1. an exact primary-source locator (edition or stable scan, theorem/equation and page, and errata);
2. autonomous versus time-dependent Hamiltonian and bounded versus unbounded representation;
3. the complex Hilbert space, operator domain, density/self-adjointness and domain-invariance rules;
4. strong/weak derivative and solution regularity, units and the precise value/range of `hbar`;
5. binder order, initial datum, existence/uniqueness strength, and each conservation conclusion;
6. zero space, zero Hamiltonian, zero initial state, and initial data outside the operator domain.

After that decision, the narrow retry is to encode the selected proposition under this owned
directory, identify the smallest pinned mathlib import (the current pinned tree does contain
`Mathlib.Analysis.InnerProductSpace.LinearPMap` support for unbounded self-adjoint operators), run
`lake env lean` from `Formalizations/Lean`, fingerprint the explicit elaborated expression, and
mutation-test the frozen hypotheses and boundary policy.

## Validation record

All commands ran in this worker clone. The Lean check below validates only the discoverability and
current elaboration of the rejected legacy candidate; it is not elaboration evidence for an exact
rev-5.6 target.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1525` | 0 | rank 193; lifecycle `planned`; L0/rework-required; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -C 15 '薛定谔方程' Docs/researches Docs --glob '*.md' --glob '*.json'` | 0 | located the formula-only source record and the less-specific duplicate record |
| `rg -n 'IsSelfAdjoint' Formalizations/Lean/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace` | 0 | pinned mathlib exposes both bounded and `LinearPMap` self-adjoint APIs, but no source choice selects a target |
| `lake env lean --version` (cwd `Formalizations/Lean`) | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `lake env lean AwesomeTheorems/Stage1/S1_M_193.lean` (cwd `Formalizations/Lean`) | 0 | rejected historical statement and substrate wrappers elaborate in the pinned environment |
| `test ! -e .stage1-worker-selftest.json` | 0 | no self-test manifest existed before this blocked phase |

Master acceptance remains outstanding. This artifact does not edit the generated blueprint or task
DAG and does not claim the assigned statement node as self-tested.
