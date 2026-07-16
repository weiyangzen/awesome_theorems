# THM-M-0449 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the repository label
`海涅曼-洛基塔斯基定理`. The only repo-local source wording is "local Langlands
correspondence for p-adic groups". That wording does not identify one exact theorem.

## Scope map

| Surface | Intake scope | Boundary |
|---|---|---|
| Human identity | label, attributed authors Guy Henniart / Marie-France Vigneras, year 2000 | no paper, theorem number, edition, pages, or errata record |
| Mathematical root | some local Langlands correspondence for a p-adic group | group family, characteristics, coefficients, parameter equivalence, normalization, and compatibilities are unspecified |
| Automorphic side | smooth irreducible/admissible representations are expected subject matter | exact category and equivalence relation are not frozen |
| Galois side | Weil, Weil-Deligne, or L-parameters are possible interpretations | parameter object and enhancement are not frozen |
| Legacy Lean surface | `AwesomeTheorems.Stage1.S1_M_063.FrozenTheoremVariant` | an abstract `Nonempty` package; explicitly not a terminal local Langlands proof and not accepted as the source statement |
| Foundation and TCB | Lean 4 plus pinned mathlib is intended | profile, toolchain pin, imports, and dependency fingerprint remain open |

The scope deliberately preserves ambiguity rather than selecting `GL_n`, a general reductive
group, a mod-l correspondence, or an abstract package. Resolving the primary source is a hard
prerequisite to the dependent statement phase.

## Current verdict

Lifecycle is `planned`; provisional root vector is `[H4, M4, R4]`. The first failed gate is exact
source identification. The metadata label `已验证` is untrusted, and the historical Lean file is
discovery input only. No theorem completion, proof closure, or accepted receipt is claimed.

The statement phase now owns a declaration-free `Statement.lean`, a null-target `statement.json`,
a structured blocked receipt, and a semantic validator. They self-test the negative boundary and
propose only unfinished `[_]` worker evidence. The validator reports `phase_accepted=false`; no
canonical statement, statement acceptance, audit completion, or theorem completion is claimed.

## Validation

The exact commands and results establishing manifest membership, repository consistency, JSON
syntax, and dossier-local hygiene are recorded in `validation.md`. No Lean target is introduced by
this intake phase.
