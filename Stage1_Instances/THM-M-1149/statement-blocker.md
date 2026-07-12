# Statement gate blocker

Item: `S56-M-1149-STATEMENT`  
Theorem: `THM-M-1149`  
Verdict: blocked; no exact canonical Lean target is claimed.

## First failed gate

The repository source record gives only the title "Dirichlet problem" and the gloss "the
boundary-value problem for Laplace's equation." It does not state a proposition. In particular, it
does not select any of the materially different claims commonly associated with that problem:

- existence, uniqueness, regularity, boundary convergence, or a representation formula;
- a disk, a smooth bounded domain, a Lipschitz domain, or a general domain with regular boundary
  points;
- a classical harmonic solution, a weak Sobolev solution, or a Perron solution;
- continuous pointwise boundary data, trace data, or data in another function space.

It also supplies no primary source, edition, theorem/page, hypotheses, definitions, or errata.
Connectedness, dimension, boundedness, boundary regularity, compatibility, and degenerate cases are
therefore unresolved. Choosing a standard modern existence-and-uniqueness theorem, or reusing the
neighboring disk Poisson-formula target `THM-M-1148`, would invent scope and substitute a different
theorem. The untrusted metadata label `已验证` cannot select that scope.

The pinned mathlib source search found Poisson-kernel and planar harmonic-analysis infrastructure,
but no declaration described as a general Dirichlet boundary-value theorem. That adjacent API
cannot repair the missing human claim. Under rev-5.6 sections 2 and 5, statement ambiguity and the
absence of an elaborated expression fingerprint are hard blockers.

Consequently the ordered binders, hypotheses, conclusion, minimal imports, serialized expression,
checked alternate transports, and meaningful removed-hypothesis, changed-domain, changed-binder-
scope, and boundary-case mutations cannot truthfully be produced. No `Statement.lean` is created:
an abstract solution predicate or caller-supplied proposition would be a proxy placeholder rather
than the exact target. The machine state remains `M4`, and no `sorry`, axiom, placeholder, proof
claim, or theorem-completion claim is introduced.

## Environment fingerprint

- Repository base revision: `3727de2a4ceed9cd590d437f2e2e51c1a2e7c172`.
- Validation date: 2026-07-12 (Asia/Shanghai).
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- Checked mathlib revision: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.
- `lean-toolchain` SHA-256:
  `651c8accb402b0c071cd336e9d3dc0a55516b1bfb434ddc4801f14936785b1d2`.
- Lake manifest SHA-256:
  `321626c846f14bcae3019c2fa6fb25a8fe879c21094d22bf30badb3335cb2d81`.

## Validation evidence

Commands ran from this worker clone and reused only the existing canonical pinned `.lake`
artifacts. No update, build, fetch, clone, or dependency mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, and 1546 uniform-L0 Lean 4 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1149` | 0 | rank 354; planned; legacy artifacts unaccepted; theorem incomplete |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | checked mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `(cd Formalizations/Lean && sha256sum lean-toolchain lake-manifest.json)` | 0 | hashes match the environment fingerprint above |
| `rg -n -i 'Dirichlet problem\|Dirichlet.*boundary\|boundary.*Dirichlet' Formalizations/Lean/.lake/packages/mathlib/Mathlib --glob '*.lean'` | 1 | no matching general Dirichlet-problem declaration or source description in pinned mathlib; exit 1 means no matches |

No exact target exists to submit to `lake env lean`; claiming a Lean elaboration check on an
invented proxy would conceal rather than validate the failed gate.

## Retry condition

An accountable source review must provide an immutable primary-source theorem/page and freeze its
exact conclusion, domain and dimension, boundary regularity, data and solution spaces, Laplacian
and trace conventions, quantifier order, constant dependencies, and degenerate cases. The next
statement run can then encode that source-faithful claim with minimal pinned imports, serialize its
elaborated expression and environment, and execute all four required mutation classes.

Until that input exists, statement acceptance and theorem completion are false. Because the
assigned phase is not genuinely self-tested to its completion gate, no
`.stage1-worker-selftest.json` is emitted.
