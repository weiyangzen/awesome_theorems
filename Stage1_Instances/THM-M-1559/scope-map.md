# Scope map

## Included problem family

- A finite set of singular points on the complex projective line and finite-dimensional complex
  monodromy data for its punctured complement.
- Existence of a linear differential system or connection realizing that monodromy.
- A regular-singular/Fuchsian condition, with the exact distinction fixed from the selected source.
- Both the historically claimed positive result and the later counterexample boundary, so the
  canonical target cannot silently encode a false unrestricted assertion.

## Decisions required by the statement phase

The chosen source must fix whether the data are a representation or conjugacy classes; rank,
irreducibility, singular set, inclusion of infinity, bundle triviality, allowed apparent
singularities, and equivalence up to gauge/conjugacy. It must also distinguish a logarithmic
connection on some holomorphic vector bundle from a Fuchsian system on the trivial bundle. These
choices change the truth value and are not notation details.

## Explicit exclusions

- Treating "integrable systems" as a formal statement or substituting an unrelated inverse-scattering result.
- Claiming unrestricted realization on the trivial bundle without addressing counterexamples.
- Replacing regular singularities by arbitrary meromorphic connections or adding apparent poles unnoticed.
- Encoding the desired system as an assumed structure field.
- Crediting a non-Lean proof, a library API, or an abstract existence hypothesis as kernel closure.

The later Lean target needs concrete encodings of the punctured sphere, fundamental-group
representation/monodromy, holomorphic or meromorphic connection, regular singularity, and the
chosen equivalence relation, or a precise API blocker for each absent interface.
