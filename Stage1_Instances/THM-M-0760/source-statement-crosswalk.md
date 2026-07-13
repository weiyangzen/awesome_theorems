# Source-statement crosswalk

## Repository records and provenance

`Docs/researches/math_theorems.md:5598-5603` supplies the title, attribution John Myhill / Anil
Nerode, year 1958, gloss `正则语言的特征`, importance `高`, and status `已验证`. The uncited block
originates at repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no
definition, formula, theorem/page, assumption list, proof boundary, correction, erratum, or formal
artifact.

`Docs/Stage0_Blueprint.md:20758-20783` projects that row as `THM-M-0760` and explicitly leaves the
formal system, exact definitions and premises, proof route, dependencies, equivalent forms, axioms,
machine status, and artifact links open. Rev-5.6 retains `已验证` only as untrusted metadata and
resets the target to `L0 / rework_required`.

A separate source row, `Docs/researches/cs_theorems.md:233`, describes the same named theorem as
"minimal DFA and distinguishable strings" and is projected to the excluded non-Stage1 record
`THM-C-0134`. That wording is useful scope provenance, but the target sets and descriptions are not
identical. It does not authorize silently adding minimality to `THM-M-0760`.

## Conventional statement leads

PlanetMath's 2013 entries "Myhill-Nerode theorem" and "Nerode equivalence" give a precise public
secondary formulation. For a language `L` over a finite alphabet `A`, DFA recognizability is
equivalent to finiteness of `A* / N_L`; moreover the number of classes is the smallest number of
states in a recognizing DFA. It defines `s1 N_X s2` by agreement of membership after every right
extension and explicitly calls the relation right-invariant, usually not a two-sided congruence.

These entries are useful statement leads, not H0 evidence: they are secondary, lack independent
review here, assume a finite alphabet that the repository gloss omits, and include a minimality
conclusion absent from the pinned mathlib theorem. Observed pages:

- `https://planetmath.org/myhillnerodetheorem`, created/last modified 2013-03-22;
  observed HTML SHA-256 `2e92cc48a7bdabb931a4f7fd9faec0dc6a2028f6f0f8b7f8e23bb71ad07d8cc7`.
- `https://planetmath.org/nerodeequivalence`, created/last modified 2013-03-22;
  observed HTML SHA-256 `dd1f29458b18d08bf4ed2a90ee11cb3df2aeb599e4c0f1588d0ec79e04aba21e`.

Crossref confirms the historical bibliographic lead Anil Nerode, "Linear automaton
transformations," *Proceedings of the American Mathematical Society* 9(4) (August 1958), 541-544,
DOI `10.1090/S0002-9939-1958-0135681-9`. The AMS version-of-record PDF was inspected at intake
(378,668 bytes; SHA-256
`61c6dea6da6ac3c6aff383b6c635629c295a89cfec1b7064b0fb8df734829823`). Its Lemma 2 on journal
page 543 characterizes finite-state automaton transformations by causality and finitely many
intrinsic states and gives a least-state-count conclusion. It concerns stream transformations, not
the exact modern language proposition above. It is therefore a genealogy lead, not an accepted
primary proof source for this root.

The catalog also attributes John Myhill, but no immutable Myhill source, exact statement, or page
was located and inspected in this intake. The historical attribution and relation between the two
original lines of work remain source-audit obligations.

## Literal-to-formal crosswalk

| Repository/source component | Mathematical interpretation | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| regular language | language recognized exactly by a finite-state DFA | `Language.IsRegular` | matching candidate definition located |
| word over an alphabet | finite list of alphabet symbols | `List alpha`; `Language alpha := Set (List alpha)` | matching candidate encoding located |
| indistinguishable prefixes | every right-appended suffix yields the same membership result | equality of `L.leftQuotient x` and `L.leftQuotient y` | extensional correspondence identified; checked transport open |
| finite Nerode index | finitely many equivalence classes/residual languages | `(Set.range L.leftQuotient).Finite` | matching candidate representation located |
| characterization | both DFA-to-finite-index and finite-index-to-DFA directions | `Language.isRegular_iff_finite_range_leftQuotient` | exact-looking candidate, not canonicalized |
| canonical automaton | states are residual languages and it accepts `L` | `Language.toDFA`, `Language.accepts_toDFA` | construction candidate located |
| minimal DFA | class count is a lower bound attained by the canonical DFA | no root conclusion in the pinned theorem | separate source wording; scope decision open |
| finite alphabet | common textbook premise | no such premise in the pinned theorem | proposition-changing domain choice open |
| `已验证` | claimed formal status | accepted kernel receipt would be required | explicitly rejected as evidence |

## Pinned Lean provenance boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, source file
`Mathlib/Computability/MyhillNerode.lean` (SHA-256
`c5e64f8def4527f5e1049d8fa5949fd004b7356326685931a91043d2983eea5e`) defines
`Language.leftQuotient` at lines 33-35 and declares the candidate theorem at lines 101-106. It also
contains both implication lemmas and the residual-state DFA construction. The file originated in
mathlib commit `3f57df84d5d9781f66f1880399a6ca1563c91f63` by Chris Wong (2025-01-20), whose commit message
explicitly distinguishes this residual-range formulation from a quotient by the Nerode relation.

`IntakeProbe.lean` elaborates the named declarations and reports the candidate's current axiom set
as `propext`, `Classical.choice`, and `Quot.sound`. This is bounded candidate discovery only. Intake
does not normalize or hash the canonical target, inspect terminal proof provenance transitively,
accept the axiom/TCB boundary, or assign M0 proof credit; those belong to dependent phases.

## First downstream blocker

The statement phase needs an accountable source decision that selects the exact root strength and
alphabet domain, reconciles the math and computer-science descriptions, maps the residual-range and
relational encodings, audits primary-source genealogy and errata, and obtains independent review.
Only then may it adopt or wrap the pinned candidate, serialize the elaborated expression and
environment fingerprints, compile checked alternate transports, and run all four required mutation
classes. H0 remains unavailable until a pinpoint primary proof source is mapped premise by premise
and independently approved.
