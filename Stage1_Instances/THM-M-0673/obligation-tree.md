# THM-M-0673 frozen obligation architecture

Item: `S56-M-0673-OBLIGATION_TREE`. Registry version: 1. Freeze date: 2026-07-15.

The denominator contains 28 stable semantic obligations frozen from the exact statement and the
source-visible pinned route before proof-phase credit. The sentence and formula declarations are
terminal wrappers over one bounded-formula induction and do not earn duplicate proof-body credit.

## Root and statement layer

<a id="m0673-root"></a> `M0673-ROOT` is exactly the sentence satisfaction biconditional in
`Stage1Instances.THM_M_0673.LosSentenceTarget`.

<a id="m0673-s-interface"></a> `M0673-S-INTERFACE` owns all universes, the arbitrary index and
factor families, the ultrafilter, structure and nonempty instances, and the universal sentence
binder. <a id="m0673-s-boundary"></a> `M0673-S-BOUNDARY` keeps principal and nonprincipal
ultrafilters, arbitrary index types, empty languages, nullary symbols, and quantified sentences in
scope. <a id="m0673-s-foundation"></a> `M0673-S-FOUNDATION` records the open policy boundary for
`propext`, `Classical.choice`, `Quot.sound`, the kernel, and the no-oracle computation profile.

No normalization layer occurs before proof: the canonical target already uses mathlib's filter
product quotient. That exclusion and the absence of computation remain pending independent review.

## Terminal route

<a id="m0673-t-adapter"></a> `M0673-T-ADAPTER` conditionally maps the exact sentence interface to
the root. <a id="m0673-a-sentence"></a> `M0673-A-SENTENCE` removes the unique assignment of an empty
free-variable type. <a id="m0673-a-formula"></a> `M0673-A-FORMULA` specializes bounded formulas to
zero in-scope bound variables. <a id="m0673-a-bounded"></a> `M0673-A-BOUNDED` is the substantive
structural induction on all bounded formulas. `ObligationTree.lean` checks only the first three
child-to-parent compositions with the bounded package left as an explicit premise.

## Structural induction

<a id="m0673-b-falsum"></a> `M0673-B-FALSUM` uses eventual constancy in a proper filter.
<a id="m0673-b-equality"></a> `M0673-B-EQUALITY` transports term values and quotient equality.
<a id="m0673-b-relation"></a> `M0673-B-RELATION` transports term values and quotient relation
semantics. <a id="m0673-b-implication"></a> `M0673-B-IMPLICATION` uses the ultrafilter implication
biconditional. <a id="m0673-b-universal"></a> `M0673-B-UNIVERSAL` expands the quantifier argument
through quotient representatives, assignment extension, factorwise witness choice, and eventual
set monotonicity. These are all proof-relevant branches; none may be hidden by the short invocation
of `sentence_realize`.

## Semantic support

<a id="m0673-t-term"></a> `M0673-T-TERM` owns term evaluation through the quotient injection.
<a id="m0673-c-prestructure"></a> `M0673-C-PRESTRUCTURE` owns the induced quotient structure and its
well-definedness. <a id="m0673-l-funmap"></a> `M0673-L-FUNMAP` owns function-symbol compatibility.
<a id="m0673-l-quot-eq"></a> `M0673-L-QUOT-EQ` owns equality of quotient classes.
<a id="m0673-l-quot-rel"></a> `M0673-L-QUOT-REL` owns relation-symbol compatibility.
<a id="m0673-l-ultrafilter-imp"></a> `M0673-L-ULTRAFILTER-IMP` owns eventual implication.

<a id="m0673-l-quot-forall"></a> `M0673-L-QUOT-FORALL` moves universal quantification to quotient
representatives. <a id="m0673-t-snoc"></a> `M0673-T-SNOC` owns the factorwise `Fin.snoc` assignment
identity. <a id="m0673-c-epsilon"></a> `M0673-C-EPSILON` owns the factorwise classical
counterexample choice. <a id="m0673-l-eventual-set"></a> `M0673-L-EVENTUAL-SET` owns the final
eventual-set containment step.

## Assurance boundaries

<a id="m0673-x-source"></a> `M0673-X-SOURCE` keeps the exact primary edition, theorem/page,
assumption, errata, and node review open. <a id="m0673-x-provenance"></a>
`M0673-X-PROVENANCE` must bind the unique terminal route and all source blobs without duplicate
credit. <a id="m0673-x-trust"></a> `M0673-X-TRUST` requires release-grade compiled-artifact,
license, TCB, replay, and independent trust closure. <a id="m0673-x-readable"></a>
`M0673-X-READABLE` requires a complete independently reviewed reconstruction; this architecture is
not R0. <a id="m0673-x-workflow"></a> `M0673-X-WORKFLOW` owns dependency, freshness, revocation,
validation, independent verification, and release acceptance.

## Closure boundary

The root cut set is `M0673-A-BOUNDED`, `M0673-S-FOUNDATION`, `M0673-X-SOURCE`,
`M0673-X-PROVENANCE`, `M0673-X-TRUST`, `M0673-X-READABLE`, and `M0673-X-WORKFLOW`. The exact pinned
mathlib route remains only an uninstalled `M0-W` candidate; every accepted obligation list is empty,
and the authoritative root remains `[H1, M3, R4]`. Proof integration, H0, R0, validation, release,
AUDIT-Z, and theorem completion are open.
