# Exact-statement gate: blocked

Item: `S56-M-1187-STATEMENT`  
Theorem: `THM-M-1187`  
Base revision: `8d12c8a5047e3d61ed7d598a80a7077501591a36`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. Its
entire mathematical statement is `热方程及其推广` ("the heat equation and its generalizations"),
under the topic label `抛物型方程` ("parabolic equations"). This describes a subject and a family
of equations, not a proposition with fixed hypotheses and a conclusion.

At minimum, inequivalent choices remain open for:

- the spatial domain, time interval, scalar field, and dimension;
- the operator, coefficients, ellipticity/parabolicity convention, and forcing term;
- initial and boundary data and their compatibility conditions;
- weak, mild, strong, or classical solution concepts and their function spaces;
- whether the conclusion is existence, uniqueness, regularity, stability, an estimate, or another
  qualitative property;
- the exact quantifier order, coefficient/data regularity, constants, endpoints, and degenerate
  cases.

The source supplies no primary edition, theorem/page, exact wording, or errata record that resolves
these choices. Stage0 explicitly marks the definitions, premises, proof, formal system, and machine
artifacts as `待补充` (to be supplied). The metadata value `已验证` is untrusted and gives neither
statement identity nor proof credit.

Choosing the classical heat equation, a generic uniformly parabolic equation, or any one
existence/uniqueness theorem would substitute invented mathematics. Choosing a maximum principle,
Schauder regularity theorem, or L-p estimate would additionally collide with separately indexed
targets `THM-M-1188`, `THM-M-1189`, and `THM-M-1190`. The older generated Stage1 gloss
`抛物型方程的正则性` is therefore discovery history only, not authority to replace this source
record.

Consequently the phase fails at canonical human-claim identity, before minimal imports, fixed
universes and binders, an elaborated expression fingerprint, checked transports, or meaningful
removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations can be established.
No Lean declaration, abstract interface that assumes a desired result, axiom, placeholder,
weakened special case, or broadened target was introduced. Machine state remains `M4`, statement
acceptance is false, and no downstream or theorem-completion credit is claimed.

## Pinned environment and narrow validation

Commands ran from this worker clone on 2026-07-12. The canonical `.lake` directory was inspected
through the existing worker symlink only; no update, build, clone, fetch, or other dependency
mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1187` | 0 | Rank 382, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `cd Formalizations/Lean && lake --version` | 0 | Lake `5.0.0-src+98dc76e` |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| repository `rg` search for the theorem ID, Chinese title, and exact source wording | 0 | Found only the underspecified source metadata, generated projections, intake record, and neighboring targets; no source-frozen proposition |
| pinned-mathlib `rg` search for heat/parabolic equations and heat kernels | 0 | No relevant PDE target; matches for "parabolic" were unrelated matrix/projective-line terminology |

There is no applicable `lake env lean <target>.lean` command: the required exact expression does
not exist. Elaborating a freely chosen proxy would be fake evidence rather than validation of the
assigned deliverable.

## Retry condition

An accountable source reviewer must select an immutable primary source and exact theorem/page,
resolve errata, and freeze all operator, domain, data, solution-space, hypothesis, conclusion,
constant, endpoint, and degenerate-case choices above. The selection must also document its
boundary from `THM-M-1188` through `THM-M-1190`. A later statement worker can then encode the exact
claim, minimize pinned imports, serialize and hash the elaborated expression and environment, and
run all four required mutation classes.

First failed gate: exact source-statement identity. Known failures are the canonical Lean target,
minimal-import determination, expression and environment fingerprints, checked transports, and
mutation tests. The assigned phase is not genuinely self-tested to completion, so no
`.stage1-worker-selftest.json` is emitted.
