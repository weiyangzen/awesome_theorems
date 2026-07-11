# THM-M-0387 frozen obligation architecture

## Freeze boundary

This is registry version 1 for `S56-M-0387-OBLIGATION_TREE`. It freezes 132
canonical IDs before the proof phase: 121 root-relevant proof/refinement
obligations and 11 informational trust/provenance overlays. The machine,
human-source, and readable denominators are explicit ordered ID sets in
`obligation-registry.json`; their canonical projection digest is
`e934e59a6dfc78dda8ade1978b1b037c982ab8d1a9ca3d2e6c105b6f00b36643`.
No item is excluded because it lacks a proof. The informational `M0387-X*`
records are excluded only from proof/source denominators because they model
trust and candidate provenance rather than mathematical conclusions.

The mandatory section 12.2 architecture is present and recursively expanded.
The retained `THM-M-0387/proof_units.json` supplied discovery names and
decomposition only. `build_obligation_artifacts.py` deliberately discards its
status, debt, evidence, and completion fields before producing this new
planned registry. Thus no historical `[x]`, wrapper, source label, or coverage
number receives rev-5.6 proof credit.

## Typed proof route

```text
M0387-ROOT  exact frozen natural-number target [open M2]
|-- M0387-S  statement, transport, and foundation refinements
|-- M0387-R  exponent reduction and conditional recomposition
|-- M0387-B3  exponent-three branch
|-- M0387-B4  exponent-four descent branch
|-- M0387-RP  regular-prime branch
|-- M0387-SMALL  additional bounded-exponent discovery branch
`-- M0387-WTW  general odd-prime branch [remaining root cut]
    |-- W01 primitive counterexample normalization
    |-- W02 Frey curve construction and local invariants
    |-- W03 mod-p representation and ramification properties
    |-- W04 semistable modularity
    |   |-- modular forms and Hecke algebras
    |   |-- residual modularity
    |   |-- universal and local deformation problems
    |   |-- Taylor-Wiles primes and patching
    |   |-- minimal R=T
    |   `-- non-minimal lifting and terminal modularity
    |-- W05 level lowering
    |-- W06 level-two weight-two impossibility
    |-- W07 contradiction
    |-- W08 all odd-prime closure
    `-- W09 exact-root recomposition
```

The complete edges, including every B3, B4, regular-prime, and WTW child, are
machine-readable in `typed-graphs.json`. Proof and refinement edges alone
reach every required obligation from `M0387-ROOT` and are acyclic. Provenance,
evidence, trust, documentation, and workflow edges are separate graphs, so a
source link or workflow transition cannot masquerade as a proof premise.

## Leaf and composition policy

Every nonleaf has `step_budget: "split-required"`. Every presently leaf-shaped
record has a budget at most 100 plus a substantive planned ledger, but is not
certified as a final leaf: most signatures are still planned rather than exact
elaborated Lean declarations, source crosswalks are not pinpoint-complete, and
parent composition certificates do not exist. Later proof work must split any
leaf whose exact signature, source structure, dependency fan-in, or substantive
ledger reveals hidden high-risk work. The seven canonical high-risk packages
named by `Docs/Blueprint_Guidelines.md` remain represented within the B4 and
regular-prime subtrees rather than being collapsed into wrappers.

No child-to-parent certificate is credited in this phase. For each nonleaf,
the proof phase must add an exact harness binding the parent and child
fingerprints, consuming every required child, and yielding the full parent
target. `FermatLastTheorem.of_odd_primes` is only the conditional assembly
anchor; it does not discharge `M0387-WTW`.

## Provenance and trust boundary

The anchor audit found pinned declarations for exponents 3 and 4, regular
primes, and conditional recomposition. Those are candidate body boundaries for
later node-scoped admission, not closed obligations here. The Imperial exact
root is an informational provenance overlay because its immutable audited body
transitively contains `sorry`; it supplies no machine closure. Foundation,
transitive declaration closure, axioms, computation, and TCB records remain
pending for every proof body admitted later.

## Phase verdict

The registry and seven typed graphs are frozen and structurally self-tested.
The exact statement re-elaborates with the pinned Lean executable. This phase
proves no FLT branch, checks no parent composition certificate, and makes no
`AUDIT-Z` or `THEOREM-Z` claim. The root remains `M2`; the remaining root cut
set is `M0387-WTW`, the general nonregular odd-prime closure.
