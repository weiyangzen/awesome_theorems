# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:11665-11670` supplies exactly the title `算法信息论`, attribution
to Ray Solomonoff/Andrey Kolmogorov/Gregory Chaitin, the period 1960s, the gloss `信息的算法理论`,
importance `high`, and status `verified`. Git history places all six uncited fields in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`.

`Docs/Stage0_Blueprint.md:43039-43064` repeats the metadata but explicitly leaves the target formal
system and foundation, exact definitions and premises, proof route, dependencies, equivalent
forms, axiom policy, machine-checked status, and artifact links open. The rev-5.6 manifest preserves
`verified` only as untrusted metadata and resets the target to `L0 / rework_required`.

The catalog has no bibliography, theorem/page locator, formal object, machine model, encoding,
ordered binder, hypothesis, conclusion, constant convention, incorporated definition, proof
boundary, correction record, or reviewer. `The algorithmic theory of information` describes a
field rather than one stable truth-valued proposition.

## Literal crosswalk

| Catalog element | Material interpretations | Prospective Lean surface | Intake assessment |
|---|---|---|---|
| `algorithmic information theory` | complexity, incompressibility, algorithmic probability, randomness, induction, incompleteness, and Omega results | one exact source-versioned `Prop` | field label, not a proposition |
| `information` | finite description length, universal probability, randomness deficiency, or another source-defined quantity | encoded objects, machine semantics, length/probability definition | object and invariant absent |
| `algorithmic theory` | partial computability, prefix machines, semicomputable semimeasures, tests, or formal theories | computability model and representations | model and quantifiers absent |
| Solomonoff/Kolmogorov/Chaitin | distinct programs and theorem families with related independent origins | provenance and node mapping only | no result or source selected |
| `1960s` | broad origin period spanning multiple definitions and publications | immutable source locator only | not an exact result locator |
| `verified` | untrusted inventory field | accepted source review and kernel receipt would be required | no H or M credit |

## Source-family boundary

The attribution is historically consistent with a field jointly developed through Solomonoff's
algorithmic probability and induction, Kolmogorov's complexity definition and invariance program,
and Chaitin's independently developed program-size complexity, incompleteness, and halting
probability. That correspondence does not identify a single source theorem.

No primary source is cited in the repository, and intake does not select one from memory. A source
audit must separately inspect a lawful immutable edition and exact result locator for whichever
root an accountable correction chooses, including translations, revisions, errata, incorporated
definitions, assumptions, and proof boundary. Historical attribution alone is not `H0` evidence.

The adjacent math records strengthen the non-substitution boundary. `THM-M-1582` separately names
Kolmogorov complexity and gives the gloss `minimum description length of an object`;
`THM-M-1584` separately names Chaitin's uncomputable number. The computer-science catalog also has
a separate Kolmogorov-complexity row at `Docs/researches/cs_theorems.md:647` and an
incompressibility row at line 648. Their statements and status do not transfer to this target.

## Candidate-root discrimination

| Candidate root | Required defining choices | Why not canonical at intake |
|---|---|---|
| invariance theorem | two description systems, universality/optimality, complexity definition, additive constant and its dependencies | catalog selects neither systems nor theorem |
| incompressibility counting | finite alphabet/strings, length, description system, deficit, strict boundary, counting measure | separately named neighboring family and absent binders |
| complexity uncomputability | plain/prefix complexity, fixed optimal machine, exact computability or approximation claim | conclusion and machine convention absent |
| coding theorem | universal semimeasure, prefix complexity, logarithm base, additive/multiplicative constants | probability objects and normalization absent |
| randomness characterization | infinite-sequence representation, effective tests, prefix complexity, constant quantifiers | catalog does not mention randomness |
| Solomonoff convergence | environment class, predictor, posterior, loss/convergence mode | catalog does not select induction |
| Chaitin result | prefix-free machine, Omega or formal theory, randomness/uncomputability/incompleteness conclusion | separately owned Omega-style target |

Choosing or conjoining any row would add mathematics not present in the source record.

## Lean discovery boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
`Nat.Partrec.Code`, its encoding and evaluation, `Nat.Partrec.Code.exists_code`,
`Nat.Partrec.Code.eval_part`, `InformationTheory.UniquelyDecodable`, and
`InformationTheory.kraft_mcmillan_inequality`. A bounded exact-topic search found no declaration
for algorithmic information, Kolmogorov complexity, universal prefix machines, Solomonoff
induction, or Chaitin Omega in repository-local Lean or pinned mathlib. The unrelated word
`incompressible` occurs in fluid-mechanics files and is excluded.

These are discovery facts only, not an exhaustive external anchor audit or proof of global
absence. The checked code evaluator is not prefix-free by itself, and Kraft-McMillan for finite
uniquely decodable codes does not define or prove a complexity invariance, coding, randomness,
induction, or Omega theorem.

## Source and statement gate

Before ordinary theorem-proof execution, an accountable owner must correct, redirect, or split the
field label into one stable proposition; preserve and hash a lawful primary source edition; select
an exact result and proof boundary; transcribe every incorporated definition, ordered binder,
hypothesis, conclusion, representation, constant dependency, and boundary case; reconcile the
neighboring target ownership; audit corrections and translations; and obtain independent source
review.

Only after that decision may the statement phase freeze minimal imports, a canonical Lean
expression, checked transports, expression and environment fingerprints, and the required removed-
hypothesis, changed-domain, binder-scope, and boundary mutations. Until then, `H5` records only
that the received field label is non-propositional. No exact statement or proof is claimed.
