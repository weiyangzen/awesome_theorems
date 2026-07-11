# THM-M-0113 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 26 root-relevant obligations before the proof phase
assigns any closure. All 26 are independently eligible for machine, primary
source, and readable-reconstruction coverage; none is excluded because the
required analytic infrastructure is difficult or absent. The ordered canonical
projection and its SHA-256 in `obligation-registry.json` are the denominator.
Any later split, merge, exclusion, or eligibility change requires registry
version 2 and an append-only ID delta.

Only `M0113-ROOT` has a frozen Lean source fingerprint. Other signatures are
marked `planned:v1`; their prose does not pretend that a Lean declaration has
already elaborated. Every semantic leaf has a premise/inference/output ledger
with a provisional eight-step budget. Discovery of hidden mathematical work or
a proof exceeding 100 steps requires a registry split before closure credit.

## Typed proof route

```text
M0113-ROOT  exact compact-Kahler target [open M4]
`-- M0113-T  exact final composition
    |-- M0113-S  statement/data/boundary/transport
    |-- M0113-D  internal direct sum in every degree
    |   |-- M0113-H  harmonic representative equivalence
    |   |   |-- M0113-A  analytic complexes and elliptic theory
    |   |   |-- M0113-H-EXIST
    |   |   `-- M0113-H-UNIQUE
    |   |-- M0113-K  Kahler identities and type preservation
    |   |-- M0113-D-INDEP
    |   `-- M0113-D-SPAN
    |-- M0113-C  conjugation symmetry
    |   |-- M0113-C-CHAIN
    |   |-- M0113-C-TYPE
    |   `-- M0113-C-IFF
    |-- M0113-P  terminal provenance
    |-- M0113-V  trust and evidence
    `-- M0113-R  primary sources and readable reconstruction
```

The proof and refinement graphs are acyclic and reach every obligation.
Provenance, evidence, trust, documentation, and workflow are separate typed
graphs, preventing a source link, task transition, or validation record from
being counted as a proof premise.

## Current cut set

The first concrete machine cut is `M0113-A-DR`, `M0113-A-DOL`, `M0113-A-ELL`,
`M0113-K-ID`, and `M0113-C-CHAIN`: de Rham/Dolbeault cohomology, elliptic Hodge
theory, Kahler identities, and chain-level conjugation are absent from the
pinned support surface. This cut is architectural, not a proof of minimality or
global nonexistence. It records where implementation must begin without
substituting algebraic Kahler differentials or assuming the desired theorem in
`HodgeData`.

`ObligationTree.lean` kernel-checks two composition-only steps: joining the
direct-sum and conjugation branches degreewise, and obtaining the required
membership `iff` from two forward type swaps plus involutivity. It supplies no
analytic premise and closes no registry node. H0, M0, R0, audit completion,
theorem completion, release evidence, and master acceptance remain open.
