# THM-M-0010 frozen obligation architecture

Item: `S56-M-0010-OBLIGATION_TREE`  
Registry version: 1  
Denominator: `cad255358d70a3800a3c8cc01487f3fd885892841121614567e7c739d109a9cc`

The registry freezes ten canonical obligations before the proof phase observes
or assigns closure. Proof-requirement edges point from parent to child, and
every such edge has a reciprocal child-to-parent composition edge. Separate
refinement, provenance, evidence, trust, documentation, and workflow graphs
prevent support relations from being mistaken for proof dependencies.

## Proof route

```text
M0010-ROOT
+-- M0010-S-EXACT
+-- M0010-S-BOUNDARY
`-- M0010-T-COMPOSE
    `-- M0010-B-UPSTREAM
        +-- M0010-C-STABLE
        +-- M0010-C-INTER
        |   `-- M0010-C-STABLE
        `-- M0010-L-EVENTUAL
```

`M0010-X-SOURCE` and `M0010-X-FOUNDATION` are typed support overlays. They do
not become proof children and cannot inflate machine closure.

## Node ledger

### m0010-root

**Claim:** The exact elaborated Artin-Rees target. **Role:** canonical root.
**Inputs:** exact-statement, boundary, and terminal-composition children.
**Proof route:** compose those children without weakening a binder or equality.
**Branch logic:** bottom/top ideal, bottom submodule, and `n = k` stay explicit.
**Formal map:** `Stage1Instances.THM_M_0010.ArtinReesTarget`. **Trust boundary:**
Lean kernel and pinned mathlib; release trust audit open. **Step ledger:** the
structured node record names premises, inference, output, and outgoing use;
budget 40. **Boundary:** architecture only. **Status vector:** `[H1, M4, R3]`.

### m0010-s-exact

**Claim:** Preserve every universe, typeclass, binder, guard, and equality.
**Role:** statement interface child. **Inputs:** frozen statement fingerprint.
**Proof route:** use only the identical elaborated target. **Branch logic:** no
implicit domain restriction is permitted. **Formal map:** `ArtinReesTarget`.
**Trust boundary:** elaborator and kernel. **Step ledger:** budget 40.
**Boundary:** no root proof. **Status vector:** `[H1, M4, R3]`.

### m0010-s-boundary

**Claim:** Retain all four frozen boundary probes. **Role:** prevent a generic
route from hiding degenerate behavior. **Inputs:** statement boundary records.
**Proof route:** later proof validation must cover these instantiations.
**Branch logic:** bottom ideal, top ideal, bottom submodule, and witness index.
**Formal map:** `boundaryBottomIdeal` and its sibling definitions. **Trust
boundary:** elaborator and kernel. **Step ledger:** budget 40. **Boundary:** the
probes are expressions, not proofs. **Status vector:** `[H1, M4, R3]`.

### m0010-c-stable

**Claim:** The ambient `I`-adic filtration on top is stable. **Role:** supplies
the construction consumed by intersection. **Inputs:** Noetherian ring and
finite module. **Proof route:** audit the terminal body behind
`Ideal.stableFiltration_stable`. **Branch logic:** none currently exposed.
**Formal map:** pinned mathlib declaration. **Trust boundary:** its transitive
body and axioms require proof-phase evidence. **Step ledger:** budget 100.
**Boundary:** naming a deep declaration is not closure. **Status vector:**
`[H1, M4, R3]`.

### m0010-c-inter

**Claim:** Intersection with the trivial filtration on `N` preserves stability.
**Role:** constructs the induced filtration. **Inputs:** `M0010-C-STABLE` and
the trivial filtration. **Proof route:** audit `Stable.inter_right` and its
specialization. **Branch logic:** confirm the right-intersection orientation.
**Formal map:** `Ideal.Filtration.Stable.inter_right`. **Trust boundary:** pinned
mathlib dependency closure. **Step ledger:** budget 100. **Boundary:** no proof
credit from the architecture phase. **Status vector:** `[H1, M4, R3]`.

### m0010-l-eventual

**Claim:** Stability yields one `k` and the shifted equality for every `n >= k`.
**Role:** core mathematical extraction. **Inputs:** the stable intersected
filtration. **Proof route:** expand and audit `exists_pow_smul_eq_of_ge`.
**Branch logic:** preserve the lower-bound guard and natural subtraction.
**Formal map:** `Ideal.Filtration.Stable.exists_pow_smul_eq_of_ge`. **Trust
boundary:** pinned body closure. **Step ledger:** budget 100. **Boundary:** the
deep bridge remains a distinct obligation. **Status vector:** `[H1, M4, R3]`.

### m0010-b-upstream

**Claim:** The pinned upstream theorem has exactly the frozen equality. **Role:**
bridge the three stable-filtration obligations to the candidate package.
**Inputs:** construction and eventual-equality nodes. **Proof route:** inspect
the pinned body that composes those declarations. **Branch logic:** no alias is
counted as a second body. **Formal map:** `Ideal.exists_pow_inf_eq_pow_smul`.
**Trust boundary:** candidate reports `propext`, `Classical.choice`, and
`Quot.sound`; transitive acceptance is open. **Step ledger:** budget 40.
**Boundary:** anchor feasibility is not proof acceptance. **Status vector:**
`[H1, M1, R3]`.

### m0010-t-compose

**Claim:** An exact candidate package yields the identical package. **Role:**
freeze the final composition interface. **Inputs:** `M0010-B-UPSTREAM`.
**Proof route:** consume the named package directly. **Branch logic:** none.
**Formal map:** `root_of_exact_candidate`. **Trust boundary:** Lean reports only
the already observed standard axioms. **Step ledger:** budget 40. **Boundary:**
the conditional identity supplies no candidate and closes no node. **Status
vector:** `[H1, M3, R3]`.

### m0010-x-source

**Claim:** Pinpoint source passages must cover the substantive proof nodes.
**Role:** human-source overlay. **Inputs:** source crosswalk and proof graph.
**Proof route:** later reviewed passage mapping. **Branch logic:** errata and
edition drift remain explicit. **Formal map:** non-machine support node. **Trust
boundary:** independent source review. **Step ledger:** budget 40. **Boundary:**
no machine credit. **Status vector:** `[H1, M4, R3]`.

### m0010-x-foundation

**Claim:** Terminal bodies, imports, axioms, TCB, and replay evidence must be
inventoried. **Role:** provenance and trust overlay. **Inputs:** every terminal
machine body. **Proof route:** later machine-derived closure report. **Branch
logic:** wrappers and aliases are deduplicated. **Formal map:** typed support
edges in `typed-graphs.json`. **Trust boundary:** release audit remains open.
**Step ledger:** budget 40. **Boundary:** informational only. **Status vector:**
`[H1, M4, R3]`.

## Status boundary

This item freezes architecture and validation recipes only. No obligation is
credited closed, the root remains `M4`, and audit, theorem, readable, source,
trust, independent-review, and release completion all remain false.
