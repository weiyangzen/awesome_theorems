# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:3574-3579` supplies the title `弱哥德巴赫猜想`, attributes its
origin to Christian Goldbach in 1742, and states `大于5的奇数可表为三素数之和`. Git blame
attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record gives no proof source, definitions,
formal artifact, assumptions, dependency boundary, corrections, errata, or reviewer.

`Docs/Stage0_Blueprint.md:13352-13377` repeats the sentence while leaving exact definitions,
premises, proof route, dependencies, axioms, equivalent forms, and machine artifacts open. The
rev-5.6 manifest retains `已验证` only as `source_status_untrusted` and resets the target to
`L0 / rework_required`. These records identify the target but grant no H or M proof credit.

## Inspected proof-source lead

Harald A. Helfgott, *The ternary Goldbach conjecture is true*, arXiv:1312.7748v2, submitted
2013-12-30 and revised 2014-01-17, DOI `10.48550/arXiv.1312.7748`, is an exact primary proof-source
lead. The immutable arXiv source archive has SHA-256
`f2be46b7480bae643083e211dc19b539018950384dc59c1c5faa6e263fd2b366`; its `ternvin.tex` has
SHA-256 `86ea555015d974174c744dbf7b78d777015e959f2986c0b9b6873634f44e0fed`.

The abstract states the claim at source lines 76-79. The unnumbered Main Theorem at lines 123-127
says: "Every odd integer n greater than 5 can be expressed as the sum of three primes." The final
argument at lines 5372-5391 proves odd `N >= 10^27` analytically and invokes the Helfgott-Platt
finite verification through `8.875 * 10^30` to conclude all odd `N > 5`.

This inspection is not an accepted `H0` packet. Later work must immutably admit and crosswalk the
main paper, its cited major-arc and minor-arc results, the companion computation paper and
artifacts/certificates, dependencies, assumptions, corrections, errata, and proof boundary, then
obtain an independent qualified review. Goldbach's 1742 correspondence is historical origin;
Helfgott and the cited dependencies supply the modern proof route.

## Crosswalk

| Repository/source phrase | Mathematical component | Candidate Lean component | Intake status |
|---|---|---|---|
| "odd integer n" | an integer input of odd parity | likely `n : Nat` and `Odd n`, plus checked integer/natural transport | family fixed; encoding not frozen |
| "greater than 5" | strict lower bound excluding 5 and including 7 | likely `5 < n` | family fixed; boundary transport open |
| "three primes" | three positive prime witnesses; repetition permitted | likely `p q r : Nat` and three `Nat.Prime` predicates | family fixed; binders not frozen |
| "sum" / "represented" | exact additive equality | likely `n = p + q + r` | family fixed; expression not frozen |
| every qualifying input | one universal assertion, not an eventual filter | likely `forall n, 5 < n -> Odd n -> ...` | family fixed; quantifier order open |
| analytic range | odd `N >= 10^27` | future major/minor-arc obligation package | primary dependency audit open |
| finite range | computation through `8.875 * 10^30` closes the gap | future certificate/computation-profile obligations | artifacts and trust audit open |
| 1742 / Goldbach | historical origin | no Lean proposition or proof credit | provenance only |
| `已验证` | untrusted repository metadata | no proof object | explicitly rejected |

## Formal boundary

Pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` exposes natural prime,
parity, arithmetic, and finite-decision APIs. The narrow probe validates only those ingredients.
A bounded source search found no Goldbach or sum-of-three-primes terminal theorem in pinned
mathlib. The only exact public Lean declaration already recorded by the neighboring `THM-M-0508`
audit is `TernaryGoldbachConjecture.ternaryGoldbach` in
`google-deepmind/formal-conjectures@b2e608fc52d765510915a244bb69b1a2741acc3c`; its body is
literally `by sorry` and is forbidden evidence. This intake neither imports nor credits it.

`THM-M-0508` owns Vinogradov's eventual three-primes theorem. An eventual threshold statement is
strictly weaker than this all-odd-`>5` target and cannot close or replace `THM-M-0487`.
