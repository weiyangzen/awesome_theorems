# THM-M-1058 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the large deviation principle. The source label
is broad: an LDP is normally a property of a family of probability measures at a specified speed
and rate function, not an unconditional theorem about every family. This intake therefore freezes
the standard open/closed-set property as the candidate boundary and does not claim that it holds.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Root property | closed-set upper bound and open-set lower bound for a sequence of probability measures | Candidate only; exact elaboration is owned by the statement phase |
| State space | topological measurable space `E` | Compatibility and regularity assumptions require source and Lean audit |
| Scaling | positive speed tending to infinity | Sequence indexing is provisional; nets and small-parameter conventions are excluded |
| Rate function | nonnegative lower-semicontinuous extended-real function | Goodness (compact sublevel sets) is not silently assumed |
| Event rate | infimum of the rate function over the event | Empty-set and extended-arithmetic conventions require mutation probes |
| Variants | weak LDP, full LDP, good LDP, Laplace principle | Separate candidates; no equivalence credit at intake |
| Machine surface | legacy `S1_M_250.lean` definitions | Discovery input only; no inherited proof or statement credit |

The structured claim, binders, and exclusions are in `intake.json`; the source relationship is in
`source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M3, R3]`. The first failed theorem gate is
the exact statement gate: no accepted source pinpoint, normalized Lean expression hash, environment
fingerprint, checked transports, or mutation results exist. The theorem is not complete.

## Validation

The commands in `validation.md` establish manifest membership, standard consistency, JSON syntax,
and dossier-local integrity only. Master acceptance and all dependent phases remain outstanding.
