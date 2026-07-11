# Source-statement crosswalk

## Available provenance

The repository supplies attribution to Wei-Liang Chow, year 1949, the Chinese
name `周炜良引理`, and the gloss `代数簇的坐标环性质`. It supplies no publication,
edition, theorem number, page, quotation, assumptions, or errata record. The
intake therefore records `H4`; it does not invent a primary-source citation or
upgrade the untrusted `已验证` label.

## Conflict crosswalk

| Repository datum | Apparent meaning | Intake disposition |
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

## Required source audit

The next source audit must locate a stable primary publication or a scholarly
source with a precise theorem locator, compare its exact wording to both the
name and gloss, record all hypotheses and terminology changes, check errata,
and obtain independent review. Only then can a node-specific crosswalk support
`H1` or `H0` and an exact Lean statement.
