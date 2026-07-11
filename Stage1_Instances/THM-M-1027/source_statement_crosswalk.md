# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Existence of a probability law on continuous paths modeling Brownian motion | N. Wiener, "Differential-Space", *Journal of Mathematics and Physics* 2 (1923), 131-174 | existential `StatementShape` or a canonical path-space measure | Foundational primary source located by bibliographic identity; exact theorem/page/premise and errata audit are not yet accepted (`H1`) |
| Modern defining laws: zero start, independent normal increments, continuous paths | D. Revuz and M. Yor, *Continuous Martingales and Brownian Motion*, 3rd ed., Springer, 1999, Chapter I (discovery anchor) | fields of legacy `WienerProcess` | Secondary-source discovery anchor only; edition pages and exact definition/existence theorem crosswalk remain open |
| Time domain | Standard one-sided Brownian motion uses `t >= 0` | `BrownianTime := ℝ≥0` | Plausible candidate; mutation against `ℝ`, intervals, and binder scope belongs to statement phase |
| Increment law | For `s <= t`, `W_t-W_s` is centered normal with variance `t-s` | `HasLaw ... (gaussianReal 0 (incrementVariance s t hst)) P` | Legacy expression located; exact parameter convention and elaboration are unaccepted |
| Independent increments | Disjoint ordered increments are independent | `HasIndepIncrements W P` | API candidate only; its precise mathlib semantics must be inspected before equivalence is claimed |
| Continuous paths | Sample paths are continuous almost surely | `∀ᵐ ω ∂P, Continuous (fun t => W t ω)` | Matches the conservative human root in prose; measurability and representative issues remain to audit |
| Zero initial value | `W_0 = 0` almost surely | `∀ᵐ ω ∂P, W 0 ω = 0` | Candidate boundary law; everywhere-zero-at-origin encodings require a checked transport |
| Gaussian process and adaptation | Common derived/package properties | `IsGaussianProcess W P` and `Adapted (Filtration.natural ...) W` | Not automatically part of the canonical existence claim; retain as candidate consequences rather than broaden the root |

The repository catalogue provides only the Chinese gloss `布朗运动的数学构造` (mathematical
construction of Brownian motion). The intake therefore chooses the standard one-dimensional,
zero-drift, unit-variance, nonnegative-time existence theorem as the conservative target, while
leaving its exact source identity open. The statement phase may freeze this target only after a
pinpoint source audit and must record any semantic delta rather than silently changing it.

Discovery locators (not immutable evidence receipts):

- Wiener article bibliographic record: DOI `10.1002/sapm192321131`.
- Revuz-Yor: Springer, ISBN `978-3-540-64325-8`.
- Repo-local candidate: `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_218.lean`.

No `H0`, exact Lean statement, external proof integration, or theorem completion is claimed.
Required follow-up includes source-file hashes, pinpoint page/theorem mapping, assumptions and
normalization audit, errata search, independent review, exact Lean elaboration, checked transports,
and statement mutation tests.
