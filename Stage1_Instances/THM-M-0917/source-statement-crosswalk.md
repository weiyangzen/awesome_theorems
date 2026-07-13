# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:6707-6712`, introduced by repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`, contains the complete catalog record:

- title: `分拆函数` (partition function);
- attribution: Leonhard Euler;
- year: 1748;
- gloss: `整数分拆的计数` (counting integer partitions);
- importance: high; and
- formalization status: `已验证`.

`Docs/Stage0_Blueprint.md:25012-25037` repeats the record and explicitly leaves the precise
definition and premises, proof route, equivalent forms, axioms, current machine status, and artifact
links open. The rev-5.6 manifest preserves `已验证` only as `source_status_untrusted` and resets the
target to `L0 / rework_required`. These secondary inventory rows establish identity provenance, not
a primary theorem statement, H evidence, or Lean proof receipt.

## Historical-source boundary

The attribution and year plausibly point toward Euler's 1748 *Introductio in analysin infinitorum*,
but the catalog gives no title, volume, chapter, proposition, page, edition, or formula. An Euler
Archive metadata page for volume 1 was inspected only as a bibliographic lead; it identifies the
1748 Lausanne volume and an 1885 German translation, but it does not establish which partition
claim the catalog intended. A full immutable source passage, its incorporated definitions, proof
boundary, translation differences, corrections, and independent review are not accepted here.
Consequently the literal record is `H5`, not `H0` or `H1`: it is not yet a stable proposition. This
does not classify any corrected source-selected Euler theorem.

## Literal clause crosswalk

| Repository element | Required mathematical decision | Pinned Lean surface | Intake result |
|---|---|---|---|
| `分拆` / integer partition | positive parts, unordered equality, representation | `Nat.Partition n` | compatible definition located; source transport open |
| "function" | symbol, input domain, codomain, totalization | `fun n : Nat => Fintype.card (Nat.Partition n)` | viable encoding only; not a selected theorem |
| "counting" | what class is counted and whether equality to an encoding is asserted | `Fintype.card`; finite instance | interface elaborates; conclusion absent |
| Euler / 1748 | exact work, edition, chapter/page, statement, proof and errata | documentation/provenance only | bibliographic lead; no pinpoint admission |
| `已验证` | independently accepted human and machine evidence | source crosswalk plus kernel receipts required | no H or M proof credit |

## Candidate-form boundary

The following are mathematically related but inequivalent and uncredited:

| Candidate claim | Why it cannot be inferred from the gloss |
|---|---|
| `p(n) = #(Nat.Partition n)` | this may merely define `p`; the source representation and theorem direction are not selected |
| `p(0) = 1`, `p(1) = 1` | boundary facts do not determine the general root |
| Euler product / pentagonal recurrence | this is a substantive identity and overlaps `THM-M-0916` |
| odd-parts equals distinct-parts | this is Euler/Glaisher's restricted-partition theorem, a different claim |
| Hardy-Ramanujan or Rademacher formula | these have separate targets, dates, sources, analytic binders, and conclusions |
| a recurrence, congruence, or computed table | each selects additional mathematics absent from the catalog |

## Lean discovery boundary

Pinned `Partition.Basic` defines `Nat.Partition` and its `Fintype`; `Partition.GenFun` supplies a
generic character-weighted power series and product theorem. The module explicitly records the
ordinary constant-one partition-function specialization as a TODO. Pinned `Partition.Glaisher`
proves restricted-count and odd/distinct identities, but those do not close this unspecified root.

The bounded repository search found no repo-local canonical THM-M-0917 declaration. Existing
THM-M-0510/0511 material uses `Fintype.card (Nat.Partition n)` for their own source-selected analytic
claims and transfers no statement or proof credit. These observations are intake discovery, not the
later immutable anchor audit and not a global claim that no external formalization exists.

Before `STATEMENT` may elaborate a target, the integration/source-review lane must approve one
truth-valued proposition and a pinpoint immutable source crosswalk. It must then freeze every
binder, premise, conclusion, boundary convention, representation transport, and mutation test.
