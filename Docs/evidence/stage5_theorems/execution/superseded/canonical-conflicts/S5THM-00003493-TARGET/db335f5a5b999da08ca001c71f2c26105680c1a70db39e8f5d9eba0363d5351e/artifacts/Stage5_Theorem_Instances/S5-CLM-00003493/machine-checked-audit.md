# Machine-checked audit: S5-CLM-00003493

The exact frozen source proposition is

```text
∃ Ω : ℕ → ℝ,
  (fun n : ℕ => (Real.iteratedLog n : ℝ)) =O[atTop] Ω ∧
  ∀ n, maximalLength n ≤ n ^ 2 / Real.exp (Ω n)
```

The target files spell the same expression after delta reduction of the four
source-local definitions. `Real.iteratedLog n` becomes the natural infimum of
iteration counts whose iterated real logarithm is at most one;
`maximalLength n` becomes the supremum of lengths of lists whose coordinate
ranges lie in `[1,n]` and whose distinct ordered members are strictly increasing
in two coordinates. This explicit form prevents a same-header/local-shadow
substitution.

`Proof.lean` closes the root as follows. Pigeonhole the first two coordinates of
any list longer than `n²`; two positions collide. Pairwise two-coordinate strict
increase in either position order contradicts those two equal coordinates.
Consequently the supremum is at most `n²`. Let `L` be the unfolded iterated-log
function and choose `Ω n = -L n`. The norm of `-L` equals the norm of `L`, so
`L =O[atTop] -L` follows from reflexive Big-O and negation on the right. Since
`L n ≥ 0`, `exp (-L n) ≤ 1`; its positivity permits division, and dividing
`n²` by it can only increase the bound.

`Audit.lean` independently duplicates the collision lemma, supremum bound, and
root proof instead of importing `Proof.lean`. Trust-zero elaboration succeeds.
The terminal `#print axioms` reports exactly `propext`, `Classical.choice`, and
`Quot.sound` for the root, with no `sorryAx`, claim-specific axiom, unsafe
declaration, opaque oracle, or unreviewed bodyless constant.

The machine cut set is empty. Cold replay starts from the three claim-owned
Lean sources plus the pinned Mathlib checkout; no generated claim object or
provider theorem body is proof authority.
