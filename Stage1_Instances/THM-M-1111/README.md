# THM-M-1111 rev-5.6 intake

This directory is the `planned` intake for the Tao-Vu four moment theorem. It fixes the target to
the eigenvalue-statistics comparison theorem for two Wigner Hermitian ensembles with four-moment
off-diagonal matching and two-moment diagonal matching. It does not silently replace that result
with a generic moment lemma or with an unquantified universality slogan.

The primary paper family is identified, but source versions contain multiple four-moment variants.
The statement phase must select one immutable version and preserve its precise tail condition, test
function derivative bounds, eigenvalue normalization, index range, and error quantifiers. The
provisional root vector is `[H1, M4, R4]`. No Lean statement or proof completion is claimed.

The scope map and source crosswalk state the frozen boundaries; the open task DAG records all later
phases. Intake checks and their exact results are recorded in `validation.md`.
