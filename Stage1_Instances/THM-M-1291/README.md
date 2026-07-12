# THM-M-1291 rev-5.6 dossier

This is the `planned` intake dossier for the Brezis-Lieb lemma. It freezes the
intended theorem family and its boundaries. The statement node now freezes and
kernel-elaborates the exact complex-valued target in `Statement.lean`; it does
not claim a proof.

The canonical human claim is the integral splitting result from Brezis and
Lieb's 1983 paper: for an almost-everywhere convergent, uniformly `L^p`-bounded
sequence (`0 < p < infinity`), the `p`-power integral of the sequence splits
asymptotically into the integral of the limit and that of the remainder. See
`intake.json`, `scope-map.md`, and `source-statement-crosswalk.md`.

## Intake verdict

Lifecycle remains `planned`; provisional root vector is `[H1, M3, R3]`. The source
paper is identified to theorem and pages, but a stable copy/hash, verbatim
premise audit, and errata review remain open. The first failed theorem gate is
the anchor-audit gate. The canonical Lean expression is elaborated and
fingerprinted in `statement.json`, pending master acceptance. Historical
metadata saying `已验证` supplies no proof credit.
