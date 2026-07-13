# THM-M-1589 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `线性码`
(`linear codes`). The repository supplies only the gloss `线性纠错码` ("linear
error-correcting codes"), attributes the topic to many mathematicians in the twentieth century,
and carries an untrusted `已验证` label. Those fields name a mathematical object and subject,
not a binder-complete truth-valued proposition.

## Intake result

The intake preserves that boundary instead of choosing a familiar theorem. A linear code may be
defined as a finite-field subspace of a word space, but the definition is not itself a theorem.
Possible results include generator-matrix representation, parity-check kernel characterization,
dimension or cardinality, equality of minimum distance and minimum nonzero Hamming weight,
systematic form, dual-code identities, or an encoding and decoding guarantee. These have different
domains, assumptions, conclusions, and degenerate cases. The catalog selects none.

Venkatesan Guruswami's 2010 introductory coding-theory notes were inspected as a modern source
lead. Definitions 7 and 8 and the subsequent exercises and lemmas confirm the distinct definition,
generator, parity-check, distance, and duality surfaces. The notes are not repository-cited, do not
select a canonical root for this target, and receive no H0 credit.

## Formal boundary

`IntakeProbe.lean` checks only pinned Hamming-distance, Hamming-weight, submodule, and matrix-vector
APIs adjacent to a possible future encoding. A bounded repository and pinned-mathlib search found
no exact linear-code declaration under the recorded terms. These observations are discovery-only,
not an exhaustive anchor audit, and establish neither a canonical code definition nor a theorem or
proof body.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the received noun phrase as not yet
a stable proposition; it does not refute standard linear-code theorems. No usable exact formal
artifact or proof reconstruction is credited. All six downstream tasks remain open. No canonical
Lean expression, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
