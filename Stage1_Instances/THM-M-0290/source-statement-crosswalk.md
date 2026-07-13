# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:2083-2088` supplies the title `卡尔松-亨特定理`
("Carleson-Hunt theorem"), the attribution Lennart Carleson/Richard Hunt, the year 1968, the gloss
`L^p函数的傅里叶级数几乎处处收敛` ("the Fourier series of an `L^p` function converges almost
everywhere"), importance `高` ("high"), and status `已验证` ("verified"). Git blame places all six
uncited lines in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:8008-8033` mechanically repeats the gloss while expressly leaving exact
definitions and premises, proof route, dependencies, equivalent formulations, axioms, machine
status, and artifact links open. It is not an independent mathematical source. The rev-5.6
manifest deliberately retains `verified` only as untrusted metadata and resets the target to
`L0 / rework_required`.

## Primary-source lead

The immutable external formalization bibliography at
`fpvandoorn/carleson@80e151dff5ddce2426079ec6392616496a4ec927`,
`blueprint/src/bibliography.bib:980-991` (file SHA-256
`0974024f446ede17cc12e71dd9db10008775d9bb1f7c2cf8c1cf5bf74c30b0ad`), identifies this likely
primary work:

Richard A. Hunt, "On the convergence of Fourier series," in *Orthogonal Expansions and their
Continuous Analogues* (Proceedings of the Conference, Edwardsville, Illinois, 1967), pages 235-255,
Southern Illinois University Press, Carbondale, Illinois, 1968; MR238019.

The attribution, date, and subject match the repository record. The paper text, exact theorem or
section locator, definition chain, complete assumptions, proof nodes, corrections, and errata were
not inspected in this intake. The citation is therefore a named primary-work lead with an explicit
unresolved mapping list (`H1`), not accepted `H0` evidence. Source reviewer: unassigned independent
reviewer.

Lennart Carleson's antecedent *On convergence and growth of partial sums of Fourier series*,
*Acta Mathematica* **116** (1966), pages 135-157, is recorded in the read-only `THM-M-0346`
crosswalk as the `L^2` source candidate. Its exact dependency role in Hunt's `L^p` proof has not
been source-mapped here. It is a dependent-source lead, not proof credit for this root.

## Component crosswalk

| Repository phrase | Candidate mathematical component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `L^p` function | periodic measurable function in a source-selected exponent range | `MeasureTheory.MemLp f p AddCircle.haarAddCircle` or `MeasureTheory.Lp` plus a representative | exponent range and function model absent from catalog |
| Fourier series | coefficients against integer characters of a one-dimensional periodic group | `fourierCoeff`, `fourier`, finite sums | period, sign, scalar, and normalization open |
| partial sums | conventionally the full symmetric sequence | finite integer interval such as inclusive `[-N, N]` | catalog does not state a cutoff convention |
| almost everywhere | outside a null set for the source measure | `∀ᵐ x ∂μ, ...` | measure and normalization open |
| converges | full sequence rather than a subsequence or Cesaro means | `Tendsto ... atTop ...` | sequence/filter and target topology open |
| target value | the original function at almost every point | `nhds (f x)` plus representative transport | representative semantics open |
| Carleson/Hunt, 1968 | historical theorem family and source identity | no Lean proof credit | candidate paper identified, exact passage uninspected |

The source record does not state `1 < p`, a finite upper endpoint, an infinity endpoint, circle or
interval domain, period, scalar field, Haar/Lebesgue normalization, symmetric cutoffs, function
versus equivalence class, or representative semantics. None of these is silently inferred as the
canonical source claim.

## Formal discovery boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` provides
`Mathlib.Analysis.Fourier.AddCircle`, including normalized `AddCircle.haarAddCircle`, `fourier`,
`fourierCoeff`, `fourierLp`, and `hasSum_fourier_series_L2`. The last declaration proves summation in
the `L^2` space, not pointwise or almost-everywhere convergence. A bounded name search found no
local `carleson_hunt` declaration or `partialFourierSum'` definition. This is intake discovery, not
the later exhaustive immutable anchor audit.

The read-only `THM-M-0346` audit records an external candidate at
`fpvandoorn/carleson@80e151dff5ddce2426079ec6392616496a4ec927`, module
`Carleson.Classical.CarlesonHunt`, file `Carleson/Classical/CarlesonHunt.lean:261-267`,
declaration:

```lean
theorem carleson_hunt {T : ℝ} [hT : Fact (0 < T)] {f : AddCircle T → ℂ} {p : ℝ≥0∞} (hp : 1 < p)
  (hf : MemLp f p AddCircle.haarAddCircle) :
    ∀ᵐ x, Tendsto (partialFourierSum' · f x) atTop (𝓝 (f x)) :=
  carleson_hunt' hp hf.of_haarAddCircle
```

The inspected `CarlesonHunt.lean` file has SHA-256
`d9a8d0f084dd38fe383e0cee972392bb89ad52e7ebe05a9e73fd8f2abb71bf1c`. At the same commit,
`Carleson/Classical/Basic.lean:32-33` (file SHA-256
`dcfd4cb122d04deb4e982ec509430385fbe4532fdfea4235ec52998adb4d364e`) defines
`partialFourierSum' N f` as the inclusive symmetric sum over integer frequencies from `-N` through
`N`. The project uses Lean
`v4.30.0-rc2` and mathlib
`1a4917a18b30ea1333c195e597067fe044ac9176`, is not in the existing dependency lock, and was not
fetched, built, imported, or transitively axiom-checked for this intake. It is
`external_upstream_anchor_only` discovery and receives no M0 proof credit.

Before `H0`, accountable reviewers must inspect a fixed primary-source edition, pinpoint every
incorporated definition, premise, proof boundary, transition, and conclusion, audit corrections and
errata, and independently approve the mapping. Before the statement gate, those accepted choices
must become one elaborated Lean expression with environment and expression fingerprints, checked
alternate encodings, and the required statement mutations.
