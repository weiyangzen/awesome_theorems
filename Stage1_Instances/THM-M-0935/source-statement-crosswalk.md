# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6833-6838` supplies exactly the title
`Dias da Silva-Hamidoune定理`, attribution `Dias da Silva/Hamidoune`, year 1994, gloss
`Erdős-Heilbronn猜想的证明`, importance "high," and status `已验证`. Git history attributes all
six uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no
formula, definitions, binders, hypotheses, theorem/page locator, source edition, correction history,
proof boundary, reviewer, or formal artifact.

`Docs/Stage0_Blueprint.md:25498-25523` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, alternate statements, axiom policy, machine status, and
artifact links open. The rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and
resets the target to `L0 / rework_required`.

## Primary bibliographic lead

Crossref authenticates J. A. Dias da Silva and Y. O. Hamidoune, "Cyclic Spaces for Grassmann
Derivatives and Additive Theory," *Bulletin of the London Mathematical Society* 26(2), March 1994,
pages 140-146, DOI `10.1112/blms/26.2.140`. The DOI/publisher path was access-blocked during this
intake. Therefore no exact internal theorem number or page, definition context, proof text,
correction/errata state, or source-to-node map was inspected or admitted. The paper is a primary
bibliographic lead, not an accepted `E4`/`H0` packet.

The zbMATH Open record `Zbl 0819.11007` (`id 695039`) contains a summary saying that, for finite
`A` in `Z_p`, the paper proves that sums of all `m`-subsets have cardinality at least
`min(p, m(|A|-m)+1)` and thereby answers the two-subset conjecture. It also summarizes the more
general Grassmann-space result. This source-close metadata strongly identifies the general family,
but the displayed summary omits the admissible range for `m` and does not expose an internal
theorem/page locator, incorporated definitions, proof text, or errata. It is therefore discovery
evidence, not a substitute for primary-text admission.

## Inspected scholarly statement leads

Two accessible sources state the general theorem and cite the 1994 paper:

- Eric Balandraud, "Addition theorems in Fp via the polynomial method," arXiv:1702.06419v1,
  Definition 1 and Theorem 2, printed page 2. For `A` in `F_p` and natural
  `h in [0, |A|]`, it defines `h^A` as sums of `h` pairwise distinct elements and states
  `|h^A| >= min(p, h(|A| - h) + 1)`. The inspected 13-page PDF has SHA-256
  `479d268d10d987942924681dcbc14bfa2eb1e47e415357de91af5d29ad8c78bf`.
- Laszlo M. Feher and Janos Nagy, "Additive combinatorics using equivariant cohomology,"
  arXiv:1610.02539v4, introduction and Theorem 3.1, printed pages 2 and 6. For `|A| = n` and
  `1 <= k <= n`, it states `|k^A| >= min((n-k)k+1, p)`. The inspected 26-page PDF has SHA-256
  `2d2d3b703428a28cc94191f065c4df6ff820ba7ac3d9194c2708ae07138aef59`.

A third inspected source, Jayasuriya-Reich-Wheeler, arXiv:1210.6509v2, Theorem 2.2 and Remark 2.3,
uses "Dias da Silva-Hamidoune theorem" for the `A = B` Erdos-Heilbronn case
`|A dot+ A| >= min(p, 2|A|-3)`. It also distinguishes the later unequal-two-set extension. Its
17-page PDF has SHA-256
`fb3e54b877a46c4bd3677f50061d2cb39de1a88aec48a7c6e4a019918135b26c`.

These are secondary or later proof sources (`E5` discovery evidence here), not substitutes for the
uninspected primary article. Together they establish the scope fork and prevent intake from
silently selecting the convenient `h = 2` statement or silently broadening the catalog gloss to all
`h`.

## Clause crosswalk

| Catalog/source component | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| Dias da Silva-Hamidoune theorem | general fixed-cardinality restricted subset-sum bound in later sources | image of `A.powersetCard h` under `Finset.sum` in `ZMod p` | strong family lead; exact primary locator and target ownership open |
| Erdos-Heilbronn proof | `h = 2` unequal-pair self-sumset lower bound | two-element subsets or `A.offDiag.image (fun ab => ab.1 + ab.2)` | specialization lead only; checked transport and neighbor ownership open |
| pairwise distinct | no element may occur twice among the `h` summands | fixed-cardinality finsets, or tuples plus `Pairwise` | representation and quotient/permutation transport open |
| prime modulus | additive group/field of `p` elements | `p : Nat`, `hp : p.Prime`, `ZMod p` | likely domain; exact primary notation and field/group transport open |
| lower bound | `min(p, h(|A|-h)+1)` | natural cardinal inequality with explicit `h <= A.card` | exact binder order, endpoint, casts, and subtraction semantics open |
| 1994 proof | exterior-algebra / Grassmann-derivative source proof | future source nodes and formal proof obligations | primary proof and dependency tree uninspected |
| `已验证` | untrusted catalog metadata | no declaration or proof body | no H, M, or R credit |

## Formal discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, bounded repository and
mathlib text searches found no Dias da Silva-Hamidoune, Erdos-Heilbronn, or exact restricted
fixed-cardinality sumset declaration. `IntakeProbe.lean` authenticates adjacent APIs:

- `Finset.powersetCard`, `Finset.mem_powersetCard`, and `Finset.card_powersetCard` for choosing
  distinct `h`-element subsets;
- `Finset.sum` and `Finset.image` for a prospective restricted-sumset definition;
- `Finset.subsetSum`, which is deliberately broader because it uses all subset sizes; and
- `ZMod.cauchy_davenport`, an ordinary two-set sumset theorem without the distinctness constraint.

The probe does not define the target, elaborate a canonical expression, or inspect any proof body.
The bounded search is not the later precommitted exhaustive anchor audit. The truthful provisional
machine state is `M4`, not `M3` or any `M0` class.

## Missing source-to-statement obligations

Before a canonical statement can be frozen, downstream work must:

1. lawfully preserve and inspect an immutable primary edition and pinpoint the exact theorem,
   definitions, inherited assumptions, proof boundary, and corrections or errata;
2. obtain independent review of the transcription and catalog mapping;
3. decide general `h`-fold ownership versus the `h = 2` conjecture specialization and reconcile
   `THM-M-0934` without sharing proof credit;
4. settle `h = 0` versus `h >= 1`, nonempty-set requirements, `F_p` versus `ZMod p`, and all cases
   listed in the scope map;
5. choose a restricted-sumset encoding and prove every claimed tuple/subset, order, and domain
   transport in the required direction; and
6. elaborate the exact Lean target with minimal pinned imports, serialized expression and
   environment fingerprints, and the required removed-hypothesis, changed-domain, binder-scope,
   and boundary mutations.

Until those obligations close, the source crosswalk is intentionally incomplete and all downstream
tasks remain open.
