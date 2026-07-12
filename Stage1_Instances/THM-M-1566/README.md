# THM-M-1566 intake dossier

This planned rev-5.6 instance covers the Gubinelli-Imkeller-Perkowski
paracontrolled-distribution theory. The repository label, "regularity of
parabolic SPDEs", is not a unique theorem. The statement phase selects
Corollary 5.9 of *Paracontrolled distributions and singular PDEs*: local
existence, uniqueness, and convergence of renormalized approximations for the
generalized parabolic Anderson model on the two-dimensional torus.

The exact Lean proposition is `Stage1Instances.THMM1566.GIPCorollary59Target`
in `Statement.lean`. It uses a typed abstract analytic API because the pinned
libraries lack paracontrolled distributions and the renormalized PAM solution
notion. The API contains no assumed conclusion. This is an elaborated statement
boundary, not proof closure.

## Scope map

| Node | Scope | Intake state |
|---|---|---|
| `GIP-ROOT` | Exact well-posedness and approximation-convergence claim | statement frozen: Corollary 5.9 |
| `GIP-SPACE` | Parabolic Holder-Besov spaces and norms | open |
| `GIP-NOISE` | Spatial white noise and enhanced renormalized data | open |
| `GIP-CALC` | Paraproduct, resonant product, and commutator estimates | open |
| `GIP-FIX` | Local fixed point, existence, and uniqueness | open |
| `GIP-REN` | Mollification and counterterms from Lemma 5.8 | open |
| `GIP-CONV` | Positive stopping time and convergence in probability | open |

The historical module `AwesomeTheorems.Stage1.S1_M_182` is discovery input
only. Its `StatementShape` packages assumed propositions and is not the
primary-source theorem. No legacy declaration, source label, or build result
is accepted as machine closure.

Authoritative structured intake: `intake.json`. Source mapping:
`source_statement_crosswalk.md`. Validation record: `validation.md`.

Current boundary: `planned`, root vector `H1 / M4 / R3`, theorem completion
`false`. The statement node is self-tested pending master acceptance; every
later node remains open.
