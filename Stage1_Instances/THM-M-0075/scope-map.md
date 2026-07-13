# Scope map

## Received claim

The preserved catalog claim is only `阿廷定理: 关于诱导特征标的线性无关性`, attributed to Emil
Artin in 1931. It recognizes a finite-group character-theory area but does not yet determine a
stable mathematical proposition.

## Proposition-changing decisions

The statement phase must resolve all of the following before elaborating a canonical target:

1. Whether the catalog intended Artin's induction theorem, its cyclic-subgroup corollary, a
   rational-character/permutation-character variant, or an actual independence theorem.
2. Whether `G` is finite, and whether subgroups are arbitrary, cyclic, elementary, proper, or a
   conjugacy-stable selected family.
3. Whether inducing maps arise from subgroup inclusions, injective group homomorphisms, or another
   convention, and how conjugate or duplicate subgroups are indexed.
4. Whether characters are ordinary complex characters, irreducible characters, rational-valued
   characters, linear characters, virtual characters, or class functions.
5. Whether the coefficient object is `Z`, `Q`, `C`, a character ring, its scalar extension, or a
   module of class functions.
6. Whether the conclusion is linear independence, rational spanning, finite cokernel, an equality
   after multiplying by a positive integer, or an equivalence with subgroup conjugate coverage.
7. Whether the general family theorem or only the cyclic-family corollary is the root, and which
   implication directions and equivalent formulations are included.
8. How zero rings/modules, the trivial or empty group, empty subgroup families, zero characters,
   repeated induced characters, and conjugate subgroups are treated.

## Candidate roots not credited

- Serre Theorem 17: conjugate coverage by a subgroup family iff the direct-sum induction map on
  virtual-character rings has finite cokernel.
- Serre's cyclic corollary: every ordinary complex character is a rational linear combination of
  characters induced from characters of cyclic subgroups.
- The rational-character variant using induced trivial/permutation characters of cyclic subgroups.
- A literal linear-independence theorem for a source-defined, duplicate-free family of induced
  characters; no such source proposition has yet been identified.

These statements have different domains and conclusions. None may be selected merely because it is
familiar or easier to encode.

## Boundary cases to resolve

- the trivial finite group and the zero virtual character;
- an empty subgroup family and a family containing `G` itself;
- repeated subgroups, conjugate subgroups, and repeated or equal induced characters;
- cyclic subgroups of order one;
- source characters that are reducible, irreducible, virtual, zero, or Galois-conjugate;
- denominators in rational decompositions and the integer multiplier `d`;
- finite-cokernel versus surjectivity after scalar extension;
- restriction/induction conventions and universe choices in Lean.

No degenerate case is excluded at intake.

## Excluded substitutions

- Dedekind's linear independence of distinct monoid or field homomorphisms;
- independence/orthogonality of irreducible characters;
- the definition or existence of induced representations;
- Frobenius reciprocity or the induction-restriction adjunction alone;
- Maschke's theorem or complete reducibility;
- Brauer induction, modular/Brauer character results, or Artin L-function continuation;
- a finite-group, cyclic-group, abelian-group, or one-dimensional special case unless selected by
  the accepted source proposition;
- a hypothesis, structure field, or class asserting the desired decomposition or independence;
- the catalog's `已验证` label or a passing discovery probe as proof evidence.

## Neighbor and related-target boundaries

| Target or surface | Boundary |
|---|---|
| `THM-M-0066` / Schur's lemma | possible character-theory infrastructure, not Artin induction or induced-character independence |
| `THM-M-0067` / Maschke's theorem | semisimplicity infrastructure for finite-group representations, not the target conclusion |
| `THM-M-0076` / Brauer character theorem | separately owned modular-character family; not permission to replace Artin's theorem by Brauer induction |
| `THM-M-0429` / Brauer theorem for Artin L-functions | analytic continuation target whose legacy file mentions missing Brauer induction; no proof credit transfers |
| Dedekind character independence in mathlib | distinct monoid homomorphisms are independent; the objects are not induced representation characters |

## Formal boundary

Pinned mathlib has representation induction and finite-dimensional representation characters, but
the bounded intake search found no virtual-character-ring Artin induction theorem or a theorem
matching the catalog's literal independence gloss. Because the human claim is unresolved, the
canonical Lean module, expression, expression hash, environment fingerprint, alternate transports,
mutation tests, obligation registry, and discovery protocol remain null. `IntakeProbe.lean` checks
only adjacent APIs and is not a target statement.

## Current boundary

This intake freezes an ambiguity and a source mismatch; it does not resolve either. The root remains
`[H1, M4, R4]`, audit and theorem completion are false, and all downstream tasks remain open.
