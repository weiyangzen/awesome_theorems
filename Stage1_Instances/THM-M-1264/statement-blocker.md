# Exact-statement gate: blocked

Item: `S56-M-1264-STATEMENT`  
Theorem: `THM-M-1264`  
Base revision: `58cde546113e54bfa95299c69db6ee1508316872`

## Decision

No exact Lean 4 target can be truthfully elaborated from the repository source. The entire claim is
`PDE的变分方法` ("variational methods for PDE"), with the title `变分法与PDE`. This is a subject
label rather than a truth-valued proposition. In particular, it does not determine:

- a domain, unknown, scalar field, or function space;
- a PDE/operator, coefficients, data, or boundary conditions;
- a functional and the relation between its critical points or minimizers and the PDE;
- differentiability, coercivity, convexity, semicontinuity, compactness, or regularity hypotheses;
- an existence, uniqueness, regularity, minimization, or Euler-Lagrange conclusion;
- quantifier order, excluded degenerate cases, or an attributable theorem-bearing source.

These omissions cannot be repaired as notation choices. For example, an Euler-Lagrange
equivalence, a direct-method existence theorem, a weak solution theorem for an elliptic boundary
value problem, and a minimax critical-point theorem have different objects, hypotheses, and
conclusions. Choosing any one of them would substitute a new theorem for the assigned source
record. The separately scheduled `THM-M-1265` (direct method) also makes adopting that result here
an especially clear target-boundary violation.

The intake record therefore correctly leaves `canonical_statement`, domain, binders, hypotheses,
conclusion, Lean module, and declaration/expression null. Without a canonical human proposition,
there is no legitimate expression for Lean to elaborate, no minimal import set to establish, no
normalized expression hash, no alternate-form transport, and no meaningful removed-hypothesis,
changed-domain, changed-binder-scope, or boundary-case mutations. Creating an abstract predicate or
assuming the desired PDE result would be fake statement evidence. No Lean declaration, axiom,
placeholder, weakened case, or broadened theorem was introduced. Machine state remains `M4`, and
the statement node is not complete.

## Pinned environment and validation

Commands ran in this worker clone on 2026-07-12 (Asia/Shanghai). The existing canonical `.lake`
artifacts were read only; no update, build, clone, or fetch command was used.

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
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 1546 uniform-L0 Lean 4 targets, and the execution skill passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1264` | 0 | rank 441, planned, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | produced the pinned Lean version and commit above |
| `cd Formalizations/Lean && lake --version` | 0 | produced the Lake version above |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | produced the two hashes above |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | produced the pinned mathlib revision above |
| repository `rg` search for `变分法与PDE` and `PDE的变分方法` | 0 | found only the same topic metadata and generated projections; no exact proposition or source citation |

There is no applicable `lake env lean <target>.lean` run: the exact expression required by section
5.1 does not exist. The Lean version command is environment evidence only and receives no
elaboration or theorem credit.

## Retry condition

An accountable source decision must provide an immutable primary-source edition and exact
theorem/page, including every domain, function-space, PDE, boundary, functional, hypothesis,
quantifier, conclusion, and degenerate-case convention. It must distinguish the root from the
separately queued direct-method and related variational-analysis targets. A later statement run can
then encode that exact claim, minimize its pinned imports, serialize the elaborated expression and
environment fingerprint, check alternate transports, and run all four required mutation classes.

First failed gate: exact human statement identification under sections 5 and 5.1. The remaining
root cut set begins with authoritative statement recovery. This artifact claims neither statement
acceptance nor theorem completion. Because the assigned phase cannot be genuinely self-tested to
its completion gate, no `.stage1-worker-selftest.json` is emitted.
