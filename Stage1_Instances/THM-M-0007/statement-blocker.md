# Statement gate blocker

Item: `S56-M-0007-STATEMENT`
Theorem: `THM-M-0007`
Verdict: blocked; no exact canonical Lean target is claimed.
Worker base: `1cc6aa61bb055a5c032297ee457905c849af7608`.

## First failed gate

The intake identifies Weibel, *An Introduction to Homological Algebra*, Theorem 5.8.3 only as an
uninspected theorem-family anchor. The owned source crosswalk explicitly leaves the printed
definitions, exact hypotheses, page convention, naturality, and convergence conclusion open. The
repository contains no scan or transcription of the cited pages. Consequently there is not enough
source evidence in this clone to choose, without inventing mathematics, among an objectwise versus
functorial target, weak versus strong convergence, the associated filtration and its boundedness,
or the precise placement of enough-injectives and acyclicity assumptions.

There is also a concrete encoding gap in the pinned dependency. Mathlib provides the typed carrier
`E₂CohomologicalSpectralSequenceNat E`, its pages and differentials, and the required right-derived
functors, but a repository-wide search of pinned `Mathlib/Algebra/Homology` and
`Mathlib/CategoryTheory` finds no abutment, `ConvergesTo`, or `StronglyConvergesTo` interface. The
legacy `GrothendieckSpectralSequenceBoundary` cannot fill that gap: its `spectralSequence` is an
arbitrary `Type`, while naturality and convergence are bare `Prop` fields. Reusing it would violate
the intake's explicit exclusion of opaque proxy fields and would broaden the exact-statement claim.

Therefore ordered binders, exact conclusion, definition-level source crosswalk, expression
fingerprint, checked transports, and meaningful statement mutations cannot truthfully be frozen.
`Statement.lean` checks only the noncontroversial typed substrate and deliberately declares no
canonical theorem, axiom, placeholder, or proxy convergence predicate. Accordingly the positive
statement completion predicate fails at `S02-EXACT-TARGET`; the four required `S03-MUTATIONS`
classes cannot be executed without manufacturing a canonical expression.

## Environment fingerprint

- Repository base revision: `1cc6aa61bb055a5c032297ee457905c849af7608`.
- Validation date: 2026-07-17.
- Lean toolchain: `leanprover/lean4:v4.29.0`; Lean `4.29.0`, commit
  `98dc76e3c0a9b856c9b98726b713fb04fab16740`.
- mathlib Lake pin: `8a178386ffc0f5fef0b77738bb5449d50efeea95`.

## Validation evidence

Lean commands ran from `Formalizations/Lean` against the existing pinned `.lake` symlink. No
update, build, fetch, or clone command was used.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean --trust=0 ../../Stage1_Instances/THM-M-0007/Statement.lean` | 0 | all four `#check` commands printed typed declarations; this is substrate evidence only |
| `lake env lean AwesomeTheorems/Stage1/S1_M_094.lean` | 0 | legacy discovery artifact elaborated; not exact-statement credit |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum lean-toolchain lake-manifest.json lakefile.lean` | 0 | respectively `651c8a...81d2`, `321626...2d81`, and `43259b...4b4dcda` |
| `rg -l "StronglyConverges\|stronglyConverges\|ConvergesTo\|convergesTo\|abutment\|Abutment" Formalizations/Lean/.lake/packages/mathlib/Mathlib/Algebra/Homology Formalizations/Lean/.lake/packages/mathlib/Mathlib/CategoryTheory -g '*.lean' \| wc -l` | 0 | `0` matching files |
| `/usr/bin/python3 -I -B Stage1_Instances/THM-M-0007/check_statement.py` | 0 | emits exactly one typed negative semantic JSON object with `phase_accepted=false`; scheduler replay still requires these validator bytes at a later worker base |

The exact final command list and results are content-bound in `statement-receipt.json` and the root
worker self-test handoff. Global v2 inventory validators are expected to report the new target-owned
evidence inventory as stale until the master lane integrates these files and regenerates its
read-only projection; this worker does not edit that authority.

## Retry condition

The authoritative lane must provide and approve a page-level transcription of the selected primary
source, including its definitions of acyclicity and convergence, and select or implement a typed
Lean convergence/abutment interface. The statement phase can then encode the exact claim, verify
its complete expansion, and run source-directed hypothesis, domain, binder-scope, and boundary
mutations.

Until then the statement gate remains at `M4`; statement acceptance and theorem completion are
false. The negative packet may be worker-self-tested and handed off as `[_]`, but raw `blocked`
cannot close this positive phase and cannot be inferred as `phase_accepted` from exit code zero.
