# THM-M-1592 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog item `Reed-Solomon码`
(`Reed-Solomon codes`). The authoritative mathematics record supplies only the gloss `MDS码`, an
attribution to Reed and Solomon, the year 1960, and an untrusted `已验证` label. Those fields identify
a coding-theory family, but they do not identify a binder-complete mathematical proposition.

## Intake result

Bibliographic metadata confirms a primary-source lead: I. S. Reed and G. Solomon, "Polynomial
Codes Over Certain Finite Fields," *Journal of the Society for Industrial and Applied Mathematics*
8(2), 1960, pages 300-304, DOI `10.1137/0108018`. The paper text was not available through the
publisher endpoint in this worker run, and the repository cites neither that paper nor a pinpoint
result. Consequently, the lead does not settle whether the target is an evaluation-code
construction, injectivity and dimension, minimum distance, equality in the Singleton bound, an
error-correction guarantee, a decoding result, or some bundle of these claims.

This intake therefore preserves the ambiguity rather than silently choosing the familiar modern
`[n, k, n-k+1]` theorem. The separate Stage0 computer-science item `THM-C-0381` uses the broader
gloss `MDS码的构造`; it is contextual duplicate provenance, not authority to change this target.

## Formal boundary

`IntakeProbe.lean` checks only pinned Hamming, polynomial-root, and Vandermonde-matrix APIs adjacent
to a possible evaluation-code encoding. A bounded exact-topic search found no Reed-Solomon or MDS
code declaration in repo-local Lean or pinned mathlib. These are discovery observations, not an
exhaustive anchor audit, a canonical code definition, a statement match, or a proof body.

The provisional root vector is `[H1, M4, R4]`: a credible primary-source family is known, but exact
source-to-root selection, assumptions, proof/errata mapping, and independent review remain open; no
usable exact formal artifact is credited; and no readable proof can attach to an unfrozen root. All
six downstream tasks remain open. No canonical Lean expression, H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
