# Source-statement crosswalk

Primary-source candidate: Robin Hartshorne, *Algebraic Geometry*, Graduate Texts in Mathematics 52,
Springer (1977), Chapter IV, Section 1, Theorem 1.3. This is a discovery citation, not accepted `H0`
evidence; printed page, edition identity, exact assumptions, definitions, and errata remain unaudited.

| Canonical component | Candidate source locus | Intended Lean surface | Intake disposition |
|---|---|---|---|
| nonsingular projective curve and divisor `D` | Chapter IV, Section 1 setup and Theorem 1.3 | scheme/curve plus divisor structures | mapped in prose; exact predicates open |
| canonical divisor `K_X` | terminology preceding Theorem 1.3 | canonical sheaf/divisor representation | source definition and bridge open |
| `l(E)` | divisor linear-system notation in Section 1 | finite dimension of global sections | cohomology and finiteness API open |
| genus `g` and degree | Section 1 conventions | genus and divisor-degree APIs | conventions/coercions open |
| `l(D)-l(K-D)=deg D+1-g` | Theorem 1.3 | no declaration selected | exact elaboration deferred |
| arbitrary-field, geometrically integral normalization | modern scheme-level scope used by this intake | explicit hypotheses | requires a checked source bridge |

The repository metadata phrase "divisor dimension formula on an algebraic curve" does not specify
field conventions, smoothness, projectivity, geometric integrality, or the divisor model. Those are
not silently erased; they are explicit scope decisions awaiting source audit. No claim is made that
mathlib already contains the theorem. The anchor audit must record exact module, declaration, type,
revision, dependency feasibility, proof-body provenance, and trust boundary for every candidate.
