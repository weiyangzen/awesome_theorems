# THM-M-0474 frozen obligation architecture

Item `S56-M-0474-OBLIGATION_TREE` freezes registry version 1 against the exact statement and
immutable anchor audit. The 21 canonical IDs are the denominator for later machine, human-source,
and readable coverage. Eligibility was derived from the statement and visible terminal source
chain rather than the known availability of the candidate. Any target correction, split, merge,
exclusion, eligibility change, or terminal-body change requires a new registry version and an
append-only delta.

## Proof Route

```text
M0474-ROOT exact Fermat little theorem target [open M3]
`-- M0474-T-COMPOSE conditional exact child-to-root composition
    `-- M0474-L-NAT Nat.ModEq.pow_card_sub_one_eq_one [audited candidate]
        |-- M0474-N-NAT-INT natural ModEq and power casts to Int
        |-- M0474-N-COPRIME Nat.Coprime to integer IsCoprime
        `-- M0474-L-INT Int.ModEq.pow_card_sub_one_eq_one
            |-- M0474-C-ZMOD-NONZERO prime instance and nonzero ZMod residue
            |-- M0474-T-INT-ZMOD ZMod equality to integer ModEq
            `-- M0474-L-ZMOD ZMod.pow_card_sub_one_eq_one
                |-- M0474-T-ZMOD-CARD card (ZMod p) = p
                `-- M0474-L-FINITE-FIELD FiniteField.pow_card_sub_one_eq_one
                    |-- M0474-C-UNIT package the nonzero element as a unit
                    `-- M0474-L-GROUP-CARD finite-group pow_card_eq_one
```

The proof graph mirrors the pinned source bodies rather than treating the one-line natural wrapper
as a leaf. Every parent-to-child `proof_requires` edge has a reciprocal child-to-parent `composes`
edge. The exact interface, p = 2 and degenerate-case policy, and coprime/not-divides transport live
in the refinement graph. Source, provenance, evidence, trust, documentation, and workflow edges
are separate and cannot receive proof credit.

## Assurance Overlays

### m0474-s-interface

The exact ordered natural binders, primality and coprimality premises, exponent, modulus, and
`Nat.ModEq` conclusion are preserved. The expression fingerprint is `5475969f...590e8`.

### m0474-s-boundary

The case `p = 2` stays in scope. Composite and zero moduli are excluded by `p.Prime`; bases
divisible by `p` are excluded by `a.Coprime p`. No additional nonzero or lower-bound premise is
introduced. The visible proof is uniform, so a separate case split is marked not applicable only
pending independent review.

### m0474-s-transport

`fermatLittleTheoremTarget_iff_notDvd` checks the transport between coprimality and nondivisibility.
It is one semantic obligation and creates no duplicate root or proof-body credit.

### m0474-s-foundation

The anchor audit observed `propext`, `Classical.choice`, and `Quot.sound`; full transitive
foundation, TCB, computation, and independent replay acceptance remains open.

### m0474-x-source

The catalog sentence omits the domain, primality, and coprimality assumptions. A primary edition,
pinpoint theorem or page, translation and assumption map, errata review, and independent source
review remain required. Human debt therefore remains `H1`.

### m0474-x-provenance

The exact natural body has stable identity
`git-blob:fb3668d594f865e52f20c8af45e91e7e3b1eebd8:Nat.ModEq.pow_card_sub_one_eq_one`.
The visible chain is pinned in two mathlib source files, but complete transitive declaration,
license, trust, and replay closure is still a downstream gate.

### m0474-x-readable

This route summary is architecture documentation, not an independently reviewed `R0`
reconstruction. Every leaf budget is at most 60 substantive steps and must be split again if later
formalization exposes hidden work. Readability debt remains `R4`.

### m0474-x-workflow

Proof installation, node validation, hermetic replay, independent verification, release, freshness,
and revocation receipts remain open and do not act as proof premises.

## Freeze Boundary

`ObligationTree.lean` checks only `root_of_exactNatAnchor`, with the exact natural anchor as an
explicit premise. It does not invoke that anchor to construct the root. The anchor remains an
`M0-W_candidate_pending_proof_phase_and_master_acceptance`; accepted proof state is empty and the
authoritative root remains `[H1, M3, R4]`. No H0, R0, audit completion, release, or theorem
completion is claimed.
