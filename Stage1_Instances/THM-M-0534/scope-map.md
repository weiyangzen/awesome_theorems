# Scope map

## Included theorem family

- A short exact sequence `0 -> A -> B -> C -> 0` of homological chain complexes in an abelian
  category, with the same complex shape and explicit adjacent indices.
- The degreewise homology maps induced by the two chain maps.
- A connecting morphism from the homology of `C` in one degree to the homology of `A` in the next
  degree, using the selected homological indexing convention.
- Exactness at every position of the resulting repeated homology sequence.
- Naturality of the connecting morphism only if it belongs to the selected source statement.

## Topological interpretation to freeze

The repository category is algebraic topology, but its wording does not specify how spaces enter.
The statement phase must choose, from an inspected source, one of these noninterchangeable roots:

1. the general chain-complex theorem, later applicable to singular chain complexes;
2. the long exact homology sequence of a pair `(X, A)`, obtained from the relevant quotient short
   exact sequence of singular chain complexes;
3. the long exact sequence of a triple `B subset A subset X`;
4. an exactness axiom for an abstract homology theory.

It must also freeze the abelian target category or coefficient ring, chain versus cochain direction,
integer/natural/general index type, degree shift and sign, reduced versus unreduced homology,
relative-homology encoding, naturality, and boundary behavior at degree zero. These choices affect
domains, binders, maps, or conclusions rather than notation alone.

## Explicit exclusions

- The Mayer-Vietoris sequence, Ext/Tor long exact sequences, or a spectral sequence as substitutes.
- Merely proving that consecutive maps compose to zero without exactness.
- A finite six-term window presented as the entire unbounded sequence without a quantified local
  exactness formulation.
- A structure or hypothesis that contains the desired connecting map and exactness as assumed data.
- Reusing `THM-M-0001` or its legacy wrapper as accepted status for this separately owned target.
- Treating the repository metadata value `verified` as source or kernel evidence.

The later exact Lean target must quantify the local exactness windows needed to express the whole
sequence and must crosswalk any topological specialization to the chain-level theorem by checked
constructions.
