# THM-M-0901 rev-5.6 intake

`THM-M-0901` is the combinatorics catalog item `拉丁方` (Latin squares). The catalog supplies only
the compound gloss `拉丁方的存在性与计数` (existence and counting of Latin squares), an
attribution to many mathematicians, the twentieth century, and an untrusted `已验证` (verified)
label. Those fields identify a subject family, not one proposition with fixed binders and a
truth-valued conclusion.

## Intake result

This dossier records a fail-closed `planned` instance. It does not choose a familiar theorem from
memory. The existence half could mean existence at every positive order, completion or embedding
of partial squares, or existence of orthogonal squares. The counting half could mean the total or
reduced number at a fixed order, an exact formula, finite enumerations, asymptotic bounds, or counts
modulo isomorphism, isotopy, or paratopy. Combining a convenient existence construction with one
unrelated enumeration theorem would manufacture a compound root that the catalog never states.

McKay and Wanless, *On the Number of Latin Squares*, is an inspected authoritative counting source
lead. It supplies a precise finite-array definition and several distinct enumeration results, while
also stating that the asymptotic value of the number of reduced squares was unknown at writing. A
Marshall Hall paper is a bibliographic existence lead, but its theorem text was not inspected.
These leads demonstrate rather than resolve the catalog ambiguity, so neither is selected as the
canonical root or credited as `H0`.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned matrix, finite-type, bijection, and cardinality APIs.
A bounded repo-local and pinned-mathlib search found no declaration named for Latin squares or
quasigroups. The probe and search are intake discovery only, not the downstream formal-anchor audit.

The canonical mathematical statement and Lean expression remain null. The provisional vector is
`[H5, M4, R4]`: `H5` classifies the received compound wording as not yet a stable proposition, not
as a claim that standard Latin-square theorems are false; no usable formal artifact for an exact
root is credited; and no proof reconstruction can attach before that root is selected. All six
downstream tasks remain open. No accepted proof state, audit completion, theorem completion, or
master acceptance is claimed.
