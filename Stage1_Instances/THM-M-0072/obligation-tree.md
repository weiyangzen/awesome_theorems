# THM-M-0072 obligation tree

This is the version-1 frozen architecture for Thompson's transfer lemma. It follows the proof of
Lemma 5.38(a)(i), printed page 411: transfer from `G` to `S/M`, parity of fixed Sylow cosets, and a
contradiction with the absence of an index-two subgroup. Each record below is an architecture
ledger, not an accepted `H0` proof reconstruction. The transfer branch remains open.

## Root And Statement

<a id="m0072-root"></a>
### `M0072-ROOT` - root
Exact printed universal target. It requires `M0072-T-ASSEMBLE`; current vector `H1/M3/R4`.

<a id="m0072-s-target"></a>
### `M0072-S-TARGET` - definition
Preserve the exact universes, binders, premises, nested coercions, and ambient conjugacy conclusion.

<a id="m0072-s-domain"></a>
### `M0072-S-DOMAIN` - definition
Keep finite even-order `G`, literal absence of every index-two subgroup, `S : Sylow 2 G`, maximal
proper `M : Subgroup S`, and exact order-two `u : S`.

<a id="m0072-s-boundary"></a>
### `M0072-S-BOUNDARY` - branch
Separate `u in M`, where self-conjugacy works, from `u notin M`, where transfer is required.

<a id="m0072-s-transport"></a>
### `M0072-S-TRANSPORT` - transport
Use the statement-phase checked equivalence between the printed universal form and the common
outside-maximal form. It changes no premise and earns no duplicate root credit.

<a id="m0072-s-foundation"></a>
### `M0072-S-FOUNDATION` - certificate
Lean 4 dependent type theory and pinned mathlib are the selected foundation. Full transitive axiom,
dependency, and TCB acceptance remains downstream; no computation or oracle is credited.

## Reduction And Branches

<a id="m0072-n-outside"></a>
### `M0072-N-OUTSIDE` - reduction
Fix an involution outside `M`. This is the exact nontrivial branch, not a stronger perfect-group or
fusion-system substitute.

<a id="m0072-b-membership"></a>
### `M0072-B-MEMBERSHIP` - branch
The membership split is exhaustive. `ObligationTree.lean` checks that both exact branch products
compose into the printed universal proposition.

<a id="m0072-t-inside"></a>
### `M0072-T-INSIDE` - terminal
For `u in M`, choose `u` itself as the witness. `insideMaximalConclusion` kernel-checks this leaf.

<a id="m0072-b-contradiction"></a>
### `M0072-B-CONTRADICTION` - branch
Assume no ambient conjugate of the outside involution lies in `M`. The transfer product will be
nontrivial, while the no-index-two premise forces it to be trivial.

## Quotient And Transfer

<a id="m0072-c-normal"></a>
### `M0072-C-NORMAL` - construction
Show that the maximal subgroup `M` of the finite 2-group `S` is normal. Exact Lean implementation
and its child composition are open.

<a id="m0072-l-index-two"></a>
### `M0072-L-INDEX-TWO` - core lemma
Show that the proper maximal subgroup `M` has index two in `S`. This is material: it makes `S/M`
the two-element transfer target and cannot be hidden inside a quotient constructor.

<a id="m0072-c-quotient"></a>
### `M0072-C-QUOTIENT` - construction
Construct `S/M`, its quotient map, and the nontrivial coset represented by the outside involution.
Normality and the index-two result are explicit children.

<a id="m0072-c-transfer"></a>
### `M0072-C-TRANSFER` - construction
Construct transfer `G -> S/M`. Pinned `MonoidHom.transfer` is audited substrate only; the required
normal quotient and the exact specialization to this theorem remain open.

<a id="m0072-l-sylow-odd"></a>
### `M0072-L-SYLOW-ODD` - core lemma
Use the Sylow property to establish that the index of `S` in `G` is odd.

<a id="m0072-c-coset-action"></a>
### `M0072-C-COSET-ACTION` - construction
Model left multiplication by the involution on the cosets of `S` in `G`, with nonfixed orbits of
size two and fixed cosets represented explicitly.

<a id="m0072-l-fixed-parity"></a>
### `M0072-L-FIXED-PARITY` - core lemma
Since the total number of Sylow cosets is odd and nonfixed orbits pair, the number of fixed cosets
is odd. The finite-action parity argument remains an exact planned Lean leaf.

<a id="m0072-l-transfer-formula"></a>
### `M0072-L-TRANSFER-FORMULA` - bridge
Specialize the pinned transfer orbit-product formula so `t(u)` is the product of factors indexed by
the fixed cosets. This deep imported boundary is not replaced by a short theorem call.

<a id="m0072-l-factor-dichotomy"></a>
### `M0072-L-FACTOR-DICHOTOMY` - core lemma
For each fixed coset representative `g`, identify its transfer factor with the quotient coset of an
ambient conjugate of `u`, and relate membership of that conjugate in `M` to the identity coset.

<a id="m0072-l-odd-product"></a>
### `M0072-L-ODD-PRODUCT` - core lemma
Under the no-conjugate-in-`M` assumption, every fixed-coset factor is the unique nontrivial element
of `S/M`; an odd product of those factors is nontrivial.

<a id="m0072-l-noindex-transfer"></a>
### `M0072-L-NOINDEX-TRANSFER` - core lemma
If transfer to the two-element quotient were nontrivial, its kernel would have index two in `G`.
The frozen ambient premise excludes that, so transfer is trivial.

## Terminals

<a id="m0072-t-outside"></a>
### `M0072-T-OUTSIDE` - terminal
Discharge the contradiction and produce an element of `M` ambient-conjugate to the outside
involution. This is the minimal open root cut; it remains an explicit hypothesis in the Lean harness.

<a id="m0072-t-assemble"></a>
### `M0072-T-ASSEMBLE` - terminal
Merge `M0072-T-INSIDE` and `M0072-T-OUTSIDE`. The conditional merge is kernel-checked, but no
accepted closure follows while the outside child is open.

## Assurance Boundaries

<a id="m0072-x-source"></a>
### `M0072-X-SOURCE` - terminal
Map premises and each transfer transition to Thompson 1968 Lemma 5.38(a)(i). Independent `H0`
review, correction/errata review, preservation, and the catalog's 1964/1968 conflict remain open.

<a id="m0072-x-provenance"></a>
### `M0072-X-PROVENANCE` - certificate
Track the local statement and conditional wrappers separately from pinned mathlib transfer/focal
substrate. No wrapper relocates or invents a terminal proof body.

<a id="m0072-x-trust"></a>
### `M0072-X-TRUST` - certificate
Bind imports, declarations, axioms, toolchain, and dependency revisions. Full transitive trust and
release evidence are not supplied by this warm worker check.

<a id="m0072-x-readable"></a>
### `M0072-X-READABLE` - terminal
Own the future detailed proof reconstruction and independent `R0` review. This architecture outline
is intentionally still `R4`.

<a id="m0072-x-workflow"></a>
### `M0072-X-WORKFLOW` - terminal
Bind every obligation to the obligation-tree/proof tasks and the authoritative seven-stage workflow.
Only the integration lane may accept receipts or advance state.

## Frozen Boundary

The registry has 28 unique obligations and a single minimal open machine cut,
`M0072-T-OUTSIDE`, expanded into ten open source-faithful packages. Twenty internal edges are
typed `logical_decomposition`, not checked composition. Accepted obligations and receipts remain
empty; the root remains `H1/M3/R4`; `audit_complete=false` and `theorem_complete=false`.
