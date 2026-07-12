# THM-M-0721 frozen obligation tree

This is an architecture freeze, not an NP-completeness proof. All open semantic packages remain `unchecked`.

## m0721-root

**There exists a binary-word language in the frozen verifier-based NP that is polynomial-time many-one hard for every such NP language.**

Formal target: `Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage`  
Debt: `H1 / M3 / R4`; budget: `100`; state: `unchecked`.

Output: Stage1Instances.THM_M_0721.ExistsNPCompleteLanguage

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-s-definitions

**Freeze Word, Language, encodings, verifier-based InNP, TM2 polynomial time, reductions, and NPComplete.**

Formal target: `Stage1Instances.THM_M_0721.{Word,Language,encodePair,InNP,PolyManyOneReducible,NPComplete}`  
Debt: `H1 / M0-L / R4`; budget: `40`; state: `provisional checked interface`.

Output: The elaborated statement interface and its exact encodings.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-s-boundary

**Preserve the binary alphabet, empty input and certificate, separator pairing, and zero-bound behavior.**

Formal target: `Stage1Instances.THM_M_0721.{binary_alphabet_has_two_distinct_symbols,encodePair_empty_empty,empty_certificate_is_in_boundary}`  
Debt: `H1 / M0-L / R4`; budget: `40`; state: `provisional checked interface`.

Output: Checked encoding boundary facts.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-s-foundation

**Audit classical principles, terminal axioms, imports, TCB, and the no-oracle policy.**

Formal target: `planned exact axiom and transitive import report`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: An accepted transitive foundation and trust report.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-n-sat-encoding

**Define faithful Boolean formula syntax plus total binary encoders and decoders for formulas, assignments, and verifier pairs.**

Formal target: `planned Lean SAT syntax, encoding, decoding, and round-trip signatures`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: A concrete binary-word satisfiability language with encoding invariants.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-c-sat-verifier

**Construct the deterministic TM2 verifier that decodes a formula and assignment and evaluates satisfaction.**

Formal target: `planned TM2 verifier construction`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: A verifier function and implementing machine.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-l-sat-correct

**Prove the verifier accepts exactly the satisfying assignments of the decoded formula.**

Formal target: `planned verifier correctness theorem`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: Verifier soundness and completeness for SAT membership.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-l-sat-runtime

**Prove the SAT verifier TM2 runs in polynomial time under the frozen pair encoding.**

Formal target: `planned verifier runtime theorem`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: TM2ComputableInPolyTime evidence for the verifier.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-t-sat-in-np

**Assemble decoding, certificate length, verifier correctness, and runtime into InNP for the candidate language.**

Formal target: `planned Stage1Instances.THM_M_0721.sat_in_np`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: CandidateMembership for the chosen SAT language.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-n-machine-normalize

**Normalize an arbitrary frozen InNP verifier, its polynomial certificate bound, and input into a bounded computation instance.**

Formal target: `planned verifier-to-bounded-computation normalization`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: A uniform bounded TM2 computation description.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-c-tableau

**Construct variables and local constraints encoding the normalized accepting computation tableau.**

Formal target: `planned Cook-Levin tableau construction`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: A finite tableau constraint system with well-formed indices and local invariants.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-l-tableau-sound

**Decode any satisfying tableau assignment into an accepting verifier computation and a certificate within the frozen bound.**

Formal target: `planned tableau soundness theorem`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: Formula satisfiability implies source-language membership.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-l-tableau-complete

**Encode any bounded accepting verifier computation as a satisfying tableau assignment.**

Formal target: `planned tableau completeness theorem`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: Source-language membership implies formula satisfiability.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-l-reduction-runtime

**Prove construction and binary serialization of the tableau formula are performed by a TM2 in polynomial time.**

Formal target: `planned Cook-Levin reduction runtime theorem`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: PolytimeFunction evidence for the reduction.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-t-universal-hardness

**For every frozen InNP source, assemble the tableau construction, two correctness directions, and runtime into a many-one reduction to SAT.**

Formal target: `planned Stage1Instances.THM_M_0721.sat_hard`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: CandidateHardness for the same candidate language.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-t-assemble

**Combine candidate membership and universal hardness without adding a premise.**

Formal target: `Stage1Instances.THM_M_0721.root_of_candidate_packages`  
Debt: `H1 / M0-L / R4`; budget: `40`; state: `provisional checked interface`.

Output: The exact existential NP-completeness target.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-x-source

**Pin primary Cook-Levin and NP-completeness sources and map each proof node to exact assumptions and proof passages.**

Formal target: `planned primary-source node crosswalk`  
Debt: `H1 / M4 / R4`; budget: `40`; state: `unchecked`.

Output: Human-source coverage; no machine proof credit.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

## m0721-x-provenance

**Inventory terminal bodies, wrappers, imports, placeholders, axioms, and replay evidence.**

Formal target: `planned terminal-body provenance ledger`  
Debt: `H1 / M4 / R4`; budget: `100`; state: `unchecked`.

Output: Release provenance coverage; no mathematical proof credit.

Boundary: Frozen architecture or conditional interface only; no unlisted premise and no root closure is supplied.

