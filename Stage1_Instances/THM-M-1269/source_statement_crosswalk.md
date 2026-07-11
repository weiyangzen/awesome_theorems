# Source-statement crosswalk

| Claim component | Repository source anchor | Mathematical basis | Lean candidate | Intake assessment |
|---|---|---|---|---|
| Variational approximation | `Docs/Stage0_Blueprint.md`, `THM-M-1269`: `变分问题的逼近` | Standard defining property of a finite infimum | `sInf (Set.range F)` plus `Tendsto` | The repository wording is too broad to count as an exact source statement |
| Nonempty admissible class | Implicit in the phrase "variational problem" | Needed to choose approximate minimizers | `[Nonempty X]` or an explicit witness | Frozen as an explicit hypothesis; encoding remains provisional |
| Finite lower endpoint | Not stated in Stage0 | Real-valued convergence to an infimum requires the range to be bounded below | `BddBelow (Set.range F)` | Added as a necessary scope condition, not silently attributed to Stage0 |
| Minimizing sequence | Stage0 title `极小化序列` | `F (u n)` converges to `inf F`; no convergence of `u n` is asserted | `Tendsto (fun n => F (u n)) atTop (nhds (sInf ...))` | Canonical intake interpretation pending statement acceptance |
| Minimizer existence | Not claimed | Requires additional compactness/lower-semicontinuity machinery | deliberately absent | Explicitly out of scope |

No primary mathematical source is named by the repository entry. Accordingly,
this intake makes no invented author, edition, theorem number, or page claim.
The statement is the elementary infimum-approximation lemma commonly used to
start the direct method, rather than the substantially stronger direct-method
existence theorem. A later source audit must identify and pin a primary or
authoritative textbook statement, map every premise, and check errata before
the human-source status can advance.

The statement phase must also inspect the actual mathlib APIs, elaborate the
ordered binders and universes, serialize the normalized target, test the empty
and unbounded variants, and check any subtype or extended-real transport. No
external theorem, historical `已验证` label, or candidate API receives proof
credit here.
