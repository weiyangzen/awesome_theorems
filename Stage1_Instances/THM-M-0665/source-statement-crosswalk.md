# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` attributes the result to Jonathan Pila and Alex Wilkie, dates it
to 2006, and says only "rational points in o-minimal structures". Stage0 repeats the theorem name,
and the rev-5.6 manifest preserves `已验证` as explicitly untrusted metadata. These records do not
specify a theorem number, height convention, algebraic part, quantifier dependencies, or proof.

## Candidate primary source

Jonathan Pila and Alex J. Wilkie, "The rational points of a definable set," *Duke Mathematical
Journal* **133** (2006), no. 3, 591-616, DOI `10.1215/S0012-7094-06-13336-7`, is the primary work
associated with the named theorem. The repo-local dossier for the separate target `THM-M-0441`
identifies Theorem 1.8 (first version), Definition 1.3 (affine height), and Definition 1.5
(algebraic part), and records a inspected-copy SHA-256. That record is a useful locator only: this
intake has not independently inspected or accepted its copy, errata search, or crosswalk.

The statement phase freezes Theorem 1.8 (first version), Definition 1.3, and Definition 1.5, using
the independently elaborated `Statement.lean`. The inspected-copy record in `THM-M-0441`
corroborates the pinpoint but transfers no H-state or proof credit. Before `H0`, a source reviewer
must independently acquire an immutable copy, record its hash and exact pages,
inspect the named theorem and definitions, check published corrections, map the proof nodes and
assumptions, and approve the crosswalk independently.

## Crosswalk

| Repository/source phrase | Provisional mathematical meaning | Required Lean component | Intake status |
|---|---|---|---|
| o-minimal structure | an o-minimal expansion of the ordered real field | `IsOMinimalExpansion L` | frozen and elaborated |
| definable set `X` | a parameter-definable subset of real affine `n`-space | `(Set.univ : Set Real).Definable L X` | frozen and elaborated |
| rational points | `q in Q^n` embedded coordinatewise in `R^n` | `RationalPoint n` and `rationalPointToReal` | frozen and elaborated |
| height at most `T` | coordinate maximum of the source affine rational height | `rationalHeight`, `pointHeight`, and a nonstrict bound | frozen and elaborated |
| algebraic part `X_alg` | union of connected positive-dimensional semialgebraic subsets of `X` | `algebraicPart X`, using nontriviality for positive dimension | frozen and elaborated |
| subpolynomial bound | for every `epsilon > 0`, some `c > 0` bounds all `T >= 1` by `c*T^epsilon` | explicit finiteness, `Set.ncard`, real coercion and `Real.rpow` notation | frozen and elaborated |

## Lean discovery boundary

At the pinned mathlib revision, `Mathlib.ModelTheory.Definability` exposes parameter-definability,
`Mathlib.Data.Set.Card` exposes `Set.Finite` and `Set.ncard`, and
`Mathlib.Analysis.SpecialFunctions.Pow.Real` exposes real powers. `IntakeProbe.lean` checks these
ingredient names and types with the pinned Lean executable.

The exact statement is credited only to this target's checked `Statement.lean`; no proof is
credited. The legacy `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_087.lean`
belongs to `THM-M-0441` and explicitly uses uninstantiated boundary data for missing concepts. It
cannot be imported as either the exact statement or a proof of this target. A later anchor audit
must independently inventory pinned mathlib and external Lean 4 candidates at immutable revisions.
