# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6103-6108` supplies exactly the title `Karger算法`, attribution to
David Karger, year 1993, gloss `全局最小割的随机算法` ("a randomized algorithm for global minimum
cut"), importance "high," and status `已验证`. Git history attributes all six uncited lines to
commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, graph
definition, contraction semantics, theorem locator, probability or complexity conclusion,
hypotheses, proof boundary, correction history, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:22685-22710` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

## Inspected primary-source lead

David R. Karger, *Global Min-cuts in RNC, and Other Ramifications of a Simple Min-Cut Algorithm*,
Proceedings of the Fourth Annual ACM-SIAM Symposium on Discrete Algorithms (SODA 1993), pages
21-30, was inspected from the author's hosted PDF at
`https://people.csail.mit.edu/karger/Papers/mincut.pdf` on 2026-07-13. The DBLP record
`https://dblp.org/rec/conf/soda/Karger93` confirms the author, title, venue, year, pages, and ACM
locator `http://dl.acm.org/citation.cfm?id=313559.313605`. The observed PDF has SHA-256
`f090415d0aeeeaa7c907f76bb78fc2ce9293fd45c6bbca19276a5a5eb0c354cd`; its manuscript header is
dated 1992-10-30.

Section 1 assumes connected graphs and defines global minimum cut as a bipartition into two
nonempty vertex sets minimizing crossing edge count, or crossing weight in a weighted graph.
Section 2 starts with a multigraph `G(V,E)`, retains parallel edges under contraction, removes
self-loops, chooses a current edge uniformly at random, contracts its endpoints, and stops when two
supervertices remain.

Theorem 2.1, beginning on PDF page 2 and continuing on PDF page 3, states that a particular minimum
cut is produced with probability `Omega(n^-2)`. Its proof supplies the sharper bound

```text
product over r = n,...,3 of (1 - 2/r) = 1 / binom(n, 2).
```

The proof fixes a minimum cut of size `c`, observes that avoiding its edges preserves the cut and a
minimum cut of at least `c`, derives at least `r*c/2` current edges when `r` vertices remain, and
bounds the conditional chance of selecting a fixed-cut edge by `2/r`. It notes tightness on an
`n`-cycle. Corollary 2.1 then states that `O(n^2 log n)` independent contractions find a minimum
cut, indeed every minimum cut, with high probability.

This is a direct and strong source-family match, but the catalog does not cite the paper or select
Theorem 2.1 over amplification, weighted, implementation, runtime, or RNC claims. The asymptotic
theorem wording and explicit proof bound must be reconciled, incorporated definitions and every
premise must be mapped, official corrections or errata must be audited, and an independent source
reviewer must approve the target. The paper is therefore an inspected source lead, not `H0`, and
intake does not silently promote one candidate proposition to the canonical root.

## Component crosswalk

| Catalog/source component | Primary-source component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| "global minimum cut" | nontrivial vertex bipartition minimizing crossing multiplicity or weight | cut predicate, crossing edge set/multiset, minimum value | exact cut equality and weighted scope open |
| "randomized algorithm" | repeatedly choose a current edge uniformly and contract its endpoints | finite-state transition using `PMF`, quotient/partition state | transition and termination are not in pinned graph API |
| multigraph | parallel edges retained; self-loops removed after contraction | `Graph alpha beta` with explicit edge identities | suitable substrate probed; finiteness and contraction layer absent |
| fixed-cut success | Theorem 2.1 returns a particular minimum cut with `Omega(n^-2)` probability | event probability lower bound | asymptotic versus explicit `1 / binom(n,2)` target open |
| amplification | Corollary 2.1 uses independent repetitions and "high probability" | product PMF and explicit failure parameter | trial count and quantification open |
| weighted result | edge weights represented or sampled by multiplicity/proportional weight | weighted graph or multigraph transport | distinct later implementation claim; not selected |
| `已验证` | uncited inventory label | accepted H/M receipts would be required | no source or proof credit |

## Pinned Lean boundary

`IntakeProbe.lean` checks the pinned `Graph`, incidence, adjacency, loop, and banana-graph APIs plus
uniform finite and multiset probability mass functions. These APIs can express parts of a future
model but do not define cuts, contraction, a contraction trajectory, or Karger's algorithm. A
bounded case-insensitive search of repo-local Lean and pinned mathlib found no Karger, minimum-cut,
or graph-contraction declaration. These are scoped intake observations, not the later immutable
external anchor audit and not a proof of global absence.

## Source gate

Before ordinary statement execution, accountable reviewers must select one exact proposition from
the inspected source family, preserve an immutable lawful edition, map every incorporated
definition, binder, assumption, conclusion, probability convention, algorithm step, proof boundary,
and boundary case, reconcile asymptotic and explicit bounds, audit corrections, and independently
approve fidelity to `THM-M-0831`. Only then may the statement phase freeze minimal imports, an
elaborated expression and environment fingerprint, checked alternate encodings, and the required
removed-hypothesis, changed-domain, binder-scope, and boundary-case mutations.
