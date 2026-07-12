# Exact-statement gate: blocked

Item: `S56-M-1121-STATEMENT`  
Theorem: `THM-M-1121`  
Base revision: `4b371df18255c744c75b2aa9dbfaa4ebfd983dbf`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository record. The record
contains only the title "Smirnov theorem", the year 2001, and the gloss "conformal invariance of
triangular-lattice percolation". It gives no theorem number, page, exact wording, or immutable
source edition. The accepted intake therefore freezes a theorem family while explicitly leaving
the source variant and formal statement open.

The intake's primary candidate, Smirnov's *Critical percolation in the plane: conformal invariance,
Cardy's formula, scaling limits*, is recorded only as a discovery anchor. It has not been inspected
theorem by theorem or approved by an accountable source reviewer. Its title covers several
non-equivalent claims. The repository metadata does not decide among a crossing-probability limit,
Cardy's explicit formula, conformal covariance for a family of observables, an exploration-path
statement, or a stronger scaling-limit formulation.

Even after selecting the crossing formulation, each of the following unresolved choices changes
the proposition rather than merely its Lean encoding:

- triangular-lattice vertices versus the dual hexagonal-face presentation, including lattice
  orientation and mesh normalization;
- the exact critical product probability space and coloring convention;
- the planar domain class and boundary regularity, and whether marked data are boundary points,
  prime ends, or arcs;
- the discrete-domain and boundary-mark approximation hypotheses and exact crossing event;
- the conformal normalization and explicit Cardy function;
- pointwise versus uniform convergence, permitted mesh sequences, and quantifier order;
- treatment of coincident markings, nonsimple boundaries, and disconnected approximations.

Choosing familiar values for these fields would invent missing mathematics. An abstract structure
which assumes the desired limit or conformal invariance and then projects it would be a prohibited
placeholder, not an elaboration of Smirnov's theorem. A weaker finite-mesh symmetry or a stronger
full-interface scaling limit would likewise substitute a different theorem.

The exact human claim therefore fails before ordered Lean binders, minimal imports, an elaborated
expression fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain,
binder-scope, and boundary mutation tests can be established. No Lean source, axiom, placeholder,
or substituted theorem was introduced. Machine state remains `M4`; statement acceptance, audit
completion, and theorem completion are false.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The existing canonical `.lake` link was used
read-only. No update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1121` | 0 | rank 561, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository search for `Smirnov`, the English gloss, and the candidate paper | 0 | found underspecified metadata, this intake dossier, and related separately owned targets; no source-frozen proposition or Lean declaration |
| pinned-mathlib search for percolation, Cardy, Smirnov, triangular/hexagonal lattices, and crossing probabilities | 1 | no matching theorem-specific API (`rg` exit 1 means no match) |

There is no applicable `lake env lean <target>.lean` check because the repository does not identify
an exact expression to elaborate. Creating an arbitrary interface merely to obtain exit 0 would be
fake statement evidence.

## Required unblock

An accountable source reviewer must select an immutable primary edition and exact theorem or
displayed result, inspect its definitions and errata, and freeze every model, domain, boundary,
discretization, event, conformal-normalization, convergence, quantifier, and degenerate-case choice
listed above. The review must also distinguish this target from the separately scheduled Cardy
formula and SLE/percolation targets. A later statement worker can then encode that exact claim,
minimize pinned imports, fingerprint the elaborated expression, add checked transports, and run
structural mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
