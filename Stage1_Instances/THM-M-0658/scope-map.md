# Scope map

## Repository boundary

The literal claim is only "stability theory", attributed to Saharon Shelah and dated 1978. That
phrase denotes a research theory, not a proposition with fixed binders and a conclusion. The
intake therefore freezes the ambiguity itself. A later phase must select a precise result from an
inspected primary source; it may not infer one merely from the title or date.

## Candidate mathematical surfaces

| Surface | Choices that change the proposition | Intake status |
|---|---|---|
| Stability notion | counting complete types over parameter sets/models; stability in one cardinal; absence of the order property | unresolved; no equivalence is assumed |
| Theory | complete first-order theory versus an arbitrary or consistent theory | unresolved |
| Language | arbitrary cardinality, countable language, finite relational language, or named-constant expansion | unresolved |
| Variables and parameters | one formula, one finite tuple arity, all finite arities, types over sets, or types over models | unresolved |
| Cardinal scope | omega-stability, stability in a fixed `kappa`, eventual spectrum, or a bound depending on `|T|` | unresolved |
| Substantive root | a definition/characterization, a spectrum theorem, a rank/forking theorem, or a classification consequence | no root selected |
| Ambient model | ordinary structures versus saturated or monster-model conventions | unresolved |
| Foundations | compactness/completeness, classical choice, and cardinal arithmetic | exact dependency profile open |

## Exclusions and guards

- A definition of a locally chosen `TypeCountingStableAt` predicate is not by itself a theorem of
  Shelah stability theory.
- Omega-stability, superstability, total transcendence, simplicity, and forking independence are
  related but cannot silently replace generic stability.
- A finite-tuple, parameter-free type count cannot replace quantification over the source's
  parameter sets or models.
- A theorem about one stable example, or a tautology assuming the desired spectrum conclusion, is
  not the root.
- `THM-M-0659` (Shelah classification theorem), `THM-M-0660` (principal formula theorem), and
  `THM-M-0661` (forking independence) are separately scheduled targets and provide no inherited
  scope or proof credit.
- The manifest's `已验证` label and the elaborating intake probe are not mathematical or machine
  proof evidence.

## Statement-phase requirements

The next phase must pinpoint an immutable primary edition and exact theorem/page, audit definitions
incorporated by reference and errata, and justify why that theorem is the repository's intended
root. It must then freeze universes, ordered binders, theory completeness, formula/type arity,
parameter/model quantification, cardinal hypotheses and arithmetic, conclusion, and boundary cases.
Only then may it elaborate a canonical Lean expression, add checked transports, and mutation-test
the proposition-changing choices above.
