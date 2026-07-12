# Exact-statement gate: blocked

Item: `S56-M-1162-STATEMENT`  
Base revision: `5deb8c587c4f4bde14e6c99658fe76c173180019`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
entire mathematical wording is `基于边界积分的数值方法` ("a numerical method based on boundary
integrals"), under the label "boundary element method". This describes a family of methods rather
than a truth-valued proposition. In particular, it does not determine:

- a differential operator, domain, dimension, scalar field, boundary condition, or solution notion;
- a fundamental solution, layer potential, boundary integral operator, or integral formulation;
- trial and test spaces, a mesh family, quadrature, discrete system, or computed quantity;
- regularity, ellipticity, coercivity, inf-sup, uniqueness, or compatibility hypotheses;
- an existence, stability, consistency, convergence, or error-estimate conclusion;
- a norm, convergence rate, constant dependencies, or treatment of corners, nullspaces, and
  degenerate discretizations.

These choices yield inequivalent theorems. Selecting a Laplace, Helmholtz, elasticity, Galerkin,
collocation, or quadrature result would invent missing mathematics rather than elaborate the exact
repository target. `Docs/Stage0_Blueprint.md` confirms that the definitions, hypotheses, proof,
axioms, and machine artifacts are all open. The metadata value `已验证` is not a primary source or a
kernel receipt.

The intake dependency reaches the same fail-closed conclusion and records `[H4, M4, R4]`; it does
not freeze a proposition. Consequently this phase fails at canonical human-claim identity, before
minimal imports, an elaborated expression fingerprint, checked alternate encodings, or meaningful
removed-hypothesis/domain/binder-scope/boundary mutations can be defined. No `.lean` statement was
created, because any such declaration would be a broadened or substituted theorem.

## Repository search boundary

A scoped search of `Formalizations/` and `Docs/` found no legacy Lean declaration, formal module,
or source statement for `THM-M-1162` beyond the same metadata wording and generated scheduling
records. Thus there is not even an unaccepted legacy expression that could be checked as discovery
input. This negative search is not an anchor audit and does not claim that no external result
exists; it only establishes the local boundary relevant to this statement task.

## Required unblock

An accountable source reviewer must select a stable primary source by edition, theorem/page, and
exact wording. The review must freeze the model problem, operator and integral formulation, domain
and boundary regularity, boundary condition, solution and discrete spaces, mesh and stability
hypotheses, exact conclusion, norm and constant dependencies, and all endpoint or degenerate cases.
A later statement worker can then encode that claim without substitution, minimize the pinned
imports, serialize and hash its elaborated expression, and run the four required mutation classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. The existing pinned environment was only
queried; no `lake update`, build, dependency fetch, or mutation of `.lake` was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1162` | exit 0; rank 365, no legacy slot, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `rg -n -C 5 '边界元方法\|Boundary element method\|boundary element method\|THM-M-1162' Formalizations Docs --glob '!Docs/Stage1_Blueprint_rev-5.6.md' --glob '!Docs/Stage1_Execution_DAG_rev-5.6.json' --glob '!Docs/Stage1_Targets_rev-5.6.json' --glob '!Docs/Stage1_Blueprint_Applicable_Theorems.md' --glob '!Docs/Stage0_Blueprint.md' --glob '!Docs/researches/math_theorems.md'` | exit 1 with no output; after excluding known metadata and generated records, no Lean declaration or exact proposition was found |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted. No theorem completion or downstream-node credit is claimed.
