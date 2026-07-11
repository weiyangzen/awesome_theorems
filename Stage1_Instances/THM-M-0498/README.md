# THM-M-0498 rev-5.6 intake

This is the rev-5.6 `planned` dossier for the Riemann-von Mangoldt explicit
formula. The repository's short source phrase, "an explicit formula for the
prime-counting function", is not precise enough to select a unique theorem.
This intake therefore selects a weighted `psi` formula as the primary candidate
and keeps the ordinary prime-counting formula as a distinct transport target.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | explicit formula for weighted prime powers from the pole and zeros of `riemannZeta` | coefficients, correction terms, zero summation, and endpoint convention await statement freeze |
| Arithmetic objects | von Mangoldt function, `Chebyshev.psi`, `Chebyshev.theta`, and real-argument prime counting | available names are discovery anchors, not closure evidence |
| Analytic objects | zeta continuation, logarithmic derivative, pole at one, trivial and nontrivial zeros | exact imported declarations and trust closure await audit |
| Proof architecture | Perron/inverse Mellin step, contour shift, residues, zero sum convergence, endpoint correction | architecture only; no bridge is credited |
| Linked variant | transfer from weighted formula to Riemann's `J`-type or ordinary `pi` formula | requires separately checked normalization and inversion |
| Exclusion | the zero-counting asymptotic commonly also called the Riemann-von Mangoldt formula | not the manifest's prime-counting claim |
| Foundations | Lean 4 kernel and pinned mathlib with an accepted classical-analysis policy | environment fingerprint and TCB profile remain open |

The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_258.lean`
is explicitly nonterminal and packages its desired equality inside input data.
It may guide the dependent statement and anchor-audit phases, but this intake
does not inherit its checks or treat `terminalConclusion_project` as a proof of
the explicit formula.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`

The next node must choose and elaborate an exact formula without hiding the
mathematics in propositional bridge fields. It must mutation-test the lower
bound, discontinuity convention, zero family/summation order, correction
terms, and the distinction between `psi`, `J`, and `pi`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The first
failed theorem gate is the exact Lean statement gate. No expression hash,
environment fingerprint, checked source normalization, or terminal proof is
claimed. The theorem is not complete.

The commands and results supporting this intake node are recorded in
`validation.md`. Master acceptance remains outstanding.
