# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` names `共鸣定理`, attributes it to Stefan Banach, dates it to
1929, and gives only the sentence `算子点态有界则一致有界` ("pointwise bounded operators are
uniformly bounded"). `Docs/Stage0_Blueprint.md` repeats that gloss and explicitly leaves precise
definitions, assumptions, proof route, equivalent formulations, axioms, and machine artifacts open.
The manifest preserves `已验证` only as `source_status_untrusted`.

This metadata fixes the conventional theorem family but is not a primary proof source. Intake did
not identify an immutable edition, theorem/page locator, exact historical wording, assumptions,
errata, or an independent source review. Accordingly the human axis is `H1`, not `H0`.

## Crosswalk

| Repository phrase | Frozen mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "operators" | continuous semilinear maps between normed spaces | `E ->SL[sigma12] F` | candidate type checked |
| "pointwise bounded" | for every `x`, one real bound works for all family indices | `forall x, exists C, forall i, norm (g i x) <= C` | scope frozen; exact expression open |
| domain condition | Banach domain | `[CompleteSpace E]` | required, absent from repository gloss |
| "uniformly bounded" | one real bound on all operator norms | `exists C', forall i, norm (g i) <= C'` | scope frozen; exact expression open |
| `已验证` | untrusted inventory label | no proposition or proof term | explicitly no proof credit |

## Formal-source lead

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib/Analysis/Normed/Operator/BanachSteinhaus.lean` publicly declares `banach_steinhaus` with
the scoped premise and conclusion above. It also declares `banach_steinhaus_iSup_nnnorm` and cites a
more general barrelled-space theorem. These are formal candidates, not human-source evidence. Exact
expression comparison, terminal-body provenance, transitive dependencies, axioms, placeholders,
and wrapper eligibility belong to later statement and anchor-audit phases.

## Required source work

The source audit must select and independently inspect a primary or authoritative proof source,
record edition, theorem and page, map every assumption and conclusion component, check errata and
historical naming/attribution, and align its scalar/linearity conventions with the canonical root.
