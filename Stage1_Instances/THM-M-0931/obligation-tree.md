# THM-M-0931 frozen obligation architecture

## Freeze boundary

Registry version 1 freezes 32 semantic obligations and seven separate typed
graphs. The denominator binds the exact statement and anchor-audit hashes. The
anchor phase had already located a pinned mathlib candidate, but eligibility
and the denominator do not depend on accepting that candidate or on observed
closure. No obligation is accepted closed.

The public multiset wrapper is counted once. Its indexed prime-composite proof,
the prime zero-sum construction, the Chevalley-Warning bridge, and the composite
disjoint-block construction remain explicit. The `ZMod` statement transport is
an alternate view of the same integer witness and cannot duplicate root credit.

## Typed proof route

```text
M0931-ROOT exact positive exact-count target
|-- M0931-T-ROOT-COMPOSE conditional exact package
|-- M0931-S-COUNT-TRANSPORT exact count from a lower bound
`-- M0931-A-MULTISET-EGZ pinned multiset candidate
    |-- M0931-N-ENUMERATE occurrence enumeration
    `-- M0931-L-INDEXED-EGZ indexed integer theorem
        `-- M0931-B-INDUCTION zero/one/prime/composite split
            |-- M0931-B-ZERO
            |-- M0931-B-ONE
            |-- M0931-B-PRIME -> integer/ZMod prime route
            `-- M0931-B-COMPOSITE -> disjoint block route
```

Only the exact root and multiset-enumeration child interfaces are machine
composition edges in registry version 1. The internal pinned-body expansion is
stored as typed `logical_decomposition` plans pending exact child-to-parent
harnesses. Source, provenance, trust, documentation, evidence, and workflow
edges cannot act as proof premises.

## Node ledger

### m0931-root

**Claim:** For positive `n`, exactly `2 * n - 1` integer occurrences contain an
`n`-occurrence submultiset whose sum is divisible by `n`.
**Role:** Canonical root. **Inputs:** the terminal composition, at-least-count
anchor, and exact-count transport. **Proof route:** consume all three exact
packages. **Branch logic:** inherited from the indexed prime-composite route.
**Formal map:** `Stage1Instances.THM_M_0931.ErdosGinzburgZivTarget`.
**Trust boundary:** no imported proof is adopted here. **Step ledger:**
`STEP-M0931-ROOT-01`. **Boundary:** root closure remains open.
**Status vector:** `[H1, M3, R4]`.

### m0931-s-interface

**Claim:** The root binds `n : Nat`, `0 < n`, `s t : Multiset Int`, exact input
and witness cardinalities, `t <= s`, and integer divisibility in that order.
**Role:** Statement overlay. **Inputs:** frozen elaborated expression.
**Proof route:** preserve every domain, binder, cast, and occurrence condition.
**Branch logic:** none. **Formal map:** `Statement.lean` and `statement.json`.
**Trust boundary:** statement evidence only. **Step ledger:**
`STEP-M0931-S-INTERFACE-01`. **Boundary:** no proof credit.
**Status vector:** `[H1, M4, R4]`.

### m0931-s-boundary

**Claim:** `n = 0` is excluded; `n = 1`, negative, repeated, zero, and all-equal
integer inputs remain included, with exactly `2n-1` occurrences.
**Role:** Prevent silent broadening or restriction. **Inputs:** positivity and
exact-count mutations. **Proof route:** distinguish the root from all-natural
and at-least-count candidates. **Branch logic:** source-positive versus stronger
candidate boundary. **Formal map:** `statement.json` mutation ledger.
**Trust boundary:** independently reviewed source interpretation remains open.
**Step ledger:** `STEP-M0931-S-BOUNDARY-01`. **Boundary:** no H0.
**Status vector:** `[H1, M4, R4]`.

### m0931-s-count-transport

**Claim:** The at-least-count multiset theorem implies the positive exact-count
root. **Role:** source specialization. **Inputs:** `AtLeastCountAnchor` and input
cardinality equality. **Proof route:** turn equality into a lower bound and use
the statement-phase implication. **Branch logic:** positivity is retained but
unused by the stronger anchor. **Formal map:** `exactCountTransport_checked`.
**Trust boundary:** local conditional composition only. **Step ledger:**
`STEP-M0931-S-COUNT-TRANSPORT-01`. **Boundary:** it supplies no anchor.
**Status vector:** `[H1, M0-L, R4]` provisionally, with no accepted closure.

