# Scope map

## Metadata boundary

The repository provides "Taubes's theorem" with the gloss "Seiberg-Witten and Gromov invariants",
Clifford Taubes, and 1994. This identifies the `SW=Gr` theorem family, but not a single formal
proposition. Taubes's papers contain related comparison statements, direction-specific results,
and consequences. Intake must not silently select the easiest member of that family.

## Candidate mathematical boundary

A faithful comparison theorem is expected to require source-fixed versions of:

- a smooth, closed, connected, oriented symplectic four-manifold `(X, omega)` and a compatible or
  tame almost-complex structure;
- the identification among `Spin^c` structures, determinant/Chern classes, and integral
  homology or cohomology classes used to index the invariants;
- the Seiberg-Witten invariant, including orientation, perturbation, expected dimension,
  reducibles, `b2+` and chamber conventions;
- Taubes's Gromov invariant, including pseudoholomorphic currents, point constraints, signs,
  exceptional spheres, tori, and multiple-cover weights;
- the precise equality, including any sign or duality convention and its range of classes; and
- genericity, compactness, transversality, and deformation choices needed for both counts.

The source date in the metadata may point to an early nonvanishing result rather than the later
full comparison formulation. The statement phase must use the mathematical statement, not the
metadata year, to decide the root.

## Variant decision required

The following related claims are not interchangeable:

1. the full equality of source-defined Seiberg-Witten and Gromov invariants;
2. the direction conventionally denoted `SW => Gr`;
3. the converse direction `Gr => SW`;
4. nonvanishing of the Seiberg-Witten invariant of the symplectic canonical class; and
5. existence of pseudoholomorphic representatives or other consequences of the comparison.

The metadata gloss favors item 1. The statement phase must select a pinpoint primary-source
formulation of that equality and explicitly map any direction-specific papers used to establish it.

## Explicit exclusions

- Replacing `SW=Gr` with canonical-class nonvanishing, a symplecticity consequence, or existence
  of one pseudoholomorphic curve.
- Defining two abstract functions to be equal by assumption or making one invariant a synonym for
  the other.
- Restricting to a trivial class, empty moduli space, or specially chosen manifold merely to make
  the equality easy to formalize.
- Suppressing `b2+ = 1` chamber behavior, signs, exceptional classes, or multiple-cover conventions
  when the selected source requires them.
- Treating a bibliography entry, mathematical consensus, or `已验证` as source-review or Lean proof
  evidence.

Before proof-tree construction, the statement phase must freeze the exact source statement,
ordered binders, hypotheses, conclusion, degenerate cases, definitions, foundation/TCB/computation
profiles, minimal imports, elaborated expression and environment fingerprints, checked transports,
and required statement mutations.
