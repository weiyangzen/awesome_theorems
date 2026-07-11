# THM-M-0171 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the source label "Gromov embedding theorem."
The repository metadata supplies only "a necessary-and-sufficient condition for metric-space
embedding," attributes it to Gromov, and gives 1986. Those fields do not uniquely identify a
mathematical theorem. The intake therefore preserves the ambiguity rather than silently replacing
it with the convenient Kuratowski theorem found in the legacy Lean file.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | The exact theorem meant by the metadata | Open: no primary source, publication, theorem number, or complete claim is identified |
| Provisional discovery branch | Separable metric spaces embed isometrically into `l-infinity(N, R)` | Candidate only; the legacy selection is not source evidence |
| Competing interpretations | Schoenberg/Hilbert criteria, compact Gromov-Hausdorff realization, h-principle/Nash-Kuiper, and Riemannian isometric embedding | Explicitly not merged into the root |
| Statement layer | Domains, ordered binders, hypotheses, conclusion, and edge cases | Unfrozen until source identity is resolved; statement phase must not infer these from the title |
| Lean surface | `Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_132.lean` and referenced mathlib APIs | Discovery input only; all historical proof and audit credit is revoked by rev-5.6 |
| Foundations | Lean 4 kernel with versioned mathlib and an accepted classical/choice/quotient policy | Toolchain, dependency, and trust fingerprints remain open |

The dossier intentionally contains no Lean declaration. Introducing one before identifying the
human claim would risk broadening or substituting the theorem. The dependent statement phase must
first resolve the source blocker and only then serialize and mutation-test an exact target.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H5, M4, R3]`. The first failed gate is exact
human-source identification, followed by the Lean statement gate. The theorem is not complete.
Validation results and their precise evidentiary boundary are recorded in `validation.md`.