### m0931-s-residue-transport

**Claim:** Integer divisibility of the same selected sum is equivalent to its
cast being zero in `ZMod n`. **Role:** encoding crosswalk. **Inputs:** the exact
integer witness. **Proof route:** apply `ZMod.intCast_zmod_eq_zero_iff_dvd`.
**Branch logic:** none. **Formal map:**
`erdosGinzburgZivTarget_iff_residueTarget`. **Trust boundary:** this does not
replace integer inputs by `ZMod` inputs. **Step ledger:**
`STEP-M0931-S-RESIDUE-TRANSPORT-01`. **Boundary:** no duplicate root credit.
**Status vector:** `[H1, M0-L, R4]` provisionally.

### m0931-s-foundation

**Claim:** The route must be checked against the selected policy for `propext`,
`Classical.choice`, `Quot.sound`, compiled artifacts, and external execution.
**Role:** release trust gate. **Inputs:** exact declarations and transitive
closure. **Proof route:** recompute axioms and TCB membership. **Branch logic:**
allowed versus disallowed principles. **Formal map:** anchor audit and future
trust receipt. **Trust boundary:** current evidence is warm and nonrelease.
**Step ledger:** `STEP-M0931-S-FOUNDATION-01`. **Boundary:** open.
**Status vector:** `[H1, M4, R4]`.

### m0931-t-root-compose

**Claim:** `RootComposition`, `AtLeastCountAnchor`, and `ExactCountTransport`
jointly yield the exact root. **Role:** checked terminal interface.
**Inputs:** all three named children. **Proof route:** apply the composition to
the anchor and transport. **Branch logic:** none beyond explicit packages.
**Formal map:** `root_of_terminal_packages`. **Trust boundary:** imported EGZ
remains a premise. **Step ledger:** `STEP-M0931-T-ROOT-COMPOSE-01`.
**Boundary:** no accepted M0 root. **Status vector:** `[H1, M0-L, R4]`
provisionally.

### m0931-a-multiset-egz

**Claim:** At least `2n-1` integer occurrences contain an `n`-occurrence
submultiset with sum divisible by `n`. **Role:** exact stronger anchor consumed
by source specialization. **Inputs:** indexed EGZ and occurrence enumeration.
**Proof route:** enumerate, invoke indexed selection, map first projections.
**Branch logic:** delegated explicitly below. **Formal map:** pinned
`Int.erdos_ginzburg_ziv_multiset`, lines 192-195. **Trust boundary:** candidate
body is in pinned mathlib, not local. **Step ledger:**
`STEP-M0931-A-MULTISET-EGZ-01`. **Boundary:** M0-W candidate only.
**Status vector:** `[H1, M0-W, R4]` provisionally.

### m0931-n-enumerate

**Claim:** `Multiset.toEnumFinset` preserves occurrences, cardinality, and sums,
and a selected indexed subset maps to a submultiset. **Role:** representation
crossing. **Inputs:** an abstract `IndexedIntegerEGZ`. **Proof route:** apply it
to value-index pairs and use `map_fst_le_of_subset_toEnumFinset`.
**Branch logic:** none. **Formal map:** `multisetEnumerationTransport_checked`.
**Trust boundary:** uses standard quotient/classical multiset infrastructure.
**Step ledger:** `STEP-M0931-N-ENUMERATE-01`. **Boundary:** supplies no indexed
engine. **Status vector:** `[H1, M0-L, R4]` provisionally.

### m0931-l-indexed-egz

**Claim:** An indexed set of at least `2n-1` integers contains `n` selected
indices whose sum is divisible by `n`. **Role:** central engine under the
multiset wrapper. **Inputs:** modulus, index set, values, cardinality bound.
**Proof route:** prime-composite induction. **Branch logic:** zero, one, prime,
and product cases are exhaustive. **Formal map:** pinned
`Int.erdos_ginzburg_ziv`, lines 110-178. **Trust boundary:** shared imported
body, not a second root proof. **Step ledger:**
`STEP-M0931-L-INDEXED-EGZ-01`. **Boundary:** internal exact composition pending.
**Status vector:** `[H1, M0-W, R4]` as a candidate interface only.

### m0931-b-induction

