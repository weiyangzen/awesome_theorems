# Source-statement crosswalk

| Claim component | Repository source anchor | Frozen interpretation | Intake assessment |
|---|---|---|---|
| Theorem identity | `Docs/researches/math_theorems.md`, entry `霍奇分解定理` | Hodge decomposition theorem | discovery metadata only |
| Subject | source text: `微分形式的Hodge分解` | decomposition of smooth differential forms | supports the analytic form-level interpretation, but supplies no hypotheses |
| Historical attribution | `Docs/Stage0_Blueprint.md`, `THM-M-0545`: William Hodge, 1941 | classical Hodge theory | unpinned secondary metadata; no H credit |
| Manifold assumptions | absent from the source record | compact, oriented, Riemannian, boundaryless | necessary scope choice; primary-source verification remains open |
| Exact conclusion | absent from the source record | unique orthogonal harmonic/exact/coexact decomposition | canonicalized at intake, not yet source-verified or Lean-elaborated |
| Cohomology consequence | not stated | unique harmonic representative for each de Rham class | corollary boundary only; cannot substitute for the full root |

No primary mathematical source with an immutable edition, theorem/page, complete assumptions, and
errata record is present in the repository. The source label `已验证` is therefore untrusted
metadata, not evidence. The anchor-audit phase must locate and pin a primary source, map every
hypothesis and conclusion component, review errata, and obtain independent review before `H0` is
possible.

The similarly named `THM-M-0113` chooses the compact-Kahler cohomological bidegree decomposition.
That is not substituted here: this target follows its own source wording about differential forms
and freezes the Riemannian harmonic/exact/coexact theorem. Algebraic `KaehlerDifferential` APIs and
the Hodge conjecture are also explicitly outside scope.

