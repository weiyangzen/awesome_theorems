# Intake validation

Base revision: `cbe531e6fdc68190477a9c7e8f635fe5a68a4bcd`.

This validation covers target membership, dossier structure, JSON integrity, and a narrow pinned
Lean API probe. Because the repository record supplies no proposition, no canonical target,
expression hash, mutation result, primary-source acceptance, Anosov theorem, or proof is claimed.
The automation-provided canonical `.lake` symlink and pinned artifacts were used read-only; no
dependency update, build, clone, fetch, or `.lake` mutation was performed. The symlink is a
scheduler-provided, out-of-scope untracked input, so this packet is nonrelease worker evidence.

| Command | Result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | exit 0; 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | exit 0; 1546 unique targets, ranks 1..1546, all L0/rework_required |
| `python3 scripts/stage1_target.py show THM-M-1412` | exit 0; rank 911, planned, L0/rework_required, legacy artifacts unaccepted, theorem_complete false |
| `(cd Formalizations/Lean && lake env lean --version)` | exit 0; Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | exit 0; mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool` on the three owned JSON artifacts | exit 0; all are valid JSON |
| `python3 Stage1_Instances/THM-M-1412/check_intake.py` | exit 0; planned/null-target/empty-acceptance/open-DAG/false-completion and owned-artifact invariants passed |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1412/IntakeProbe.lean)` | exit 0; eight generic manifold diffeomorphism, tangent-space, and derivative APIs elaborated |
| bounded pinned-mathlib target-name search | exit 1 as expected for no matches; intake-only negative name result, not a full anchor audit |
| prohibited Lean construct scan on the owned path | exit 1 as expected for no matches; no `sorry`, `admit`, `sorryAx`, `axiom`, or `opaque` declaration |
| scoped whitespace checks | exit 0; checker inspected every new dossier file and Git reported no tracked diff errors |

Exact final commands and results, including their argument arrays, are also recorded in
`intake-receipt.json`.

These checks validate only a truthful `planned` intake. The known failures intentionally left open
are primary-source selection and independent review; selection of a truth-valued proposition and
all manifold, regularity, splitting, derivative, norm, estimate, conclusion, and boundary
decisions; canonical elaboration and required mutation tests; immutable anchor audit; obligation
and discovery freezes; proof and composition; hermetic replay; independent verification; and
master acceptance. They prevent statement and theorem completion but do not invalidate the
metadata dossier, scope map, source-statement crosswalk, and open task DAG delivered here.
