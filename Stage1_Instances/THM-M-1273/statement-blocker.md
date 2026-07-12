# Exact-statement gate: blocked

Item: `S56-M-1273-STATEMENT`  
Theorem: `THM-M-1273`  
Base revision: `386fa86262872ab67bb9e32d2aa2877520af32a4`

## Decision

No exact Lean 4 target can be truthfully elaborated from the authoritative repository record. The
record supplies only the label "applications of Morse theory to PDE" and the gloss "topological
methods for variational problems". It supplies no primary source, theorem number, equation,
domain, boundary condition, variational functional, hypotheses, or conclusion. The accepted
intake therefore correctly records the canonical claim as unresolved.

The label describes a method family rather than a proposition. In particular, it does not select
among Morse inequalities for a functional, critical-group results, a Morse-index estimate, an
existence theorem, or a multiplicity theorem. Nor does it determine:

- the PDE, its domain and dimension, and its boundary or initial conditions;
- the solution and coefficient spaces, operator class, and weak or classical solution predicate;
- the energy functional and the bridge from its critical points to PDE solutions;
- differentiability, Palais-Smale or other compactness, isolation, and nondegeneracy assumptions;
- coefficient-ring and Morse-index or critical-group conventions; or
- the exact quantified existence, multiplicity, index, or inequality conclusion and its
  degenerate cases.

These choices alter the domains, binders, hypotheses, and conclusion. Choosing any familiar PDE
application, a finite-dimensional Morse theorem, or an abstract variational proxy would broaden,
narrow, or substitute the unidentified theorem. An abstract interface that assumes the desired
critical-point or PDE conclusion would likewise be fake statement evidence.

Consequently the statement gate fails before minimal imports, an elaborated expression
fingerprint, checked transports, or meaningful removed-hypothesis, changed-domain, binder-scope,
and boundary mutations can be produced. No Lean declaration, `sorry`, axiom, placeholder, or
substitute theorem was introduced. Machine state remains `M4`; statement acceptance, audit
completion, and theorem completion are false.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing `.lake` artifacts
were read only; no update, build, clone, or fetch command was used.

- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean 4.29.0, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Lake: `5.0.0-src+98dc76e`.
- Pinned mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- `lake-manifest.json` SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1273` | 0 | Rank 446, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean version and commit recorded above |
| `cd Formalizations/Lean && lake --version` | 0 | Lake version recorded above |
| `cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json` | 0 | Produced the two hashes recorded above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Produced the pinned mathlib revision recorded above |
| repository `rg` search for the Chinese label, English label, and inventory gloss | 0 | Found only generated inventory records and `Docs/researches/math_theorems.md`; no source-frozen proposition or theorem-specific Lean module |
| pinned-mathlib and repo-local Lean `rg` search for Morse theory, Morse index, critical groups, and Palais-Smale | 0 | Found unrelated Morse-polynomial/Morse-Sard material and generic or separately owned scaffolding; no exact PDE theorem selected by this record |

There is no applicable `lake env lean <target>.lean` command: the exact target required by the
assigned deliverable does not exist. Elaborating a made-up interface would not validate this node.

## Retry condition

An accountable source review must select an immutable primary-source edition and exact
theorem/page, resolve errata, and freeze every PDE, domain, boundary condition, function space,
functional, compactness condition, Morse convention, quantifier, conclusion, and degenerate case
listed above. A later statement run can then encode that exact claim, minimize its pinned imports,
serialize its elaborated expression, crosswalk it row by row to the source, and run all required
mutation tests.

The assigned phase is not genuinely self-tested to its completion gate, so no
`.stage1-worker-selftest.json` is emitted.
