# Source-statement crosswalk

## Candidate primary sources

- Franz Rellich, "Ein Satz uber mittlere Konvergenz", *Nachrichten von der Gesellschaft der
  Wissenschaften zu Gottingen, Mathematisch-Physikalische Klasse* (1930), 30-35. This is a
  historical source candidate; its exact scope and wording have not yet been inspected.
- V. I. Kondrachov, "On certain properties of functions in the space Lp", *Doklady Akademii Nauk
  SSSR* 48 (1945), 563-566. This is a historical generalization candidate; edition/translation,
  exact theorem, assumptions, and errata remain to be inspected.
- Robert A. Adams and John J. F. Fournier, *Sobolev Spaces*, second edition, Academic Press (2003),
  the compact embedding results in Chapter 6. This is a modern statement source candidate, not yet
  an exact theorem/page citation.

These are discovery anchors, not `H0` evidence. Statement work must inspect a stable edition and
record theorem/page, definitions, assumptions, and errata. The modern formulation must not be
silently attributed verbatim to either historical paper.

## Crosswalk

| Repository phrase | Intended mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| "Sobolev spaces" | `W^{1,p}(Omega)` with weak first derivatives | concrete Sobolev-space predicate/type and norm | included; encoding open |
| "compact embedding" | bounded sequences admit an `L^q`-convergent subsequence | compact inclusion operator or equivalent checked formulation | included; representation open |
| bounded regular domain | Euclidean open set supporting extension/compactness | restricted measure plus explicit geometric hypotheses | included; exact regularity open |
| subcritical exponent | `q < np/(n-p)` for `p < n` | exponent arithmetic with side conditions | included; endpoint encoding open |
| `p >= n` branch | compactness into finite `L^q` targets | explicit branch and finiteness conditions | included; exact source scope open |

## Lean boundary

The legacy blueprint only names broad mathlib analysis, measure, and normed-space APIs; it contains
no target-specific accepted Lean declaration. Intake therefore records no mathlib or external Lean
closure. The anchor-audit phase must search the pinned dependency by exact declaration type and
inspect terminal proof provenance before assigning any machine credit.

Before `H0`, an independent reviewer must verify the selected edition and row-by-row mapping,
including domain regularity, all exponent endpoints, scalar and measure conventions, and errata.
