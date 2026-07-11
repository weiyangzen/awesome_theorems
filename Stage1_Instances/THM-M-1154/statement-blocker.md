# Statement gate blocker

Item: `S56-M-1154-STATEMENT`  
Theorem: `THM-M-1154`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record identifies only "regular boundary points" and glosses the claim as
"existence of a solution to the Dirichlet problem". It cites no source, theorem, or page and does
not fix the domain, dimension, operator, boundary-data class, solution notion, regularity
definition, or local-versus-global quantifier scope. In particular, it does not decide between:

- boundary convergence of a Perron solution at one regular point;
- solvability for every continuous boundary datum when every boundary point is regular; or
- a barrier characterization or another equivalent regularity theorem.

These are related but different propositions with different binders and assumptions. Selecting
one would invent the missing mathematics rather than elaborate the exact catalogue claim. The
intake therefore correctly records the exact human and formal statement as open. Under sections 5
and 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md`, statement ambiguity and a missing exact expression
fingerprint are hard blockers.

The legacy discovery module
`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_144.lean` cannot repair the source-identity
failure. Its `StatementShape` quantifies over an unconstrained proposition named
`admissibleDomain`; its `RegularBoundaryPointData` contains proposition-valued
`hasBarrier` and `perronConvergesToBoundaryValue` fields. The later barrier surface likewise leaves
the boundary-limit, separation, and superharmonic requirements as unconstrained `Prop` fields.
The module explicitly labels these objects as statement shapes and formalization debt. Although it
elaborates, it is an abstract interface that can be inhabited without defining the classical
potential-theoretic conditions, so it receives no exact-statement or proof credit.

Consequently the ordered binders, exact hypotheses, conclusion, normalized kernel expression,
expression hash, minimal imports, checked alternate transports, and meaningful removed-hypothesis,
domain, binder-scope, and boundary-case mutations cannot truthfully be supplied. Machine status
remains `M4`. No `sorry`, axiom, placeholder declaration, abstract proxy target, disk-only
substitute, or weakened Sobolev theorem was introduced.

## Environment fingerprint

- Repository base revision: `2ee637ed8d67dca4a6ad2a70053fe8bd6955c5d3`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.
- Legacy discovery module SHA-256:
  `8dbb2044e722235c30c5611422f9754faa9e3a6b88526d866f7401caaed90b61`.

## Narrow validation evidence

Commands ran from this worker clone using only the existing canonical pinned `.lake` artifacts.
No update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1154` | 0 | Rank 144, planned, L0/rework-required, legacy artifacts unaccepted, theorem incomplete |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | Checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `cd Formalizations/Lean && lake env lean AwesomeTheorems/Stage1/S1_M_144.lean` | 0 | Legacy abstract interface elaborated; output confirms `StatementShape`, proposition-valued boundary packages, adjacent Poisson anchors, and explicit no-completion gates |

## Retry condition

An accountable source reviewer must provide an immutable primary-source theorem/page and freeze
whether the root is local boundary convergence, global Dirichlet solvability, or an equivalence.
That decision must also fix the Euclidean dimension and domain assumptions, Laplacian/operator,
boundary-data topology, Perron or other solution construction, regularity definition, convergence
mode, uniqueness, and degenerate cases. The next statement worker can then encode the
source-faithful proposition, minimize its pinned imports, serialize its expression and environment,
and run the four required mutation classes.

Until then, statement acceptance, audit completion, and theorem completion are false. Because the
assigned phase is not self-tested to its completion gate, no `.stage1-worker-selftest.json` is
emitted.
