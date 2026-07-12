# Scope map

## Metadata boundary

The repository supplies the theorem name and only the gloss "rigidity of symplectic structures".
The common theorem attached to Gromov and Eliashberg says, informally, that a C0 limit of symplectic
diffeomorphisms which is itself a diffeomorphism is symplectic. That paraphrase still leaves several
non-equivalent formal targets, so intake cannot yet freeze ordered binders or a conclusion.

## Candidate mathematical boundary

A faithful C0-rigidity statement must select and define at least:

- symplectic manifolds `(M, omega)` and `(M', omega')`, including dimensions, boundary and
  compactness assumptions;
- smooth maps `phi_i : M -> M'` satisfying `phi_i^* omega' = omega`, and whether they are embeddings,
  diffeomorphisms, or symplectomorphisms;
- the C0 topology (compact-open, uniform for chosen metrics, or convergence uniformly on compact
  subsets), and whether convergence of inverse maps is part of the topology;
- the nature of the limit `phi`: a smooth diffeomorphism, a homeomorphism, or merely a continuous
  injection; and
- the exact conclusion: `phi^* omega' = omega`, membership in the symplectomorphism group, or a
  weaker symplectic-homeomorphism notion.

For noncompact manifolds, compact-open convergence and behavior at infinity cannot be replaced by
one unqualified global sup metric. For a merely homeomorphic limit, pullback of a differential form
is not the same statement as for a smooth diffeomorphism.

## Variant decision required

The source-review and statement phases must distinguish at least these related roots:

1. C0 closure of symplectic diffeomorphisms inside the smooth diffeomorphism group;
2. a local/embedding form for uniformly convergent symplectic embeddings with a smooth limit;
3. the broader definition and properties of symplectic homeomorphisms as C0 limits; and
4. rigidity results used in proofs, such as nonsqueezing or symplectic-capacity preservation.

The likely metadata interpretation is item 1, but that preference is not a canonical statement
until it is crosswalked to a pinpoint source formulation.

## Explicit exclusions

- Replacing the theorem by Gromov nonsqueezing, even if nonsqueezing is a proof input.
- Assuming in a hypothesis that the limit preserves the symplectic form.
- Proving continuity of pullback under C1 convergence and calling it C0 rigidity.
- Restricting to the identity sequence, dimension zero, or a single linear map to obtain an easy
  Lean proposition.
- Defining "symplectic homeomorphism" to mean a C0 limit and presenting the definition alone as the
  smooth-limit rigidity theorem.
- Treating `已验证`, consensus, or a bibliographic citation as source or kernel evidence.

Before tree construction, the statement phase must freeze the exact source edition and theorem,
domains, ordered binders, topology, hypotheses, conclusion, boundary cases, profiles, minimal
imports, declaration type, expression/environment fingerprints, alternate-form transports, and
required statement mutations.

