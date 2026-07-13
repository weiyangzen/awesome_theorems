# THM-M-0243 source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1752-1757` names the Bohr-Mollerup theorem, attributes it to
Harald Bohr and Johannes Mollerup, gives the year 1922, and says only "characterization of the
Gamma function." The record entered at repository source commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md:6734-6759` repeats that
phrase while explicitly leaving precise definitions, premises, equivalent formulations, axioms,
and machine artifacts to be supplied. The manifest's `已验证` field is untrusted under rev-5.6.

The catalog therefore identifies a named theorem family but not an exact proposition. In
particular, it omits the function domain and codomain, positivity, log-convexity, normalization,
recurrence, equality domain, and whether "characterization" denotes a uniqueness implication or a
two-sided/unique-existence package.

## Human-source leads

NIST Digital Library of Mathematical Functions, section 5.5(iv), "Bohr-Mollerup Theorem," states
the familiar modern implication: if a positive function on `(0, infinity)` satisfies
`f(x + 1) = x f(x)`, `f(1) = 1`, and convexity of `ln f(x)`, then `f(x) = Gamma(x)`. The page cites
G. E. Andrews, R. Askey, and R. Roy, *Special Functions*, Cambridge University Press (1999),
pages 34-36. This reference confirms the conventional family and supplies a modern component map.
It is secondary and was observed live, so it is not immutable primary proof evidence and does not
support `H0`.

The repository attribution and date suggest the original Bohr-Mollerup publication/book tradition,
but intake did not obtain and admit an immutable primary edition. Exact title, edition, page,
statement, definition chain, proof boundary, corrections or errata, and historical spelling are
therefore unresolved rather than invented. Before `H0`, a qualified independent source reviewer
must approve those locators and every assumption/conclusion mapping.

## Pinned Lean candidate

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` contains module
`Mathlib.Analysis.SpecialFunctions.Gamma.BohrMollerup`. Its documentation explicitly describes the
Bohr-Mollerup theorem. The exact candidate declaration is:

```lean
Real.eq_Gamma_of_log_convex
  {f : Real -> Real}
  (hf_conv : ConvexOn Real (Set.Ioi 0) (Real.log . f))
  (hf_feq : forall {y : Real}, 0 < y -> f (y + 1) = y * f y)
  (hf_pos : forall {y : Real}, 0 < y -> 0 < f y)
  (hf_one : f 1 = 1) :
  Set.EqOn f Real.Gamma (Set.Ioi (0 : Real))
```

The displayed text is a human-readable transcription of the checked type, not a newly declared
canonical target. The library represents `f` as total but observes it only on positive reals. It
states the uniqueness implication; Gamma's existence-side properties are separate declarations.

## Component crosswalk

| Catalog/reference component | Mathematical meaning to freeze | Pinned Lean component | Intake status |
|---|---|---|---|
| "Gamma function" | real Gamma on positive inputs | `Real.Gamma`; conclusion of `Real.eq_Gamma_of_log_convex` | exact-topic candidate located; root identity open |
| positive function | `f(x) > 0` for every positive `x` | `hf_pos : 0 < y -> 0 < f y` | explicit candidate premise; source mapping open |
| positive real domain | all material predicates and equality restricted to `x > 0` | `Set.Ioi 0`, `Set.EqOn` | candidate convention recorded; intrinsic-subtype transport open |
| log-convexity | convexity of `x |-> log(f x)` on positive reals | `ConvexOn Real (Set.Ioi 0) (Real.log . f)` | candidate encoding located; alternate-form transports open |
| functional equation | `f(x+1) = x f(x)` for positive `x` | `hf_feq` | quantifier and domain explicit in candidate |
| normalization | `f(1)=1` | `hf_one` | explicit candidate premise |
| characterization | any such `f` agrees with Gamma on positive reals | candidate conclusion | uniqueness implication located; full root shape open |
| Gamma satisfies conditions | existence side of a two-sided characterization | `Real.convexOn_log_Gamma`, `Real.Gamma_add_one`, `Real.Gamma_one`, `Real.Gamma_pos_of_pos` | adjacent APIs located; composition and proof credit open |

## Evidence and status boundary

`IntakeProbe.lean` elaborates the candidate and adjacent APIs using the existing pinned toolchain.
The two diagnostic axiom reports are `[propext, Classical.choice, Quot.sound]`. This authenticates
names and checked types only. It does not establish source identity, a canonical expression hash,
terminal proof-body location, complete declaration dependency closure, placeholder/unsafe/oracle
closure, accepted foundation profile, or `M0`.

The human status is provisionally `H1`: a stable named theorem and an explicit modern reference
mapping exist, while primary-source fidelity and independent review are open. The machine status is
`M3`: an exact-topic pinned checked interface exists, but the canonical target and source transport
are not frozen and the formal candidate has not undergone the downstream anchor/provenance audit.
Readability is `R4` because no source-faithful, node-reviewed proof reconstruction exists.
