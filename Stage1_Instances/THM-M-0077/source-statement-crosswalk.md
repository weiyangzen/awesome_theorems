# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:568-573` supplies exactly the title `霍尔定理`, Philip Hall,
1928, the gloss `有限可解群中Hall子群的存在性`, importance "high," and status `已验证`. Git
history attributes all six uncited lines to commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record does not define a Hall subgroup, name
the selected prime set, specify binder order, cite a theorem/page, identify a proof boundary or
errata, name a reviewer, or link a formal artifact.

`Docs/Stage0_Blueprint.md:2217-2242` repeats the same gloss while explicitly leaving the formal
system, foundations, exact definitions and premises, proof process, dependencies, alternate forms,
axioms, machine status, and artifacts open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

The repository has a different target, `THM-M-0815` / `霍尔婚配定理`, in combinatorics. Therefore
the pinned `Mathlib.Combinatorics.Hall` modules are outside this target even though they use the
same surname.

## Historical source lead

Crossref metadata identifies P. Hall, *A Note on Soluble Groups*, *Journal of the London
Mathematical Society* s1-3 (1928), issue 2, pages 98-105, DOI
`10.1112/jlms/s1-3.2.98`. Semantic Scholar independently returns the same title, author, year,
pages, and DOI and marks the article closed. The observed metadata response SHA-256 values are
`063fac8007c85510ce9bd5228a1fe81679d967f84583b1786d51094fd33ef1fd` and
`204915f0fb3fb16326871505489debccad3d9c26865c4d4e54c527281918a212`.

This is bibliographic discovery, not primary-statement evidence. The article text was absent from
the pinned repository and the publisher PDF request returned HTTP 403, so no theorem number, page,
literal proposition, incorporated notation, proof ledger, or errata was inspected. The source
remains `H1`, not `H0`.

## Component crosswalk

| Catalog component | Candidate mathematical reading | Pinned Lean surface | Intake assessment |
|---|---|---|---|
| finite group | `G : Type u`, `[Group G]`, `[Finite G]` | standard finite-group APIs | intended domain; exact binder encoding open |
| solvable | derived series terminates at bottom | `IsSolvable`, `isSolvable_def` | vocabulary authenticated; source convention mapping open |
| Hall subgroup | subgroup with `pi`-supported order and complementary index support | no general Hall-`pi` predicate found | central definition blocker |
| existence | for every allowed `pi`, there exists such a subgroup | no exact general declaration found | canonical expression and proof candidate open |
| `已验证` | untrusted inventory label | reviewed H packet and accepted kernel receipt would be required | no H or M credit |

The common stronger package also asserts conjugacy and containment of `pi`-subgroups. Those are not
present in the catalog gloss and are excluded from the target until source review establishes that
the repository intended the whole family.

## Lean discovery anchors

At the manifest-pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks:

- `IsSolvable` and `isSolvable_def`, which supply the ambient solvability vocabulary;
- `Sylow.card_coprime_index`, a valid one-prime Hall special case;
- `IsZGroup.coprime_commutator_index`, a result for the narrower finite Z-group class; and
- `Subgroup.exists_right_complement'_of_coprime`, which assumes a normal Hall subgroup and gives a
  complement rather than producing the target subgroup.

All three checked theorem bodies report only `propext`, `Classical.choice`, and `Quot.sound` through
`#print axioms`. This is useful intake evidence, but the declarations are not target-equivalent and
receive no proof credit. The anchor-audit phase must repeat a precommitted exhaustive search,
normalize any actual candidate's target, and inspect its terminal body and dependencies.

## Source gate

Before source or statement acceptance, accountable reviewers must obtain and preserve an immutable
primary edition; locate and transcribe the exact theorem and incorporated definitions; determine
whether `pi` is arbitrary and whether the result is existence-only; map every premise and conclusion
to the canonical Lean expression; inspect corrections and errata; and approve all boundary cases.
Until then the human status is `H1`, the machine status is `M4`, and the canonical Lean expression,
environment fingerprint, and alternate transports remain null.
