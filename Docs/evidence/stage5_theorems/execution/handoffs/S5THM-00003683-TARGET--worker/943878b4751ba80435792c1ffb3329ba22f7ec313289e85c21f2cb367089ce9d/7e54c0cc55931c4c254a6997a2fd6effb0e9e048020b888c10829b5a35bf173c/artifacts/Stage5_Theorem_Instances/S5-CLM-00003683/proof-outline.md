# Proof outline

1. Package `n` and the bound `h : n < 2^50` as `⟨n,h⟩ : Fin (2^50)`.
2. Apply the audited finite certificate to that value, `Odd n`, and `1 < n`.
3. Destructure the result into `k : Fin (2^50)`, `l : Fin 50`, squarefreeness of `k.1`, and the required sum equality.
4. Forget the finite bounds and return `k.1` and `l.1` as natural witnesses.

The certificate is a finite data obligation, not a hidden theorem oracle: its full type is exposed at the root trust boundary and its entries can be independently generated, mutated, and replayed. No hypothesis or exceptional boundary case is discarded.
