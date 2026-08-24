# Stage5 conjecture proof-search prompt extraction

## Pinned source

- Repository: `jinshanmu/CrouzeixConjecture`
- Commit: `f9d5c8d39bece41ceedf6346ef50ad1fb393260e`
- Source file: `crouzeix_conjecture_prompt.txt`
- Source-file SHA-256: `0a0c3000b81efc4d9edc65ec3cd1d53df0d4e69b24bfee9fe0860301d853d6fc`
- Source URL: <https://github.com/jinshanmu/CrouzeixConjecture/blob/f9d5c8d39bece41ceedf6346ef50ad1fb393260e/crouzeix_conjecture_prompt.txt>

This note extracts and paraphrases the reusable proof-search discipline from
the pinned prompt. It does not import the Crouzeix statement, its filesystem
paths, its affirmative-only orientation, or its multi-agent execution shape.
The upstream repository describes its result as a candidate proof, so this
extraction is a workflow input rather than mathematical evidence for any
Stage5 claim.

## What is unusually strong in the source prompt

1. It defines success as an exact end-to-end resolution, not an attractive
   reduction, finite experiment, or unproved theorem-strength lemma.
2. It begins with a genuinely diverse portfolio of mathematical mechanisms
   and protects early routes from premature convergence on one favored idea.
3. It keeps an explicit registry grouped by mathematical mechanism rather than
   superficial wording, so duplicate effort and neglected families are visible.
4. A route blocked on a missing lemma comparable in strength to the original
   problem is marked blocked and reopened only for a materially new mechanism.
5. Every search round must yield checkable mathematical objects: lemmas,
   constructions, equations, invariants, certificates, or counterexamples to
   proposed sublemmas. Vague progress reports receive no credit.
6. Adversarial review is continuous. Candidate proofs are tested for hidden
   hypotheses, circularity, conditional steps, unjustified limit passages, and
   equivalent restatements masquerading as progress.
7. Search is iterative: synthesize, challenge, redirect, and run another round
   instead of stopping after the first family fails.

## Stage5-compatible core prompt

The following is the extracted core used by the Stage5 conjecture Blueprint.
It is written for one long-lived `/goal` worker and therefore contains no
hidden child-agent concurrency:

> Work on exactly the claim bound by the immutable claim card. Maintain a
> diverse portfolio of substantially different mathematical mechanisms and an
> explicit approach-family registry. Develop early routes independently before
> synthesis; do not let one elegant reduction crowd out incompatible routes.
> For every route, record concrete lemmas, constructions, equations,
> invariants, certificates, or counterexamples and name its exact remaining
> gap. If the gap is comparable in strength to the original claim, mark the
> route blocked and reopen it only when a materially new mechanism appears.
> Repeatedly synthesize, challenge, redirect, and start fresh rounds. Audit
> every resolution candidate for circularity, hidden hypotheses, conditional
> steps, equivalent reformulations, and unsupported “routine” claims. A proof
> or refutation counts only when it resolves the exact `Claim` or exact
> `Not Claim`, survives adversarial review, and closes the required human and
> Lean roots. Finite checks, special cases, reductions, failed searches, and
> polished summaries remain partial evidence and must be checkpointed
> truthfully rather than presented as completion.

## Adaptation to the project execution boundary

| Upstream technique | Stage5 realization |
|---|---|
| Multiple independent agents | Independent approach families developed serially inside the same authenticated long-lived `/goal` |
| Agent-family registry | `frontier.json` plus `research/attempt-001.json`, grouped by mathematical mechanism |
| Root-agent synthesis and redirection | Same worker records synthesis, route allocation, blocking and reopening decisions in `process-audit.md` |
| Adversarial agents | Explicit self-adversarial audit in `resolution-candidate-review.json`, followed by independent canonical-Master validation |
| Concrete agent returns | Typed nodes in `resolution-proof-units.json` and exact Lean obligations |
| Full-proof-only return | Exact `Claim` or `Not Claim` release conjunction; otherwise a typed unfinished checkpoint |

The project-wide prohibition on collaboration tools, subagents, child threads,
cross-task-root access, and unaccounted requests remains unchanged. The method
is imported; the upstream concurrency topology is not.
