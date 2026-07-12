# Exact-statement gate: blocked

Item: `S56-M-1123-STATEMENT`  
Base revision: `bce5c3a2691f71daf054f0f11b5cf66c120a7306`

## Decision

The exact Lean 4 target cannot be truthfully elaborated from the repository source record. The
record gives only the label "SLE and percolation", the year 2001, the names
Smirnov/Lawler/Schramm/Werner, and the gloss "the connection between SLE and critical
percolation". It supplies no edition, theorem number, or exact wording. The accepted intake
therefore freezes only a theorem family and explicitly leaves the exact source variant and formal
statement open.

Within that family, each of the following choices changes the proposition rather than merely its
Lean encoding:

- critical site percolation on the triangular lattice versus another site or bond model;
- the domain class, marked boundary points or prime ends, and discrete approximation rule;
- Dobrushin boundary colors, interface orientation, interpolation, and terminal convention;
- the metric and quotient used for curves modulo reparametrization;
- convergence in distribution of random curves versus weak convergence of their laws;
- a stopped or local result versus full convergence from one marked boundary point to the other;
- the normalization of chordal SLE and the convention identifying the parameter as `kappa = 6`.

The intake's primary lead, Smirnov, *Critical percolation in the plane: conformal invariance,
Cardy's formula, scaling limits* (2001), was recorded only as a discovery anchor. No immutable
edition was inspected theorem by theorem, and no exact locator, assumptions, corrections, or
independent source review were approved. The repository's four-name attribution also does not
uniquely select a result. Choosing a familiar SLE6 convergence formulation would therefore invent
missing mathematics and could silently strengthen a crossing-probability result, a stopped
interface theorem, or a domain-specific theorem.

The Stage0 record confirms that precise definitions, premises, proof process, dependencies,
foundations, and machine artifacts are all `待补充` (to be supplied). Its `已验证` metadata is
explicitly untrusted under rev-5.6. The repo-local search found no pre-existing Lean declaration
that could disambiguate the claim. A generic structure that assumes a percolation law converges to
SLE6 and then exposes that field would be a forbidden placeholder, not an elaboration of the
theorem.

Consequently the phase fails at exact human-claim identity, before ordered binders, minimal pinned
imports, an elaborated-expression fingerprint, checked transports, or meaningful mutation tests
can be established. Creating a `Statement.lean` file under these conditions would substitute an
arbitrary theorem for the assigned one.

## Required unblock

An accountable source reviewer must select an immutable primary edition and exact numbered theorem
or displayed result, verify errata, and freeze the lattice and critical measure, domain and marked
boundary data, boundary conditions, discrete approximations, exploration-curve representation,
curve topology, convergence mode, SLE normalization, hypotheses, quantifier order, and degenerate
cases. A later statement worker can then encode that claim, minimize pinned imports, print and hash
the elaborated expression, check any alternate encoding, and mutation-test proposition-changing
alterations.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The existing canonical `.lake` artifact was used
read-only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1123` | exit 0; rank 563, planned, `L0/rework_required`, legacy artifacts unaccepted, theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | exit 0; `651c8acc...b1d2` and `321626c8...2d81` |

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression fingerprint, checked transport, and mutation tests. The
assigned phase is therefore not self-tested or complete, and no `.stage1-worker-selftest.json` is
emitted. No theorem completion or downstream-node credit is claimed.
