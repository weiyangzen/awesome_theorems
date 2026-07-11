# THM-M-0105 Intake Dossier

Status: `planned`; intake only. This dossier freezes the intended classical curve statement for later exact-source and Lean statement gates. It does not claim an elaborated exact target, a proof, source acceptance, or theorem completion.

## Scope Map

| Surface | In scope | Boundary still requiring a later gate |
|---|---|---|
| Base | arbitrary field `k` | confirm source conventions for non-algebraically-closed fields |
| Curve | smooth, projective, geometrically integral, dimension one over `k` | choose exact mathlib predicates and universe levels |
| Divisors | arbitrary divisor `D`; canonical divisor `K_X` | select concrete divisor/Cartier divisor and canonical sheaf APIs |
| Invariant | `l(E) = dim_k H^0(X, O_X(E))`, genus `g(X)`, divisor degree | freeze finiteness and integer/natural coercions |
| Conclusion | `l(D) - l(K_X-D) = deg(D) + 1 - g(X)` | elaborate and mutation-test in `STATEMENT` |

The historical file `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_027.lean` is discovery input only. Its `THM_M_0105_StatementShapeTarget` quantifies over abstract, existentially chosen divisor data, so it is not accepted as the exact canonical claim.

## Source-Statement Crosswalk

Primary-source candidate (pinpoint to be independently checked in `ANCHOR_AUDIT`): Robin Hartshorne, *Algebraic Geometry*, Graduate Texts in Mathematics 52, Springer (1977), Chapter IV, Section 1, Theorem 1.3 (Riemann-Roch). The intake uses the standard formula `l(D) - l(K-D) = deg D + 1 - g` associated with that theorem.

| Canonical component | Candidate source locus | Intake disposition |
|---|---|---|
| nonsingular projective curve and divisor `D` | IV.1 setup and Theorem 1.3 | mapped, not yet independently source-accepted |
| canonical divisor `K` | IV.1 terminology preceding Theorem 1.3 | mapped, edition/page and definition cross-reference pending |
| `l(D)` | IV.1 divisor linear-system notation | mapped, exact definition/page pending |
| equality `l(D)-l(K-D)=deg D+1-g` | IV.1, Theorem 1.3 | verbatim mathematical formula candidate |
| arbitrary-field/geometric-integrality formulation | modern scheme-level normalization | requires an explicit source bridge; not credited to Hartshorne without audit |

No errata search or independent source review has been completed. Consequently the human-source state remains `H5`, not `H0`. The next source audit must record ISBN/edition, printed page, exact assumptions, notation definitions, errata query, and reviewer.

## Open Task DAG

`G01 exact statement/source bridge -> G02 profiles -> G03 activation`; `D01 discovery freeze`; then `H01 primary-source audit` and `M01 formal-candidate audit`; only afterward may `T01` freeze the obligation registry. The blueprint phases `STATEMENT`, `ANCHOR_AUDIT`, `OBLIGATION_TREE`, `PROOF`, `VALIDATION`, and `RELEASE` remain open and dependency ordered.

## Validation Record

On base revision `a8d6489fd935cd71fa4499f2f3f5b051998203f4`:

- `python3 Docs/tools/check_stage1_standard.py` exited 0: standard reports 1546 uniform-L0 targets.
- `python3 scripts/stage1_target.py check` exited 0: 1546 unique targets and ranks passed.
- `python3 scripts/stage1_target.py show THM-M-0105` exited 0: rank 27, `planned`, `L0`, `rework_required`, theorem incomplete.
- `python3 -m json.tool Stage1_Instances/THM-M-0105/intake.json >/dev/null` exited 0.
- `git diff --check -- Stage1_Instances/THM-M-0105` exited 0.

This is the smallest real intake validation. Lean compilation is deliberately deferred because intake has not frozen an exact formal expression; compiling the legacy abstract target would not validate the canonical theorem.
