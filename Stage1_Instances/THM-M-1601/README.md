# THM-M-1601 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `同态加密`
(`homomorphic encryption`). The repository supplies only the gloss `密文上的计算`, an attribution
to Craig Gentry, the year 2009, and an untrusted `已验证` label. Those fields identify a subject and
capability, not a binder-complete mathematical proposition.

## Intake result

Gentry's 2009 STOC paper *Fully Homomorphic Encryption Using Ideal Lattices* was inspected as a
primary source-family lead. It distinguishes correctness of evaluation, homomorphic encryption for
a permitted circuit class, full versus leveled homomorphism, bootstrappability, a general
bootstrapping theorem, correctness of one ideal-lattice construction, and a conditional construction
of a bootstrappable scheme. The catalog cites and selects none of these distinct claims.

This intake therefore preserves the ambiguity. It does not silently replace the target by a
`RingHom` law, a correctness-by-definition interface, an additive or multiplicative special case, a
fixed-circuit example, a bootstrapping theorem, or the separate Stage0 computer-science FHE record.
The source phase must select one immutable proposition and crosswalk its scheme, circuit,
correctness, compactness, security, complexity, probability, and boundary conventions before Lean
statement elaboration.

## Formal boundary

`IntakeProbe.lean` checks only pinned operation-preservation and commuting-diagram APIs adjacent to
a possible future correctness encoding. A bounded repository and pinned-mathlib search found no
lexical homomorphic-encryption declaration. These are discovery observations, not an exhaustive
anchor audit. They establish neither a cryptosystem definition nor a canonical theorem or proof
body.

The provisional root vector is `[H5, M4, R4]`: the literal repository target is not one stable
proposition, so ordinary proof execution is blocked pending an approved source correction; no
usable exact formal artifact is credited; and no readable proof can be reconstructed against an
unfrozen root. The published source family itself is not being classified as false or open and must
be reclassified after root selection. All six downstream tasks remain open. No canonical Lean
expression, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.

The open `STATEMENT` task begins with the target-correction or redirection decision. The five later
ordinary execution tasks are recorded for workflow completeness but remain dependency-blocked; an
open row is not permission to prove a convenient member of the source family.
