# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6040-6045` and `:7036-7041` contain identical rows: the
Erdős-Ko-Rado name, attribution Erdős/Ko/Rado, year 1961, and the complete gloss `相交族的最大大小`
(maximum size of an intersecting family). Git history places both uncited rows in commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. Their identical SHA-256 excerpts confirm duplication;
the second occurrence is not independent evidence and the rev-5.6 manifest allocates one target.

`Docs/Stage0_Blueprint.md:22442-22467` repeats the gloss while leaving exact definitions and
premises, proof route, dependencies, alternate formulations, axioms, machine state, and artifact
links open. The rev-5.6 manifest retains `已验证` only as untrusted metadata and resets this target to
`L0 / rework_required`.

## Primary-source lead

P. Erdős, Chao Ko, and R. Rado, *Intersection theorems for systems of finite sets*, *Quarterly
Journal of Mathematics, Oxford Series (2)* 12 (1961), 313-320, DOI
`10.1093/qmath/12.1.313`. The inspected scan is archive item `1961-07` in the Alfréd Rényi
Institute's Collected Papers of Paul Erdős, at
`https://www.renyi.hu/~p_erdos/1961-07.pdf`; its observed SHA-256 is
`e53f1ec72accc8e55ec8da360588b224542a9133216d4b82a6918bbe309ac821`.
Crossref independently confirms the authors, title, journal, volume, issue, year, pages, and DOI.

On printed page 313, section 2 defines `S(k,l,m)` as systems of subsets of `[0,m)`, each of
cardinality at most `l`, such that distinct members are pairwise incomparable and their pairwise
intersections have cardinality at least `k`. Theorem 1 then states, in modern notation:

```text
1 <= l <= m / 2 and (a_0, ..., a_{N-1}) in S(1,l,m)
  implies N <= choose (m - 1) (l - 1).
```

It additionally gives a strict bound if one member has cardinality below `l`. Printed page 314
remarks that the bound is best possible when every member has cardinality `l`: take all `l`-sets
containing a fixed `k`-set; at `k = 1` this is the usual star family. Pages 314-316 prove Theorem 1
using Sperner's shadow lemma and induction.

This is a direct primary source. Guided by the catalog's literal "maximum size" gloss, the statement
phase provisionally selects Theorem 1's positive uniform specialization together with the following
star witness. It does not select the broader printed theorem or a modern equality classification.
The scan has no displayed erratum notice, but no systematic corrections search or independent
reviewer has accepted the crosswalk. Status is therefore `H1`, not `H0`.

## Component crosswalk

| Source/catalog component | Primary-source meaning | Pinned Lean candidate | Intake assessment |
|---|---|---|---|
| finite ground set | `[0,m)` has `m` elements | `Fin n` | selected labeled finite model after renaming; no abstract-type transport credited |
| family | a finite indexed antichain of subsets | `Finset (Finset (Fin n))` | duplicates are absent; only the uniform specialization is selected |
| member size | Theorem 1 uses `card <= l` together with incomparability | `Set.Sized r`, hence `card = r` | candidate is the uniform specialization, not the full printed premise |
| intersecting | distinct members meet in at least one point | `Set.Intersecting`, including the self-pair | checked equivalent to distinct-pair intersection under selected `1 <= r` and uniformity |
| range | `1 <= l <= m / 2` | `1 <= r` and `r <= n / 2` | exact positive range selected; equality boundary included |
| upper bound | `N <= choose (m-1)(l-1)` | `card A <= choose (n-1)(r-1)` | exact for the uniform positive-parameter specialization |
| sharpness | following remark supplies a star construction | `erdosKoRadoStar_attains` checks the construction | attainment is checked; universal upper-bound proof remains uncredited |
| equality cases | no full extremizer classification in Theorem 1 | absent | cannot be inferred from the candidate |
| `已验证` | untrusted catalog label | no receipt | no H or M credit |

## Lean candidate boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, module
`Mathlib.Combinatorics.SetFamily.KruskalKatona` declares:

```text
Finset.erdos_ko_rado
  {A : Finset (Finset (Fin n))} {r : Nat}
  (hA : (A : Set (Finset (Fin n))).Intersecting)
  (hr : (A : Set (Finset (Fin n))).Sized r)
  (hhalf : r <= n / 2) :
  A.card <= (n - 1).choose (r - 1)
```

The declaration entered mathlib in commit
`174e4bd31d28b82604fc68a45c04fbc15140c394` (`feat: The Erdős–Ko–Rado theorem`) and its terminal
body is in pinned mathlib, not this repository. `IntakeProbe.lean` elaborates the exact declaration
and reports `[propext, Classical.choice, Quot.sound]`. This establishes a credible pinned candidate
and supports `M3` discovery status only. The statement phase selects and elaborates the exact
positive uniform maximum-value claim, tests boundaries and mutations, and compiles the
source-intersection bridge and concrete-star transport. The anchor-audit phase must next audit proof-body provenance,
dependencies, placeholders, trust, and candidate completeness before any `M0-W` proposal.

The printed `S(1,l,m)` conditions range over distinct indices. At `l = 1`, a one-member system
whose member is empty is therefore vacuously admissible, while the printed strict-if-one-member-is-
smaller clause would appear to demand `1 < choose (m - 1) 0 = 1`. This may reflect an implicit
nonempty-member or family-size convention, or a degenerate exception. The intake does not repair the
source silently; independent source and correction review must resolve it. Mathlib's self-pair
`Set.Intersecting` convention instead forces an `r = 0` family empty.

## Required source admission

Before leaving H1, accountable reviewers must admit an immutable complete edition, review the
provisional source proposition and incorporated sharpness remark, map every binder, premise,
definition, conclusion, and boundary case, search corrections and errata, and independently review
the translation. The statement is now frozen as a kernel expression; before upper-bound proof
credit, its relationship to `Finset.erdos_ko_rado` must be checked and provenance-audited rather
than inferred from the eponym.
