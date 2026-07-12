# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` records `Carleson测度定理`, Lennart Carleson, 1962, and the gloss
`Carleson测度的特征` ("characterization of Carleson measures"). Stage0 repeats those fields. The
rev-5.6 manifest retains `已验证` only as `source_status_untrusted`. None supplies a definition,
theorem number, hypotheses, conclusion, paper title, edition, page, proof, errata, or formal artifact.

## Source work still required

The statement/source phase must locate the intended 1962 primary publication or another explicitly
accepted authoritative edition, record its bibliographic identity and pinpoint theorem/page,
transcribe the exact domain and normalization, map every assumption and conclusion, check errata,
and obtain independent review. The intake does not invent a citation from the year and attribution.
Consequently the root is only `H1`, not `H0`.

## Crosswalk

| Repository phrase | Possible mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "measure" | positive measure on disk/half-plane | measurable space and `Measure` | pinned API probed; carrier open |
| "Carleson" | uniform tent/box mass bound | sets of test regions, boundary size, quantified constant | absent |
| "characterization" | Hardy embedding equivalence | analytic/Hardy function space, integral norm, `iff` | candidate only |
| "characterization" | kernel or Poisson test equivalence | kernels/integrals and uniform bound | candidate only |
| "1962" / Carleson | bibliographic locator | immutable source revision and pinpoint | insufficient |
| `已验证` | untrusted inventory label | no proposition and no proof credit | rejected as evidence |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, a bounded name search
found no declaration named for Carleson measures. `IntakeProbe.lean` checks only generic measure and
integration ingredients under the pinned toolchain. This neither establishes that the required
Hardy-space infrastructure exists nor performs the later immutable anchor audit.