**Claim:** `Nat.prime_composite_induction` covers every natural modulus by
zero, one, prime, or a product of two factors at least two.
**Role:** exhaustive branch recomposition. **Inputs:** all four branch packages.
**Proof route:** generalize the index type and apply the induction principle.
**Branch logic:** exactly its four constructors. **Formal map:** EGZ lines
113-129. **Trust boundary:** exact child harness pending. **Step ledger:**
`STEP-M0931-B-INDUCTION-01`. **Boundary:** no standalone closure.
**Status vector:** `[H1, M4, R4]`.

### m0931-b-zero

**Claim:** The stronger theorem at `n=0` is witnessed by the empty subset.
**Role:** total-Nat candidate boundary, not source-root coverage. **Inputs:**
none beyond the frozen context. **Proof route:** choose empty and simplify.
**Branch logic:** zero constructor. **Formal map:** EGZ lines 116-117.
**Trust boundary:** outside the positive source theorem. **Step ledger:**
`STEP-M0931-B-ZERO-01`. **Boundary:** no human-source denominator credit.
**Status vector:** `[H1, M4, R4]`.

### m0931-b-one

**Claim:** At `n=1`, a one-element subset exists and its sum is divisible by
one. **Role:** base branch. **Inputs:** cardinality lower bound. **Proof route:**
use `exists_subset_card_eq` and simplify. **Branch logic:** one constructor.
**Formal map:** EGZ lines 118-119. **Trust boundary:** imported source body.
**Step ledger:** `STEP-M0931-B-ONE-01`. **Boundary:** internal composition
pending. **Status vector:** `[H1, M4, R4]`.

### m0931-b-prime

**Claim:** For prime `p`, trim to exactly `2p-1` inputs and apply the integer
prime theorem. **Role:** prime branch. **Inputs:** primality and the exact prime
package. **Proof route:** install `Fact p.Prime`, select the exact subset, and
compose containment. **Branch logic:** prime constructor. **Formal map:** EGZ
lines 120-125. **Trust boundary:** private terminal route below.
**Step ledger:** `STEP-M0931-B-PRIME-01`. **Boundary:** exact harness pending.
**Status vector:** `[H1, M4, R4]`.

### m0931-t-prime-cast

**Claim:** The prime `ZMod p` zero-sum selection implies integer divisibility by
`p` for the original integer values. **Role:** representation transport.
**Inputs:** exact ZMod prime theorem. **Proof route:** commute integer cast with
the sum and apply cast-zero iff divisibility. **Branch logic:** none.
**Formal map:** private `Int.erdos_ginzburg_ziv_prime`, lines 96-99.
**Trust boundary:** private body pinned by source location. **Step ledger:**
`STEP-M0931-T-PRIME-CAST-01`. **Boundary:** no public independent proof body.
**Status vector:** `[H1, M4, R4]`.

### m0931-l-zmod-prime

**Claim:** Exactly `2p-1` residues for prime `p` contain `p` whose sum is zero.
**Role:** prime combinatorial engine. **Inputs:** polynomial construction,
degree bound, Chevalley-Warning, nonzero root, support cardinality and sum.
**Proof route:** encode support by common roots and extract a nonzero one.
**Branch logic:** zero solution versus a distinct solution. **Formal map:**
private `ZMod.erdos_ginzburg_ziv_prime`, lines 56-90. **Trust boundary:** pinned
private body. **Step ledger:** `STEP-M0931-L-ZMOD-PRIME-01`.
**Boundary:** exact child harness pending. **Status vector:** `[H1, M4, R4]`.

### m0931-c-polynomials

**Claim:** The two polynomial sums encode support cardinality and weighted
input sum. **Role:** prime-case construction. **Inputs:** index set and residue
values. **Proof route:** construct `f1` and `f2` from powers `p-1`.
**Branch logic:** none. **Formal map:** EGZ lines 34-41. **Trust boundary:**
private definitions. **Step ledger:** `STEP-M0931-C-POLYNOMIALS-01`.
**Boundary:** well-formedness alone proves no selection.
**Status vector:** `[H1, M4, R4]`.

### m0931-l-degree-bound

**Claim:** The two total degrees sum to less than the `2p-1` variables.
**Role:** Chevalley-Warning premise. **Inputs:** polynomial definitions and
prime lower bound. **Proof route:** bound both degrees by `p-1` and use
arithmetic. **Branch logic:** none. **Formal map:** EGZ lines 43-50.
**Trust boundary:** private lemma. **Step ledger:**
`STEP-M0931-L-DEGREE-BOUND-01`. **Boundary:** no root-count conclusion.
**Status vector:** `[H1, M4, R4]`.

