# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6728-6733`, introduced in repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, contains the entire source record:

- title: `安德鲁斯分裂定理`;
- attribution: George Andrews;
- year: 1974;
- statement gloss: `分拆函数的进一步推广`;
- importance: high; and
- formalization status: `已验证`.

`Docs/Stage0_Blueprint.md:25093-25118` repeats the gloss while explicitly leaving the exact
definitions and premises, proof route, dependencies, equivalent formulations, axioms, machine
status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Literal crosswalk

| Repository element | Required mathematical component | Prospective Lean component | Intake result |
|---|---|---|---|
| `安德鲁斯分裂定理` | stable English identity and named result | canonical declaration identity and provenance | unresolved; `分裂` may be a mistranslation of partition terminology |
| George Andrews, 1974 | one exact work, edition, theorem, and page | pinned source revision | several related 1974 publications exist; none cited |
| "further generalization" | exact antecedent and relationship | checked equality, `Iff`, implication, or specialization transport | antecedent and direction absent |
| "partition function" | ordinary or restricted partitions and their conditions | `Nat.Partition`, restricted finite sets, or source-specific definitions | domain and restrictions absent |
| theorem conclusion | coefficient equality, series/product identity, congruence, or other result | one exact `Prop` with ordered binders | absent |
| `已验证` | accepted human-source and kernel evidence | accepted receipts | explicitly rejected as evidence |

## Strong primary-source lead

George E. Andrews, "An Analytic Generalization of the Rogers-Ramanujan Identities for Odd
Moduli," *Proceedings of the National Academy of Sciences of the United States of America* 71(10),
October 1974, pages 4082-4085, DOI `10.1073/pnas.71.10.4082`, is the strongest inspected lead.
PubMed Central record `PMC434332` exposes page images of the article.

The abstract says that a `(k-1)`-fold Eulerian series expansion is given for the reciprocal product
over positive integers whose exponents are not congruent to `0`, `i`, or `-i` modulo `2*k+1`, and
that the two Rogers-Ramanujan identities occur at the stated small parameter choices. Theorem 1 on
page 4082 gives the full multiple-series/product identity for `1 <= i <= k`; Section 2 proves it on
pages 4083-4084. This strongly matches the author, year, subject, and immediate catalog sequence.

It is not adopted. The catalog does not cite the article, does not say "odd moduli" or
"Rogers-Ramanujan," and does not distinguish its analytic Theorem 1 from a combinatorial
coefficient statement. Intake inspected the article to discriminate scope, but no complete
definition/premise/errata crosswalk, durable admitted source packet, or independent review exists.
Accordingly it is not H0 evidence and supplies no canonical root.

## Competing 1974 source boundary

Crossref DOI metadata identifies George E. Andrews, *On the general Rogers-Ramanujan theorem*,
Memoirs of the American Mathematical Society 152 (1974), DOI `10.1090/memo/0152`. Crossref also
returns other related Andrews works from 1974. This demonstrates that author, year, and broad topic
do not uniquely select the PNAS theorem. An independently reviewed catalog correction or source
admission must choose the exact work and result before statement elaboration.

## Formal crosswalk boundary

| Candidate source component | Prospective Lean surface | Status |
|---|---|---|
| ordinary integer partitions | `Nat.Partition n` and its `Fintype` | pinned API elaborated; not root evidence |
| source-selected restricted partitions | `Nat.Partition.restricted n p` plus exact predicate `p` | generic API only; predicate and combinatorial conditions open |
| partition generating function | `Nat.Partition.genFun`, `coeff_genFun`, `hasProd_genFun` | generic substrate only |
| excluded residue classes modulo `2*k+1` | `Nat.ModEq` or remainder predicates | congruence API only; exact source encoding open |
| source-specific multiple sum and infinite product | finite/infinite sums, products, power series, or analytic `q`-series | no source-identical expression or theorem located |
| analytic-to-combinatorial equivalence | coefficient extraction and checked transports | absent |

A bounded case-insensitive search in repository-local Lean and pinned mathlib found no
Andrews-Gordon or general Rogers-Ramanujan declaration. This is intake discovery only, not the
downstream immutable anchor audit or a global absence claim.

## Required statement admission

Before `S56-M-0920-STATEMENT` may elaborate a target, accountable reviewers must correct or confirm
the title, select and preserve one authoritative source edition and exact result, transcribe all
definitions and ordered binders, map every premise and conclusion, audit corrections and errata,
resolve analytic versus combinatorial scope and every boundary case, and justify the relationship
to `THM-M-0918` and `THM-M-0919`. Only then may the Lean expression, minimal imports, environment
fingerprint, checked transports, and required statement mutations be frozen.
