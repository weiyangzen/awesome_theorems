# Proof outline

## Uniform bound

Fix a natural number `n` and an admissible list `s` of triples. Suppose for contradiction that its length exceeds `n²`.

Map each position of `s` to the ordered pair consisting of the first two coordinates of its triple. Every coordinate belongs to `[1,n]`, so every image lies in the product `[1,n] × [1,n]`, which has exactly `n²` elements. There are more positions than target pairs. The finite pigeonhole principle therefore supplies distinct positions `i` and `j` whose triples agree in coordinates `0` and `1`.

The list's pairwise condition compares the earlier position with the later one. Whichever of `i` and `j` is earlier, it must be strictly smaller in two distinct coordinates. But neither coordinate `0` nor coordinate `1` can be strictly smaller, because those coordinates are equal. Among three coordinates only coordinate `2` remains, so two distinct strict-growth coordinates are impossible. This contradicts pairwise 2-increase and proves that every admissible length is at most `n²`.

## Supremum and exact root

The empty list shows that the defining set of lengths is nonempty. Since the uniform bound applies to every member, the natural supremum is consequently at most `n²`.

The source's notation `F n` abbreviates precisely this supremum, `IsIncreasing₂` is the pairwise condition, and `lt₂` is the explicit two-coordinate witness. `Statement.lean` records the bidirectional set-level normalization; `Proof.lean` proves the fully expanded proposition without relying on a provider proof body.
