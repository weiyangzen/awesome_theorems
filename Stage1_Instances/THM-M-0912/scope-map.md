# Scope map

## Preserved repository scope

The repository fixes target `THM-M-0912`, the title `帕斯卡恒等式`, attribution to Blaise Pascal,
the year 1654, and the gloss `组合数的递推关系`. This intake preserves the conventional Pascal
recurrence family for ordinary binomial coefficients. Importance `高` and status `已验证` are
catalog metadata, not human-source or kernel evidence.

The received gloss is recognizable but does not state one exact proposition. In particular, it
does not fix the coefficient definition outside the ordinary combinatorial domain or whether the
formula is intended only for valid row/column indices.

## Candidate formulations not credited

1. The source-oriented predecessor formula
   `C(m,n) = C(m-1,n) + C(m-1,n-1)` for natural numbers satisfying `m >= n >= 1`.
2. The all-natural successor formula
   `Nat.choose (Nat.succ r) (Nat.succ k) = Nat.choose r k + Nat.choose r (Nat.succ k)`.
3. The equivalent addition spelling
   `Nat.choose (r + 1) (k + 1) = Nat.choose r k + Nat.choose r (k + 1)`.
4. The positive-column predecessor spelling
   `Nat.choose (r + 1) k = Nat.choose r (k - 1) + Nat.choose r k` under `0 < k`.

The second and third forms are total on `Nat` because mathlib defines out-of-range coefficients as
zero. They strictly include index pairs excluded by the displayed DLMF constraint. The fourth form
uses truncated natural subtraction and a different binder/side-condition presentation. They are
closely related, but source fidelity and any credited transport must be checked rather than assumed.

## Statement-phase decisions

The statement phase now provisionally freezes the source-restricted predecessor formula, natural
binders, `Nat.choose` encoding, ordered premises, conclusion, checked transports, and all listed
boundary dispositions. Dependency-ordered master acceptance remains open. The following source and
review decisions are still required for H0 and later release, but no longer make the conservative
H1 statement expression ambiguous:

1. The exact source edition and locator, including whether the modern DLMF formulation is accepted
   as the canonical source or only a lead toward a historical/primary proof source.
2. The historical relationship between the source's binomial coefficient and the provisionally
   selected recursively defined `Nat.choose` encoding.
3. Independent review of the ordered natural binders and the selected `m >= n >= 1` domain.
4. Independent review of the checked indexing transports and their source fidelity.
5. Whether the recurrence alone is the root or whether boundary equations are incorporated into a
   larger recursive characterization. This intake excludes the latter unless a source requires it.
6. The foundation, TCB, computation, freshness, and source-review profiles for the exact target.

## Degenerate and boundary cases

No case is excluded at intake. Statement review must explicitly test row zero; column zero; the
diagonal `n = m`; the first out-of-range column `n = m + 1`; larger `n > m`; the first positive row
and column; and the effect of truncated subtraction at zero. It must distinguish a theorem whose
hypotheses rule these cases out from the all-natural zero-extended recurrence that includes them.

## Neighbor and substitution boundaries

- `THM-M-0911` (the binomial theorem) is a distinct target. It may use binomial coefficients but
  supplies no inherited statement or proof credit.
- `THM-M-0913` (inclusion-exclusion), `THM-M-0921` (Catalan numbers), and later enumerative targets
  are not alternate Pascal-identity roots.
- Vandermonde's identity, the hockey-stick identity, symmetry of binomial coefficients, factorial
  formulas, multinomial or multichoose recurrences, and Pascal-triangle geometry are not substitutes.
- A finite numerical table, a recursive definition stated as if it were independently sourced, or
  the untrusted `已验证` label supplies no theorem credit.

The statement phase supplies a provisional canonical expression fingerprint. No discovery-protocol
hash, obligation-registry hash, typed graph, accepted task state, or proof closure is frozen yet.
