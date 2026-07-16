# Source-statement crosswalk

## Available provenance

The repository supplies attribution to Wei-Liang Chow, year 1949, the Chinese
name `周炜良引理`, and the gloss `代数簇的坐标环性质`. It supplies no publication,
edition, theorem number, page, quotation, assumptions, or errata record. The
statement phase therefore preserves `H4`; it does not invent a primary-source
citation or upgrade the untrusted `已验证` label.

## Conflict crosswalk

| Repository datum | Apparent meaning | Statement disposition |
|---|---|---|
| `周炜良引理` | conventionally, Chow's lemma | provisional name only |
| year 1949 | historical metadata | unverified; no source locator |
| coordinate-ring-properties gloss | an unspecified affine algebra claim | too vague to elaborate |
| algebraic-geometry category | broad subject placement | accepted metadata, not statement evidence |
| `已验证` | legacy source-status label | explicitly untrusted by rev-5.6 manifest |

## Legacy artifact boundary

`Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_033.lean` acknowledges the
same ambiguity. It contains checked wrappers for finite-type coordinate rings
and proposes a Chow-lemma-style scheme witness, but explicitly replaces the
projectivity slot with the weaker public properness predicate. Consequently:

- the coordinate-ring wrappers are auxiliary facts, not the unidentified root;
- the proposed `StatementShape` is not an exact Chow lemma statement;
- successful elaboration of that file gives no rev-5.6 statement or proof
  credit for `THM-M-0109`.

## Exact-statement boundary

The two candidate families are materially different. Scheme-theoretic Chow's
lemma concerns a projective model or modification under formulation-dependent
hypotheses. Finite generation, polynomial-quotient presentation, and
Noetherianity are coordinate-ring facts with different binders, premises, and
conclusions. Neither family is admitted by the repository record, and neither
may be substituted for the other.

The exact human claim, domains, ordered binders, hypotheses, conclusion,
boundary cases, canonical Lean expression, minimal imports, expression and
environment fingerprints, checked transports, and four required statement
mutations therefore remain unresolved. The statement gate fails closed before
proof evidence is inspected.

## Required resolution

Admit a stable primary publication or approved authoritative source with a
precise theorem locator. Reconcile its exact wording with both the repository
name and gloss, record incorporated definitions and every premise and boundary,
check corrections and errata, and obtain independent review. Only then may a
later statement worker encode that one claim, minimize its pinned imports,
fingerprint its elaborated expression and environment, check every credited
transport, and run all four mutation classes.

This crosswalk supplies no exact-statement, proof, phase-acceptance, `H0`,
`M0`, `AUDIT-Z`, or `THEOREM-Z` credit.
