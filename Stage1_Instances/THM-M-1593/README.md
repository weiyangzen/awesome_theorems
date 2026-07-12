# THM-M-1593 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `LDPC码`
(`low-density parity-check codes`). The repository supplies only the gloss `低密度奇偶校验码`,
an attribution to Robert Gallager, the year 1963, and an untrusted `已验证` label. Those fields name
a code family. They do not identify a binder-complete mathematical proposition.

## Intake result

Gallager's 1963 monograph *Low-Density Parity-Check Codes* was inspected as an authoritative source
lead. Its opening chapter defines a regular binary low-density parity-check ensemble and summarizes
several materially different results: minimum-distance growth, maximum-likelihood error bounds,
comparisons with random codes, iterative decoding bounds, and decoder complexity. It also separates
proved bounds from a stronger decoding-performance hypothesis. The catalog cites none of these and
does not choose one as its root.

This intake therefore preserves the ambiguity. It does not silently replace the target by the
definition of a parity-check code, the elementary kernel identity for a matrix, a distance theorem,
a decoder-correctness theorem, or an asymptotic channel-performance theorem. The source phase must
select one immutable proposition and crosswalk all of its ensemble, channel, decoder, probability,
rate, and asymptotic conventions before statement elaboration.

## Formal boundary

`IntakeProbe.lean` checks only pinned Hamming-distance and matrix-vector APIs adjacent to a possible
future binary linear-code encoding. A bounded repository and pinned-mathlib search found no exact
LDPC declaration. These are discovery observations, not an exhaustive anchor audit. They establish
neither a canonical code definition nor a theorem or proof body.

The provisional root vector is `[H1, M4, R4]`: an authoritative primary source family with several
proved results is known, but exact source-to-root selection, full assumption and errata mapping, and
independent review remain open; no usable exact formal artifact is credited; and no readable proof
can be reconstructed against an unfrozen root. All six downstream tasks remain open. No canonical
Lean expression, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
