# Source-statement crosswalk

## Repository source record

The only located theorem-specific source is `Docs/researches/math_theorems.md`, record
**Hopf引理**: proposer Eberhard Hopf; date 1952; statement “边界上的导数符号” (“the sign of the
derivative at the boundary”); formalization status “已验证” (“verified”). The status is manifest
metadata marked untrusted, not an evidence receipt.

| Source phrase or context | Provisional mathematical reading | Missing information that blocks an exact statement |
|---|---|---|
| `Hopf引理` | Hopf boundary point lemma in elliptic PDE | This name also occurs in other areas; no bibliographic locator is supplied |
| PDE / differential-equations category | A second-order elliptic maximum-principle result | Operator, ellipticity, coefficient, and zeroth-order assumptions are absent |
| Neighboring Laplace, mean-value, and maximum-principle records | Harmonic/Laplacian special case is the least speculative local context | Adjacency is not a primary source and cannot freeze scope |
| `边界上的导数符号` | A normal directional derivative has a strict sign at a boundary extremum | Boundary point, inward/outward convention, maximum/minimum convention, derivative notion, and strictness are absent |
| Eberhard Hopf, 1952 | Intended genealogy may be Hopf's elliptic boundary point result | Title, edition, theorem/page, assumptions, stable identifier, and errata are absent |
| `已验证` | Historical catalog label only | No formal project, revision, module, declaration, build, or kernel receipt is identified |

## Candidate formulations kept distinct

1. Harmonic maximum form: a nonconstant harmonic function attaining a strict boundary maximum at a
   point satisfying an interior sphere condition has a strict normal-derivative sign.
2. Harmonic minimum form: the sign-reversed consequence obtained by applying the maximum form to
   `-u`, once the hypotheses and normal convention are fixed.
3. General elliptic form: replace harmonicity by an inequality for a uniformly elliptic operator
   with coefficient and sign hypotheses. This is a generalization, not an acceptable substitute for
   an unspecified root.
4. Weak boundary form: state a strict one-sided liminf quotient rather than assuming a classical
   boundary derivative. This changes both hypotheses and conclusion and needs its own checked map.

None is accepted as the exact root in this intake. No Lean theorem candidate is credited, because
anchor discovery belongs to the later audit node and inspecting closure before the statement is
frozen would violate the rev-5.6 ordering.

## Required source resolution

The statement phase needs an accepted primary edition or archival scan with theorem/section/page,
exact operator and domain hypotheses, boundary geometry, solution regularity, extremum and normal
conventions, conclusion form, correction/errata search, and a premise-by-premise mapping. It must
record whether the 1952 attribution is correct. Until then the human state remains `H4`, the formal
state remains `M4`, and the exact-statement gate is open.