### m0931-x-chevalley-warning

**Claim:** The field characteristic divides the common-root count when the
sum of two polynomial degrees is below the variable count. **Role:** major
imported bridge. **Inputs:** degree inequality. **Proof route:** encode the pair
by `Bool` and invoke finite-family Chevalley-Warning. **Branch logic:** Boolean
normalization only. **Formal map:** `char_dvd_card_solutions_of_add_lt`,
ChevalleyWarning lines 184-194. **Trust boundary:** distinct pinned source body.
**Step ledger:** `STEP-M0931-X-CHEVALLEY-WARNING-01`. **Boundary:** the 1961
source route and mathlib route are not asserted identical.
**Status vector:** `[H1, M4, R4]`.

### m0931-l-nonzero-solution

**Claim:** Zero is a common root and divisibility of a positive root count by
prime `p >= 2` produces a distinct common root. **Role:** existence step.
**Inputs:** Chevalley-Warning count and primality. **Proof route:** prove
inhabitation, derive count at least `p`, and choose another element.
**Branch logic:** zero versus distinct root. **Formal map:** EGZ lines 60-73.
**Trust boundary:** internal imported proof. **Step ledger:**
`STEP-M0931-L-NONZERO-SOLUTION-01`. **Boundary:** no selected support yet.
**Status vector:** `[H1, M4, R4]`.

### m0931-l-prime-card

**Claim:** The nonzero-coordinate support is positive, divisible by `p`, and
less than `2p`, so it has cardinality `p`. **Role:** witness cardinality.
**Inputs:** nonzero common root and the `f1` equation. **Proof route:** use the
power identity, positivity, and ambient bound. **Branch logic:** the arithmetic
multiple is forced. **Formal map:** EGZ lines 74-88. **Trust boundary:** internal
imported proof. **Step ledger:** `STEP-M0931-L-PRIME-CARD-01`.
**Boundary:** no sum conclusion. **Status vector:** `[H1, M4, R4]`.

### m0931-l-prime-sum

**Claim:** The selected support has residue sum zero. **Role:** prime witness
conclusion. **Inputs:** the `f2` common-root equation. **Proof route:** rewrite
evaluation with the power identity and filtered sum. **Branch logic:** none.
**Formal map:** EGZ lines 89-90. **Trust boundary:** internal imported proof.
**Step ledger:** `STEP-M0931-L-PRIME-SUM-01`. **Boundary:** requires the support
and cardinality nodes. **Status vector:** `[H1, M4, R4]`.

### m0931-b-composite

**Claim:** At modulus `m*n`, disjoint `n`-blocks and an `m`-selection of their
normalized sums produce the required selection. **Role:** composite branch.
**Inputs:** both induction hypotheses and disjoint-block construction.
**Proof route:** build `2m-1` blocks, select `m`, and union them.
**Branch logic:** composite constructor with factors at least two.
**Formal map:** EGZ lines 126-178. **Trust boundary:** imported source body.
**Step ledger:** `STEP-M0931-B-COMPOSITE-01`. **Boundary:** exact harness
pending. **Status vector:** `[H1, M4, R4]`.

### m0931-c-disjoint-blocks

**Claim:** Maintain a family of disjoint `n`-element subsets contained in the
input, each with sum divisible by `n`. **Role:** composite invariant.
**Inputs:** inner induction hypothesis. **Proof route:** package cardinality,
pairwise disjointness, containment, size, and divisibility. **Branch logic:**
family size induction. **Formal map:** EGZ lines 130-135.
**Trust boundary:** internal construction. **Step ledger:**
`STEP-M0931-C-DISJOINT-BLOCKS-01`. **Boundary:** no terminal union.
**Status vector:** `[H1, M4, R4]`.

### m0931-l-inner-induction

**Claim:** Extend a family of `k` blocks to `k+1` while `k+1 <= 2m-1`.
**Role:** construct all required disjoint blocks. **Inputs:** the invariant and
the `n` induction hypothesis. **Proof route:** bound unused inputs, select a new
block, and preserve disjointness. **Branch logic:** zero/successor family size.
**Formal map:** EGZ lines 146-178. **Trust boundary:** imported body.
**Step ledger:** `STEP-M0931-L-INNER-INDUCTION-01`. **Boundary:** does not select
the outer subfamily. **Status vector:** `[H1, M4, R4]`.

### m0931-l-outer-induction

