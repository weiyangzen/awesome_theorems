# Source-statement crosswalk

## Repository record and provenance

| Surface | Exact content | Intake assessment |
|---|---|---|
| `Docs/researches/math_theorems.md:5549-5554` | `跳跃反演定理`; proposers `众多数学家`; time `20世纪`; statement `跳跃算子的像`; importance `高`; status `已验证` | The six lines originate at commit `bcf3f9fa...`; title and gloss identify a theorem family but not a binder-complete proposition |
| `Docs/Stage0_Blueprint.md:20569-20592` | Repeats the title/gloss; exact definitions, premises, proof route, equivalences, axioms, and formal artifact are all `待补充` | Confirms that Stage0 did not freeze a theorem; its generic planning prose supplies no missing mathematics |
| `Docs/Stage1_Targets_rev-5.6.json` | rank 1339, L0/rework-required, planned, no accepted legacy artifact, theorem incomplete | Membership and scheduling authority only; the copied `已验证` value is explicitly untrusted |

## Statement candidates and gaps

| Claim component | Source lead | Prospective Lean surface | Intake boundary |
|---|---|---|---|
| Degree carrier and order | Encyclopedia entry defines Turing degrees using Turing reducibility on sets or relative-recursive functions | pinned `TuringDegree` over partial functions and its `PartialOrder` | Candidate model only; representative transport and source selection are open |
| Jump | Entry describes `a'` as the greatest degree recursively enumerable relative to `a` | no jump definition found in the inspected pinned module | Definition, representative invariance, and exact formal encoding are missing |
| Lower range bound | Entry states the inversion premise `a >= 0'` | would require least degree, jump, and order | Catalog omits this material premise; it cannot be inferred into the root without source acceptance |
| Inversion conclusion | Entry states existence of `b` such that `a = b'` | no canonical expression or candidate declaration | Strong secondary statement lead only; no primary theorem/proof mapping or Lean target |
| Variant | Catalog says only "image of the jump operator" | ordinary, relative, iterated, c.e.-restricted, and other degree variants are possible | Exact variant and neighbor ownership unresolved |
| `已验证` | Untrusted repository metadata | no expression or proof object | No H or M credit |

## Inspected source lead

An immutable API response for Encyclopedia of Mathematics article `Degree of undecidability`,
revision `46619` dated 2020-06-05, was inspected and hashed as
`547f7674b5e8071d5ce56a79ed8d77fcd431f25b79b57ec93e75c6967ab31224`. It says:
for every degree `a >= 0'` there is a degree `b` such that `a = b'`. Its reference list gives H.
Rogers Jr., *Theory of Recursive Functions and Effective Computability* (1967), J. Shoenfield,
*Degrees of Unsolvability* (1971), and G. E. Sacks, *Degrees of Unsolvability* (1963) for the
surrounding theory.

The exact replay URL is
`https://encyclopediaofmath.org/api.php?action=query&prop=revisions&revids=46619&rvprop=ids%7Ctimestamp%7Ccontent&rvslots=main&format=json&formatversion=2`.
The validation record gives the bounded retrieval command; replay on 2026-07-13 reproduced the
same 6,850-byte response and SHA-256.

This is an authoritative secondary source, not H0. The referenced books were not obtained and no
edition/page/theorem containing the exact result or proof was inspected. The entry does not supply
a pinpoint citation for the inversion sentence, a full premise-to-conclusion proof crosswalk, an
errata audit, or independent review. The catalog's vague attribution `众多数学家` also remains
unreconciled with the conventional name "Friedberg jump inversion theorem."

## Formal crosswalk

At the pinned revision, `Mathlib.Computability.TuringDegree` imports the oracle-recursion substrate
and defines Turing reducibility/equivalence and degrees. `IntakeProbe.lean` re-elaborates those exact
declarations. The module contains no Turing-jump definition, zero-jump term, range theorem, or jump
inversion proof. Consequently it supports only the prospective degree-model row above.

Before leaving `H1`, reviewers must pin and inspect a primary source; record its exact edition,
theorem/section/page, incorporated definitions, all assumptions, proof and correction boundary;
decide the theorem variant and target ownership; and independently approve the component mapping.
Only then may the statement phase choose minimal imports, define or select the jump, elaborate and
hash an exact expression, check transports, and mutation-test the lower-bound premise, domain,
binder scope, and boundary degrees. Until then the exact-source and exact-statement gates remain
open, with no proof credit.
