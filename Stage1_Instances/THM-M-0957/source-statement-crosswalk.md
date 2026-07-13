# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6987-6992` supplies exactly the title `Behrend construction`,
Felix Behrend, 1946, the gloss `large sets without three-term arithmetic progressions`, importance
"high," and status `verified` (English here translates the Chinese fields). All six uncited lines
originate at commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:26092-26117` repeats the gloss while leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest preserves `verified` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Inspected primary-source lead

The NLM/PMC record and scanned pages identify F. A. Behrend, "On Sets of Integers Which Contain No
Three Terms in Arithmetical Progression," *Proceedings of the National Academy of Sciences* 32(12)
(1946), 331-332, DOI `10.1073/pnas.32.12.331`, PMCID `PMC1078964`. Temporary observations on
2026-07-13 had page-image SHA-256 values
`fe479d874018a6b91949fd0e12e78fcca52a96f3b416f3d870129d8bb4eed62c` (page 331) and
`a39daa5b9856579752f1b56fa3df7982f29fa793d8c55759bfd3ec449afc485f` (page 332). The remote
images were inspected but not added to the repository.

Page 331 defines `S` as a set of nonnegative integers at most `N` with no three distinct terms in
arithmetic progression, equivalently no distinct `A, A', A''` satisfying `A + A' = 2 A''`. It
defines `v(N)` as the maximum size of such a set. Pages 331-332 construct a progression-free digit
sphere and conclude that, for every `epsilon > 0` and sufficiently large `N`,

`v(N) > N^(1 - (2 * sqrt (2 * log 2) + epsilon) / sqrt (log N))`.

This is not yet `H0`. The scan is a mutable remote observation rather than an admitted immutable
source packet; the transcription and notation-to-modern-definition mapping lack an independent
reviewer; and corrections, errata, and the historical-versus-modern bound boundary have not been
audited. It does support `H1` rather than an unlocated-source classification.

## Clause crosswalk

| Source component | Repository component | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| nonnegative integers `<= N` | sets without 3-term arithmetic progressions | `Finset Nat` contained in `Finset.range (N + 1)` | inclusive endpoint must be transported |
| three distinct `A, A', A''`; `A + A' != 2 A''` | "without three-term arithmetic progressions" | `ThreeAPFree (s : Set Nat)` and `threeAPFree_iff_eq_right` | likely compatible over `Nat`; exact distinctness/orientation transport still unchecked |
| `v(N)`, maximum cardinality | "large sets" | `rothNumberNat (N + 1)` for the inclusive source interval | source/mathlib indexing transport open |
| every `epsilon > 0`, sufficiently large `N` | quantitative Behrend lower bound | an eventual real-power inequality | exact binder order, threshold, casts, logarithm, square root, and strictness not frozen |
| sphere/digit construction | Behrend construction | `Behrend.sphere`, `Behrend.map`, `Behrend.threeAPFree_image_sphere` | proof architecture lead only |
| `verified` | untrusted inventory label | no Lean declaration or receipt | no H/M/R credit |

## Pinned Lean candidate

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains
`Mathlib.Combinatorics.Additive.AP.Three.Behrend`. Its terminal theorem

`Behrend.roth_lower_bound {N : Nat} : (N : Real) * Real.exp
(-4 * Real.sqrt (Real.log (N : Real))) <= (rothNumberNat N : Real)`

is an explicit modern lower bound for every natural `N`. The same module supplies the strict
large-`N` theorem `Behrend.roth_lower_bound_explicit`, the digit-sphere construction, and the
3AP-free image. `Mathlib.Combinatorics.Additive.AP.Three.Defs` supplies `ThreeAPFree`,
`threeAPFree_iff_eq_right`, and `rothNumberNat_spec`.

The candidate is highly relevant but not credited as the exact root at intake. The historical
paper uses the inclusive interval through `N`, an epsilon/asymptotic exponent, and a strict
inequality; mathlib uses `range N`, an explicit constant `4`, and a non-strict all-`N` inequality.
The statement phase must select one exact source-faithful root and check any implication or
index-shift transport. The anchor audit must then inspect immutable module/declaration provenance,
terminal proof body, exact type, axioms, transitive dependencies, placeholders, and trust closure.

## Source gate

Before leaving `H1`, accountable reviewers must preserve an approved immutable edition, verify the
displayed formula and incorporated definitions, map every binder, hypothesis, conclusion and
boundary case, audit errata and later reformulations, and independently approve the crosswalk. The
statement phase must then freeze the minimal imports, exact Lean expression and environment hashes,
checked alternate transports, and removed-hypothesis, changed-domain, binder-scope, and boundary
mutations.
