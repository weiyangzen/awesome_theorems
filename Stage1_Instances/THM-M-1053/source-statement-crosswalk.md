# Source-statement crosswalk

## Primary source anchor

George D. Birkhoff, "Proof of the Ergodic Theorem," *Proceedings of the National Academy of
Sciences of the United States of America* 17 (1931), 656-660, is the identified historical primary
source. Its scanned statement, notation, hypotheses, and any corrections have not yet received the
independent line-by-line review required for `H0`. A modern measure-theoretic reference must also be
selected to control the translation from Birkhoff's original formulation to current probability
space, integrability, and conditional-expectation language.

This bibliographic identification is discovery evidence only. It does not establish that the
canonical claim above is an exact transcription of the 1931 theorem.

## Crosswalk

| Repository/source phrase | Intended component | Required Lean component | Intake status |
|---|---|---|---|
| "ergodic theorem" | Birkhoff pointwise theorem | a.e. convergence of Cesaro iterates | included; encoding open |
| "time average" | averages of `f (T^k x)` | finite sums, iteration, normalization | included; zero case open |
| "space average" | `integral f dmu` | Bochner/Lebesgue integral | ergodic specialization only |
| measure-preserving dynamics | `T` preserves `mu` | measurable map and `MeasurePreserving`-like API | included; API open |
| ergodicity | invariant measurable sets are trivial | pinned ergodic predicate | required for constant limit |
| integrable observable | `f` lies in `L1(mu)` | `Integrable f mu` or exact equivalent | included; codomain open |

## Fidelity boundary

The terse repository statement omits all domains and hypotheses. The intake therefore freezes the
standard theorem family but does not invent a canonical Lean proposition. Before statement credit,
review must verify the original theorem location and conventions, select a modern exact theorem
anchor, distinguish the general invariant-limit conclusion from its ergodic corollary, and map every
hypothesis and conclusion to Lean. Mathlib and external Lean candidates remain wholly unaudited.
