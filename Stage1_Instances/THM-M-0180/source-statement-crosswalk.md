# Source-statement crosswalk

## Available repository record

`Docs/researches/math_theorems.md` records the Chinese title "丘成桐-郑绍远极值原理," attributes it
to Shing-Tung Yau and Shiu-Yuen Cheng, dates it to 1975, and glosses it as "特征函数的梯度估计"
(`gradient estimate for eigenfunctions`). `Docs/Stage0_Blueprint.md` repeats that gloss but supplies
no bibliography, theorem number, page, assumptions, proof, or errata. The rev-5.6 manifest adds only
screening metadata. Consequently none of these records earns `H0` or fixes a Lean proposition.

## Primary-source discovery anchor

Shiu-Yuen Cheng and Shing-Tung Yau, "Differential equations on Riemannian manifolds and their
geometric applications," *Communications on Pure and Applied Mathematics* 28 (1975), 333-354, is a
plausible primary-source family matching the authors and year. The paper's exact theorem numbering,
pages, hypotheses, wording, and relationship to both repository phrases have not been inspected in
an immutable edition in this phase. It is therefore a discovery anchor only, not accepted source
evidence. A later source audit must also check errata and whether the intended eponym is attached by
later literature rather than by the original paper.

## Crosswalk

| Repository element | Mathematical information | Lean information needed | Intake result |
|---|---|---|---|
| Chinese title: "maximum principle" | suggests an almost-maximum sequence theorem on a complete Riemannian manifold | manifold, metric/completeness, curvature, `f`, gradient, Laplacian, limiting predicates | candidate branch only |
| gloss: "eigenfunction gradient estimate" | suggests a quantitative bound for a Laplace eigenfunction | eigen-equation, sign, domain, norm, constants, curvature/boundary data | conflicting candidate branch |
| Cheng/Yau, 1975 | identifies a plausible publication family | exact edition, theorem/page, premise transcription | discovery anchor only |
| differential geometry category | rules out unrelated finite/combinatorial extrema | Riemannian and analytic APIs | coarse disambiguation only |
| `已验证` | untrusted metadata label | source review and kernel receipts | no credit |

## Statement gate

The next phase must inspect an immutable primary source and reconcile the title and gloss without
broadening or substitution. It must record a verbatim theorem anchor and assumption-by-assumption
crosswalk before selecting a canonical Lean expression. Candidate search and machine-proof credit
belong to the later anchor-audit phase.
