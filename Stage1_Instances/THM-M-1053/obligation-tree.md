# THM-M-1053 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 16 root-relevant obligations for
`S56-M-1053-OBLIGATION_TREE`. Eligibility was assigned from the exact statement,
the bounded anchor audit, and the classical maximal-inequality/dense-class proof
architecture, independently of current proof availability. A correction, split,
merge, or exclusion requires a new registry version and append-only delta.

## Typed proof route

```text
M1053-ROOT exact StatementShape
`-- M1053-T-ASSEMBLE checked conditional composition
    |-- M1053-T-GENERAL invariant integrable a.e. limit
    |   |-- M1053-L-AE-CONVERGENCE
    |   |   |-- M1053-L-MAXIMAL
    |   |   |-- M1053-L-DENSE-CLASS
    |   |   |-- M1053-N-AVERAGE
    |   |   `-- M1053-X-EXTERNAL
    |   |-- M1053-L-LIMIT-INTEGRABLE
    |   `-- M1053-L-LIMIT-INVARIANT
    `-- M1053-L-ERGODIC-IDENTIFICATION
```

Definitions, boundaries, foundation policy, sources, provenance, trust,
documentation, and workflow order live in separate typed graphs and cannot
masquerade as proof premises.

## Node ledger

### m1053-root
Exact elaborated target. `[H2, M1, R4]`; the anchor audit located a credible
external exact candidate, but no repo-local adapter or root proof exists.

### m1053-s-definitions
Checked `timeAverage` and `StatementShape` interface. `[H2, M0-L, R4]`.

### m1053-s-boundary
Checked zero-index average and explicit noninvertible/atomic-space scope.
`[H2, M0-L, R4]`; this is statement evidence only.

### m1053-s-foundation
Pending transitive axiom, import, TCB, and no-oracle audit. `[H2, M4, R4]`.

### m1053-n-average
Checked definitional alignment with mathlib's `birkhoffAverage`. `[H2, M0-L,
R4]`; this transport provides no convergence proof.

### m1053-l-maximal
Maximal ergodic inequality with exact exceptional-set hypotheses. Critical
budget 100; `[H2, M4, R4]`.

### m1053-l-dense-class
Pointwise convergence on a dense controlled class plus its approximation
interface. Critical budget 100; `[H2, M4, R4]`.

### m1053-l-ae-convergence
The maximal/density passage to a.e. convergence for every integrable real
observable. Critical budget 100; `[H2, M4, R4]`.

### m1053-l-limit-integrable
Integrability of the selected limit witness. `[H2, M4, R4]`.

### m1053-l-limit-invariant
Almost-everywhere invariance of the limit witness. `[H2, M4, R4]`.

### m1053-t-general
The complete nonergodic invariant-limit package. This is one member of the
minimal open root cut. `[H2, M4, R4]`.

### m1053-l-ergodic-identification
Identification of an invariant limit with the constant space integral under
ergodicity. This is the other member of the minimal open root cut. `[H2, M4,
R4]`.

### m1053-t-assemble
`statementShape_of_packages` kernel-checks exact composition and consumes both
open packages. `[H2, M0-L, R4]`; a conditional composition is not root credit.

### m1053-x-external
The immutable `lean4-ergodic-theory` candidate identified by the anchor audit.
It remains outside the pinned closure and requires authorized pinning, an exact
adapter, and transitive trust audit. `[H2, M1, R4]`.

### m1053-x-source
Pending theorem/page/assumption/convention/errata mapping for every material
analytic bridge. This is human-source coverage, not machine credit.

### m1053-x-provenance
Pending terminal-body, wrapper, license, import, axiom, TCB, and replay
inventory. It is informational and cannot inflate proof coverage.

## Status boundary

The frozen minimal root cut is `M1053-T-GENERAL` plus
`M1053-L-ERGODIC-IDENTIFICATION`. The checked conditional assembly introduces
no Birkhoff proof. This phase claims no H0, root closure, audit completion,
theorem completion, or accepted receipt.
