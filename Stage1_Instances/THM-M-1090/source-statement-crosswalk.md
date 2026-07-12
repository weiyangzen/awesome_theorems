# Source-statement crosswalk

## Available source record

The repository's immediate source is `Docs/researches/math_theorems.md`, whose complete mathematical
content for this target is the title "Markov process", attribution to Andrey Markov, year 1906,
and gloss "Markov property". `Docs/Stage0_Blueprint.md` reproduces that metadata and adds no formula,
hypotheses, bibliographic work, theorem number, page, or proof. The label `已验证` is expressly
untrusted under rev-5.6.

## Crosswalk

| Source component | Conventional mathematical reading | Lean target component needed | Intake assessment |
|---|---|---|---|
| `Markov process` | A stochastic process satisfying a memoryless conditional-law property | process, probability measure, filtration, state measurable space | topic identified; all concrete objects open |
| `Markov property` | Given the past at deterministic time `s`, the future depends on it only through `X_s` | conditional expectation/distribution or conditional-independence proposition | family identified; exact formula and null-set semantics open |
| Andrey Markov, 1906 | Historical origin in dependent-trial/chain work | immutable primary edition and definition/theorem crosswalk | attribution not independently audited here |
| `verified` | repository status label | exact declaration, proof-body provenance, and kernel receipt | no credit; no exact declaration located |

## Neighboring claims that are not the root

| Neighbor | Relationship | Boundary |
|---|---|---|
| Markov kernel | A transition object whose values are probability measures | `ProbabilityTheory.IsMarkovKernel` does not assert a process has the Markov property |
| Chapman-Kolmogorov equation | Composition consistency of transition kernels | separately owned by `THM-M-1091`; neither direction is automatic without a process/kernel model |
| Strong Markov property | Markov identity at stopping times | stronger than deterministic-time Markov in general formulations |
| SDE solution is Markov | A theorem deriving the property from SDE well-posedness | separately owned by `THM-M-1039` |
| Martingale-problem characterization | Derives/characterizes Markov families via a well-posed martingale problem | separately owned by `THM-M-1048` |

## Source gate

No `H0` or exact-statement claim is made. Before statement acceptance, an independent reviewer must
provide an immutable authoritative source, exact theorem/page and definitions, premise-by-premise
mapping, errata search, and a decision about ordinary versus strong and homogeneous versus
inhomogeneous Markov behavior. If the source record was intended only as a definition, it must be
reclassified or paired with a genuine theorem rather than converted into a tautological Lean
wrapper.
