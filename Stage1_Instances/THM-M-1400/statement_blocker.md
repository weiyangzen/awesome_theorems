# Exact-statement gate: blocked

Item: `S56-M-1400-STATEMENT`  
Base revision: `a379e5a45829099a04e92cce109f4ac3568d02c0`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
manifest wording is only `二维系统的极限集` ("limit sets of two-dimensional systems"). A second
repo-local discovery record says that bounded orbits of a two-dimensional continuous dynamical
system tend to a fixed point or a periodic orbit, but gives no source edition, theorem locator, or
definitions. These descriptions do not determine a single Poincare-Bendixson proposition. In
particular, they leave open:

- whether the dynamics is a `C^1` autonomous vector field, a generated local flow, or an arbitrary
  continuous flow;
- whether the phase space is the plane, an open planar domain, or a two-manifold;
- whether boundedness means precompactness of one forward orbit or containment in a specified
  compact positively invariant set, and which existence interval is assumed;
- whether the conclusion concerns convergence of the trajectory, equality of its omega-limit set
  with a periodic orbit, or a classification of that omega-limit set;
- whether equilibria are excluded, merely finite, or form a separate conclusion branch; and
- whether stationary trajectories, empty limit sets, nonconstant periodicity, minimal periods, and
  equilibrium connections are admitted.

These choices yield inequivalent theorems. For example, the standard no-equilibrium form concludes
that a nonempty compact omega-limit set is a periodic orbit, while broader variants permit
equilibria and connecting-orbit graphs. The repo wording "tends to a fixed point or periodic orbit"
is not by itself enough to choose either formulation and may be stronger than the usual omega-limit
statement. Selecting one from memory would substitute mathematics rather than elaborate the exact
source target.

The accepted intake material deliberately records `canonical_statement: null`, machine state
`M4`, and `blocked_pending_exact_primary_source_statement`. It therefore supplies no canonical
human claim from which ordered binders, hypotheses, a conclusion, or structural mutations can be
derived. This statement phase fails at canonical claim identity, before minimal-import selection,
expression serialization, checked transports, or meaningful removed-hypothesis/domain/binder/
boundary mutation tests.

## Legacy Lean boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_297.lean` was inspected and elaborated only as
legacy discovery input. It packages a `C^1` vector field, a global `Flow`, an integral-curve field,
a compact trapping region, omega-limit assumptions, and two unconstrained `Prop` fields. Its
conclusion has an equilibrium branch, a periodic-range branch, and a purported finite graph branch.
The last branch is represented only by a finite set of vertices contained in the omega-limit set;
it encodes no connecting orbits or graph structure. The file itself calls `StatementShape` a
formalization boundary and explicitly says it does not prove Poincare-Bendixson.

Consequently that declaration is neither a source-crosswalked exact claim nor a permissible proxy
for one. Its five direct mathlib imports are not evidence of the minimal imports for an exact target.
Its successful elaboration establishes only that this historical abstract boundary remains
type-correct in the pinned environment; it earns no rev-5.6 statement or proof credit.

## Required unblock

An accountable source reviewer must identify a stable primary source by edition, theorem/page, and
exact wording, then freeze the phase space, vector-field regularity, solution/flow and time domain,
orbit compactness hypothesis, omega-limit definition, equilibrium hypothesis or alternative,
periodic-orbit convention, exact conclusion, and all degenerate cases. A later statement worker can
then encode that chosen claim without strengthening or weakening it, minimize pinned imports, print
and hash the elaborated expression, compile any credited transports, and run all four required
mutation classes.

## Narrow validation evidence

Commands were run from this worker clone on 2026-07-12. Lean used only the existing canonical pinned
`.lake` artifacts. No update, build, dependency fetch, clone, or `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1400` | 0 | rank 297, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_297.lean` | 0 | the legacy abstract boundary elaborated and printed its declarations; this is not exact-statement evidence |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_297.lean` | 0 | SHA-256 values `651c8acc...b1d2`, `321626c8...2d81`, and `5c60b8d6...af67` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transports, and mutation tests. The
assigned phase is not self-tested or complete, so no `.stage1-worker-selftest.json` is emitted. No
theorem completion or downstream-node credit is claimed.
