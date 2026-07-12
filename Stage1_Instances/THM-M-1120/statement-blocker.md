# Exact-statement gate: blocked

Item: `S56-M-1120-STATEMENT`  
Theorem: `THM-M-1120`  
Base revision: `afd1ece847556e46e5b7fbed9cb6428864dcb6ae`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the title "Cardy formula", the year 1992, and the gloss "crossing probability
for percolation". The intake therefore freezes a theorem family, not a unique proposition, and
explicitly leaves the rigorous source variant and canonical formal target open.

The original Cardy paper and the two Smirnov papers listed in the intake are discovery citations,
not immutable, pinpoint-reviewed source statements. In particular, Cardy's 1992 physics derivation
is not interchangeable with Smirnov's later rigorous triangular-lattice convergence theorem.
Selecting a familiar formulation from memory would invent the missing source boundary.

The unresolved choices are proposition-changing:

- site versus bond percolation, the triangular/hexagonal lattice representation, critical
  parameter, independence law, and boundary-color convention;
- the class and regularity of simply connected domains, whether marked data are boundary points
  or prime ends, their cyclic order, and accessibility assumptions;
- the discrete-domain approximation, mesh parameter, crossing event and its oriented source and
  target arcs, and endpoint-contact policy;
- the convergence filter, probability normalization, and quantifier order over domains,
  approximations, and mesh;
- the conformal normalization and whether the conclusion uses a triangle coordinate or the
  hypergeometric cross-ratio formula, including branches and constants;
- whether conformal invariance is a separate conclusion or only a consequence of the selected
  explicit limit formula.

These choices determine the types, ordered binders, hypotheses, conclusion, and boundary cases.
An abstract structure carrying an assumed crossing probability or assumed scaling limit would make
the result tautological. A finite-mesh identity, rectangle specialization, arbitrary-model
universality claim, or opaque `CardyFunction` would weaken, broaden, or hide the requested theorem.
None is valid statement evidence.

The prerequisite intake node is only provisionally marked `[_]` in the generated projection and
has not received master acceptance. Independently, exact human-claim identity already fails, so
minimal imports, an elaborated kernel expression and hash, checked transports, and meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary mutation tests cannot be produced.
Machine debt remains `M4`; statement acceptance and theorem completion are false.

## Required unblock

An accountable source reviewer must select an immutable primary edition and an exact theorem or
displayed statement, check errata, and freeze every model, domain, marked-boundary, approximation,
event, convergence, and normalization choice above. The review must distinguish Cardy's prediction
from the rigorous result receiving statement credit. After the intake receipt is master-accepted, a
later statement run can encode that exact claim, minimize pinned imports, serialize and hash its
elaborated expression, compile any claimed transports, and run structural mutations.

## Narrow validation evidence

Commands ran in this worker clone on 2026-07-12. The automation-provided `.lake` symlink was used
read-only; no update, build, clone, fetch, or dependency mutation was performed.

| Command | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `ok`: 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | `ok`: 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1120` | 0 | rank 560; planned; `L0/rework_required`; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Release |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for Cardy's formula, critical percolation, and crossing probability outside this dossier | 0 | only an unrelated maximal-inequality note; no source-frozen proposition or Lean declaration for this target |
| pinned-mathlib `rg` search for Cardy, percolation, and crossing probability | 1 | no matching theorem-specific API (`rg` exit 1 is the expected no-match result) |

There is no applicable `lake env lean <target>.lean` check because an exact target expression does
not exist. Elaborating an invented interface would be a fake result rather than the assigned
deliverable. First failed gate: exact source-statement identity. Known failures are prerequisite
master acceptance, canonical target, minimal-import determination, expression fingerprint,
checked transports, and mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted. No downstream-node or theorem-completion credit is
claimed.
