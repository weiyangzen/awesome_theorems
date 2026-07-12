# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:463-468` supplies exactly the title `西罗定理`, Ludwig Sylow,
1872, the gloss `有限群中p-子群的存在性、共轭性和计数`, importance "high," and status `已验证`.
Git history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no definition of `p`-subgroup,
formula, binder order, hypotheses, theorem locator, proof boundary, errata, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:1812-1837` repeats the same gloss while explicitly leaving the formal
system, foundation, exact definitions and premises, proof process, dependencies, alternate forms,
axioms, machine status, and artifact links open. Its generic statement that a closed result is known
is planning metadata. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Inspected primary source

L. Sylow, *Théorèmes sur les groupes de substitutions*, *Mathematische Annalen* **5** (1872),
584-594, DOI `10.1007/BF01442913`, JFM `04.0056.02`, is the exact historical source lead. An open
11-page scan from Zenodo record `2329278` was inspected; its SHA-256 is
`92a14121c0b0344aefeb9a8ba8a78d685443d5f97dc8bb3663144cab830415bf`.

- Theorem I, printed page 586, says that if `n^alpha` is the largest power of the prime `n`
  dividing the order of `G`, then `G` contains a subgroup `g` of order `n^alpha`. Its accompanying
  order formula records the relevant normalizer factor.
- Theorem II, printed page 587, says that all subgroups of that order are obtained by transforming
  any one of them by substitutions of `G`, and that their exact number has the form `n*p + 1` in
  the paper's notation. It also records how many transformations produce each subgroup.

This is strong primary discovery evidence, not `H0`. The paper speaks in the historical language of
finite substitution groups, its notation must be reconstructed carefully from the preceding setup,
and the general finite-group transport and modern normalizer/divisibility formulation require an
accepted crosswalk. No independent source reviewer or complete proof-node mapping exists here.

## Component crosswalk

| Catalog component | Primary-source component | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| finite group | finite substitution group `G` | `[Group G] [Finite G]` | modern scope intended; historical transport open |
| prime `p` | prime `n` | `p : Nat`, `[Fact p.Prime]` | direct role; notation differs |
| `p`-subgroup existence | subgroup of order the largest `p`-power dividing `|G|` | `Sylow.nonempty`, `Sylow.exists_subgroup_card_pow_prime`, `Sylow.card_eq_multiplicity` | exact canonical encoding open |
| conjugacy | all subgroups of that order are transforms of one another | `Sylow.isPretransitive_of_finite`, `MulAction.exists_smul_eq` | candidate action encoding only |
| counting | number has form `n*p + 1`, with transformation/normalizer factor | `card_sylow_modEq_one`, `Sylow.card_dvd_index`, `Sylow.card_eq_index_normalizer` | precise conjunction and source mapping open |
| `已验证` | untrusted inventory label | reviewed H packet and accepted kernel receipt would be needed | no H or M credit |

## Lean discovery anchor

At the manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Mathlib.GroupTheory.Sylow` documents the same
three-part family and defines a Sylow subgroup as a maximal `p`-subgroup. The closest declarations
are:

- `Sylow.nonempty`, `IsPGroup.exists_le_sylow`, `Sylow.exists_subgroup_card_pow_prime`, and
  `Sylow.card_eq_multiplicity` for existence and order;
- `Sylow.isPretransitive_of_finite` together with `MulAction.exists_smul_eq` for conjugacy; and
- `card_sylow_modEq_one`, `Sylow.card_dvd_index`, and
  `Sylow.card_eq_index_normalizer` for counting.

`IntakeProbe.lean` imports only that module and elaborates representative uses of each branch under
a finite group and prime. This verifies availability and type compatibility, not an exact combined
target, proof provenance, or M0 closure. The formal anchor audit must separately normalize the
selected statement, resolve wrappers and terminal bodies, inspect dependency and axiom closure,
and bind any accepted result to a repo-local wrapper and content-addressed receipt.

## Source gate

Before `H0` or statement acceptance, accountable reviewers must preserve an immutable source
edition, transcribe and independently check Theorems I-II and their incorporated notation,
determine the exact modern general-finite-group bridge, select every counting clause, map all
premises and conclusions to the canonical Lean target, inspect corrections and errata, and approve
the trivial and nondividing-prime cases. Until then the source is `H1` and the canonical Lean
expression and fingerprint remain null.
