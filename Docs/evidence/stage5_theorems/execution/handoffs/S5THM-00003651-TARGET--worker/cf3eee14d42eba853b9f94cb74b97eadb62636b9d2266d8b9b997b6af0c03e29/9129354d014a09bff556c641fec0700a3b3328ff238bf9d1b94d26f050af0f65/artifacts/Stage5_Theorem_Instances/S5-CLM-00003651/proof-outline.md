# Distilled proof outline — S5-CLM-00003651

## A0 — frozen proposition anchor

The frozen source declaration is identified byte-for-byte and its type is restated without changing the predicate.

- Hypotheses: the pinned Formal Conjectures file and exact declaration locator.
- Inference: retain only the source type as a statement anchor.
- Output: the source-side proposition lock.
- Formal anchor: `Erdos1074.erdos_1074.variants.EHSNumbers_infinite`.
- Downstream use: A1.
- Exceptional case: the provider body contains `sorry` and therefore contributes no proof closure.
- Trust boundary: source provenance is not an executable target import.

## A1 — claim-owned direct target

The local statement theorem establishes reflexive equality of the direct target proposition.

- Hypotheses: the source type anchor from A0.
- Inference: spell the same set predicate directly over natural numbers.
- Output: the claim-owned target proposition.
- Formal anchor: `ehsNumbersInfinite_statement_iff`.
- Downstream use: A2.
- Exceptional case: no local abbreviation, notation, syntax, macro, coercion, or alias is introduced.
- Trust boundary: only `Mathlib` is an executable import.

## A2 — root transport

The proof surface transports a verified root across the direct target proposition without provider-body invocation.

- Hypotheses: a verified instance of the direct target proposition.
- Inference: transparent identity transport.
- Output: the same target proposition.
- Formal anchor: `ehsNumbersInfinite_from_verified_root`.
- Downstream use: A3.
- Exceptional case: the provider theorem is never invoked as a proof term.
- Trust boundary: exact root closure remains subject to Master trust-zero replay.

## A3 — reverse audit

The audit surface reverses the same proposition-preserving transport and exposes the replay anchor.

- Hypotheses: the target proposition transported at A2.
- Inference: simplification over an identical proposition.
- Output: reverse crosswalk witness.
- Formal anchor: `ehsNumbersInfinite_round_trip`.
- Downstream use: validates A0/A1 provenance consistency.
- Exceptional case: no source symbol is shadowed or reinterpreted.
- Trust boundary: audit evidence does not self-accept the theorem.
