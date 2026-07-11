# Source-statement crosswalk

| Claim component | Human-source status | Lean candidate | Intake assessment |
|---|---|---|---|
| `L^p` boundedness with `1 < p < infinity` implies a.s. and `L^p` convergence | The repository gives no bibliographic source; a primary textbook/paper theorem and edition pinpoint must be selected and verified | `FullLpConvergenceStatementShape` | Intended root, but the legacy definition permits `p = 1` and therefore is not yet exact |
| Almost-sure convergence | Classical Doob martingale convergence component; source assumptions/pinpoint open | `Submartingale.ae_tendsto_limitProcess` through the legacy wrapper | Candidate upstream bridge only; rev-5.6 anchor audit is later |
| Limit belongs to `L^p` | Classical boundedness/limit component; source pinpoint open | `Submartingale.memLp_limitProcess` | Candidate upstream bridge only |
| Convergence in `L^p` | Terminal conclusion of the root theorem | No terminal declaration identified by intake; legacy file records formalization debt | Open machine boundary |
| `p = 1` endpoint | Requires uniform integrability rather than mere `L^1` boundedness for norm convergence | `EndpointOneUniformIntegrabilityRegime` and `tendsto_eLpNorm_one_limitProcess` | Separate endpoint, excluded from root |

The source phrase in the generated legacy blueprint is only “an `L^p`-bounded martingale
converges.” It omits the exponent range, scalar codomain, time index, convergence modes, and
the identity/status of the limit. This intake freezes the conventional real-valued,
discrete-time, `1 < p < infinity` claim without pretending that the repository metadata is a
primary source. A later source audit must record an immutable edition, theorem/page, every
assumption, relevant errata, and a node-by-node premise crosswalk before `H0` is possible.

The statement phase must also decide probability measure versus finite measure, elaborate the
canonical target with the exponent regime present in its type, check the existence-versus-selected
limit transport, and mutation-test deletion of martingality, boundedness, and both exponent bounds.
No human-source or machine-closure credit is claimed here.
