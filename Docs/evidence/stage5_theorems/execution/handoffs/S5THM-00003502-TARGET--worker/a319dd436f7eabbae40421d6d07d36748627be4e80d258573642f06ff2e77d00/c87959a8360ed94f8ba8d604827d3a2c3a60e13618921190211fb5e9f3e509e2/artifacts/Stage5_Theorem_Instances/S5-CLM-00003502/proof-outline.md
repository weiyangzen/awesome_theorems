# Proof outline

1. Freeze the provider proposition `IsCancellative k k[X]` and its source declaration locator.
2. Transparently unfold `IsCancellative`: for every finitely generated commutative `k`-algebra `B`, a stable algebra equivalence `k[X][X] ≃ₐ[k] B[X]` must yield `k[X] ≃ₐ[k] B`.
3. Check both directions of the proposition-level transport, with no local reinterpretation of any source symbol.
4. Represent the inference explicitly: specialize the universally quantified closure at `B`, consume the stable equivalence hypothesis, and return the required nonempty algebra equivalence.
5. Re-elaborate the transport and composition in the independent audit surface at trust zero.

The exceptional boundary is the provider proof body: it is sorry-backed and supplies statement identity only, never target machine closure.