**Claim:** Among `2m-1` normalized block sums, choose `m` with sum divisible by
`m`. **Role:** outer selection. **Inputs:** the `m` induction hypothesis and
block divisibility by `n`. **Proof route:** assign each block `sum/n` and invoke
indexed EGZ at `m`. **Branch logic:** none. **Formal map:** EGZ lines 135-139.
**Trust boundary:** imported body. **Step ledger:**
`STEP-M0931-L-OUTER-INDUCTION-01`. **Boundary:** no union arithmetic.
**Status vector:** `[H1, M4, R4]`.

### m0931-t-composite-assemble

**Claim:** The union of the selected disjoint blocks has `m*n` elements and
sum divisible by `m*n`. **Role:** composite terminal. **Inputs:** disjoint block
family and outer selection. **Proof route:** use `card_biUnion`, `sum_biUnion`,
integer division, and divisibility recomposition. **Branch logic:** none.
**Formal map:** EGZ lines 139-145. **Trust boundary:** imported body.
**Step ledger:** `STEP-M0931-T-COMPOSITE-ASSEMBLE-01`. **Boundary:** exact child
harness pending. **Status vector:** `[H1, M4, R4]`.

### m0931-x-source

**Claim:** Every material mathematical transition must map to a pinpointed,
reviewed primary-source record. **Role:** H-axis boundary. **Inputs:** 1961 scan,
correction audit, and node map. **Proof route:** compare its prime and
multiplicative proof with this architecture. **Branch logic:** prime/composite.
**Formal map:** source crosswalk. **Trust boundary:** mathlib's Chevalley-Warning
route is not silently attributed to the paper. **Step ledger:**
`STEP-M0931-X-SOURCE-01`. **Boundary:** independent H0 review is open.
**Status vector:** `[H1, M4, R4]`.

### m0931-x-provenance

**Claim:** Wrapper, indexed body, private prime route, Chevalley-Warning body,
imports, revisions, blobs, and license must be bound without duplicate credit.
**Role:** provenance gate. **Inputs:** exact declaration closure. **Proof route:**
trace all terminal bodies transitively. **Branch logic:** local, mathlib, and
shared-body classes. **Formal map:** anchor audit. **Trust boundary:** current
inventory is not a release closure. **Step ledger:**
`STEP-M0931-X-PROVENANCE-01`. **Boundary:** open.
**Status vector:** `[H1, M4, R4]`.

### m0931-x-trust

**Claim:** Executables, compiled artifacts, axioms, unsafe/oracle boundaries,
and supply-chain inputs require hermetic audit. **Role:** release trust gate.
**Inputs:** complete TCB closure. **Proof route:** cold replay and policy check.
**Branch logic:** allowed or rejected boundary. **Formal map:** future trust
receipt. **Trust boundary:** warm shared `.lake` evidence is nonrelease.
**Step ledger:** `STEP-M0931-X-TRUST-01`. **Boundary:** open.
**Status vector:** `[H1, M4, R4]`.

### m0931-x-readable

**Claim:** A reader must be able to follow every prime and composite step and
its formal anchor. **Role:** R-axis gate. **Inputs:** the full node ledger and
independent reader. **Proof route:** expand high-risk packages and review the
claim flow. **Branch logic:** prime/composite and all nested branches.
**Formal map:** this file plus a future long reconstruction. **Trust boundary:**
file existence is not R0. **Step ledger:** `STEP-M0931-X-READABLE-01`.
**Boundary:** independent review is open. **Status vector:** `[H1, M4, R4]`.

### m0931-x-workflow

**Claim:** Proof, validation, release, freshness, revocation, and independent
verification must follow the typed task order. **Role:** workflow gate.
**Inputs:** accepted node receipts. **Proof route:** dependency-legal acceptance
and invalidation propagation. **Branch logic:** audit and theorem decisions are
separate. **Formal map:** rev-5.6 execution DAG. **Trust boundary:** workflow
cannot prove mathematics. **Step ledger:** `STEP-M0931-X-WORKFLOW-01`.
**Boundary:** every downstream phase is open. **Status vector:**
`[H1, M4, R4]`.

## Status boundary

The authoritative root remains `H1/M3/R4`, with zero accepted obligations,
`audit_complete=false`, and `theorem_complete=false`. This phase claims no
proof adoption, H0, accepted M0, R0, release evidence, `AUDIT-Z`, `THEOREM-Z`,
or master acceptance.
