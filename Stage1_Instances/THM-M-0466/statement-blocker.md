# Exact-statement gate: blocked

Item: `S56-M-0466-STATEMENT`  
Base revision: `9a198a2d8ff0981d17df1c1b8d4b11e4babaf7ed`

## Decision

The intake freezes the human root as Raynaud's Manin-Mumford theorem: over an algebraically closed
field of characteristic zero, a closed subvariety of an abelian variety whose torsion points are
Zariski dense is a finite union of translates of abelian subvarieties by torsion points. That exact
claim cannot yet be represented, and therefore cannot be elaborated, in the repository's pinned
Lean environment without inventing an unverified proxy API.

The only pinned mathlib file mentioning abelian varieties is
`Mathlib.AlgebraicGeometry.Group.Abelian`. Despite its title, it does not define an abelian-variety
object. Its exported main theorem says that a proper geometrically integral group scheme over a
field is commutative. The pinned tree has no `AbelianVariety` structure or predicate and the search
found no Manin-Mumford declaration. More importantly, the available surface does not provide the
combined vocabulary needed by the frozen conclusion: closed abelian subvarieties of such a group
scheme, their pointwise translates by rational/geometric torsion points, and equality with a
finite union of those translates.

`IsOfFinOrder` does elaborate for elements of an ordinary Lean `Monoid`. This does not bridge the
gap: a categorical `GrpObj` over `Spec k` is not, merely by importing these modules, an ordinary
monoid of the geometric points required by the theorem. Declaring abstract predicates called
`IsAbelianVariety`, `IsClosedSubvariety`, or `IsTorsionTranslate`, or quantifying over unconstrained
surrogates for them, would only elaborate a broadened interface theorem. It would not elaborate the
source claim and is forbidden by the exact-statement gate.

`StatementSurfaceProbe.lean` is deliberately not a canonical target. It contains only `#check`
commands for the real pinned declarations at this boundary. It introduces no theorem, axiom,
placeholder, or proof and gives no machine-proof credit.

## First failed gate

The first failure is canonical Lean representability against the pinned dependency closure. Since
the root's ambient object and conclusion cannot be expressed with identified definitions, there is
no exact elaborated expression to hash and no truthful minimal-import result. Checked transports,
hypothesis/domain/binder mutations, and boundary tests would all depend on first choosing or
implementing the missing mathematical API, so none is claimed.

The machine axis remains `M4`. The intake lifecycle remains `planned`; `statement_elaborated=false`,
`audit_complete=false`, and `theorem_complete=false`.

## Required unblock

Provide, at an immutable revision, a Lean 4 development defining abelian varieties, closed
subvarieties, geometric/rational points and torsion, abelian subvarieties, translations, finite
unions, and the relevant Zariski-density semantics, with a checked crosswalk to the frozen human
claim. Alternatively, implement and separately validate that foundational API in prerequisite
nodes before retrying this statement. A later statement run must then select the exact definitions,
freeze the scheme-versus-variety and equality-versus-containment conventions, minimize imports,
print and hash the expression, check transports, and mutation-test all material assumptions and
degenerate cases.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. Lean commands used the existing `.lake` symlink to
the canonical pinned artifacts read-only. No update, build, clone, or fetch was run.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0466` | 0 | rank 312; planned; legacy artifacts unaccepted; theorem incomplete |
| `rg -n -i 'abelian.?variet\|Manin.?Mumford\|torsion.*Zariski\|Zariski.*torsion' Formalizations/Lean/.lake/packages/mathlib/Mathlib` | 0 | sole relevant hit is the title of `AlgebraicGeometry/Group/Abelian.lean`; no target declaration |
| `rg -n 'structure Abelian\|def Abelian\|abbrev Abelian\|class Abelian' Formalizations/Lean/.lake/packages/mathlib/Mathlib/AlgebraicGeometry` | 1 | no abelian-variety definition found |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-0466/StatementSurfaceProbe.lean` | 0 | printed the proper/geometrically-integral group-scheme theorem and boundary types; probe elaborated with no errors |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json ../../Stage1_Instances/THM-M-0466/StatementSurfaceProbe.lean` | 0 | `651c8a...b1d2`, `321626...2d81`, and `f4ce15...b168` |

The assigned phase is not complete, so no `.stage1-worker-selftest.json` is emitted and no
downstream-node or theorem-completion credit is claimed.
