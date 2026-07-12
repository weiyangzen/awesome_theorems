# Intake validation

Base revision: `cbe531e6fdc68190477a9c7e8f635fe5a68a4bcd` (tree
`0b4a5720f51c89484fdc5f6b6f07dc01ee1e95c8`).

Validation is limited to manifest membership, repository-standard consistency, dossier structure,
JSON syntax, planned-state invariants, pinned environment identity, a bounded pinned-mathlib name
search, generic API elaboration, placeholder hygiene, and whitespace. The catalog record names an
axiom/definition but gives no truth-valued proposition, so elaborating a selected Axiom A theorem
would be substitution rather than validation. `IntakeProbe.lean` therefore states no theorem and
checks only prospective generic interfaces.

The automation-provided `Formalizations/Lean/.lake` symlink was present before this work and was
used read-only. No `lake update`, `lake build`, dependency clone/fetch, or `.lake` mutation was run.
Because the shared symlink is an out-of-scope untracked automation input and this is not a clean
hermetic replay, these results are provisional nonrelease worker evidence.

| Command (repository root unless noted) | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1413` | 0 | rank 912; planned; L0/rework_required; legacy artifacts unaccepted; theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json` | 0 | `651c8acc...b1d2` and `321626c8...2d81`, respectively |
| temporary AMS PDF download with a browser user agent, followed by `sha256sum` and page-scoped `pdftotext` | 0 | 7,390,130-byte PDF hashed to `759e0601...9551`; item (6.1) on printed page 777 and its dependent-definition locators were inspected; temporary file not committed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1413/IntakeProbe.lean)` | 0 | six generic diffeomorphism, tangent-map, omega-limit, periodic-point, and density APIs elaborated; no target theorem stated |
| bounded search for Axiom A, nonwandering, and hyperbolicity names in pinned dynamics/manifold modules | 1 (expected no-match) | no obvious framework found; intake-only name inventory, not a full anchor audit |
| `python3 Stage1_Instances/THM-M-1413/check_intake.py` | 0 | scoped identity, lifecycle, manifest/DAG, open-task, null-target, receipt-boundary, artifact-hash, and text-hygiene invariants pass |
| prohibited Lean construct scan on the owned path | 1 (expected no-match) | no `sorry`, `admit`, `sorryAx`, `axiom`, or `opaque` proof construct; API probe contains no theorem |
| scoped Git and per-file whitespace checks | 0 | owned untracked files have final LF newlines and no trailing whitespace |

Known downstream failures deliberately remain open: an approved source-backed redirection from the
definition/topic label to a stable proposition; independent acceptance of the source, standing
conventions, dependent-definition mapping, and errata audit; canonical Lean elaboration,
expression/environment fingerprints, checked transports, and all mutation classes; discovery and
obligation freezes; anchor audit; proof and composition; hermetic replay; independent verification;
and master acceptance. They prevent audit and theorem completion but do not invalidate a truthful
`planned` intake.
