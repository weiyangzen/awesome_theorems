# Source-statement crosswalk

| Claim component | Available source anchor | Formal target requirement | Intake assessment |
|---|---|---|---|
| Item identity | `Docs/researches/math_theorems.md` names `Lebesgue刺`, attributes it to Henri Lebesgue (1913), and says only `非正则边界点的例子` | Preserve the identity as Lebesgue's example, rather than a generic irregular point | Metadata discovery only; no primary citation, theorem, or page |
| Explicit spine | Not specified by the repository source | Freeze the exact ambient dimension, set formula, profile, truncation, orientation, and tip | Open; choosing a familiar exponential or logarithmic cusp now would broaden or substitute the target |
| Boundary regularity | Catalogue phrase means “example of a non-regular boundary point” | Define regularity for the classical Laplace Dirichlet problem and prove the selected tip fails it | Semantic correspondence only; data and solution conventions are unresolved |
| Expected proof bridge | The surrounding catalogue entries are Perron's method, Wiener criterion, and regular boundary points | Apply an exact capacity/barrier criterion to the sourced spine | Discovery clue only; no bridge is credited |
| Lean representation | No Lean module or declaration is cited | Select exact Euclidean-domain, harmonic/Perron, capacity, and regularity APIs after source freeze | No candidate receives machine credit |

The catalogue's `已验证` label is explicitly untrusted under rev-5.6. It supplies neither a human
proof citation nor kernel evidence. Searches of the repository found no more detailed statement for
this ID. In particular, several inequivalent thin-cusp constructions circulate under related names;
their dimensions and thickness conditions affect whether the tip is regular. The statement phase is
therefore blocked until a primary or authoritative scholarly source fixes the construction.

## Required source audit

1. Locate the cited 1913 work or a scholarly edition that explicitly attributes and states the
   example; record edition, page, original terminology, and a content hash.
2. Cross-check a modern potential-theory source for the exact definition of boundary regularity,
   the spine formula, dimension, and Wiener/capacity calculation.
3. Check corrections, translation differences, and whether “spine” denotes the removed thin set or
   the resulting domain.
4. Obtain independent review of the premise-to-claim mapping before assigning `H0` or elaborating a
   canonical Lean expression.

Current classification is `H4`: the catalogue-level claim is intelligible, but the exact claim is
not source-frozen. This is a deliberate fail-closed boundary, not evidence that the classical result
is doubtful.

