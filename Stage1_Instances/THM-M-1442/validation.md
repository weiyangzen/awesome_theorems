# Intake validation

Base revision: `b4e1220a37cc10a96534cfd411e3b29523d7fd81` (tree
`a67dd08a83c396119f4762e0ff109cd0df43ee60`).

This validation covers target membership, dossier structure, source and environment provenance,
JSON integrity, and a narrow pinned Lean API probe. Because the repository record supplies no
stable proposition, no canonical target, expression hash, mutation result, source acceptance, or
proof is claimed. The automation-provided canonical `.lake` symlink and artifacts were used
read-only; no dependency update, build, clone, fetch, or `.lake` mutation was performed. The
symlink is a pre-existing, out-of-scope untracked automation input, so this is nonrelease worker
evidence.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-1442` | 0 | rank 1121, planned, no legacy slot, legacy artifacts unaccepted, theorem incomplete |
| initial `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` | 0 | only the automation-provided `.lake` symlink was untracked; base revision and tree recorded above |
| `git blame -L 10532,10537 -- Docs/researches/math_theorems.md` | 0 | all six uncited catalog lines originate at `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f` |
| `sha256sum` over authority, source, toolchain, lock, and candidate-module inputs | 0 | fingerprints recorded in `instance.json` and `intake-receipt.json` |
| `(cd Formalizations/Lean && lake env lean --version)` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, x86_64 Linux |
| `(cd Formalizations/Lean && lake --version)` | 0 | Lake `5.0.0-src+98dc76e`; no update or build was run |
| `git -C Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD 'HEAD^{tree}'` | 0 | mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95`, tree `bdc39a3123201dae413a9d9be56ec242c19e5c2b` |
| `(cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1442/IntakeProbe.lean)` | 0 | five intermediate-value, geometric-decay, and unrelated lexical-hit interfaces elaborated; no target theorem |
| bounded repository and pinned-mathlib bisection/root searches | 0 | found adjacent IVT APIs and the unrelated `norm_num` metaprogram, but no source-identical repo theorem; discovery only |

The final JSON checks, Python syntax check, `check_intake.py --worker-packet`, prohibited-construct
scan, and scoped whitespace checks exited as recorded in `intake-receipt.json`. The Git diff check
cannot by itself cover untracked new files, so the scoped checker also enforces final newlines, LF
line endings, no NUL bytes, no trailing whitespace, the exact artifact inventory, and recorded
artifact hashes.

Known downstream failures remain intentionally open: exact source selection and independent
review; function, domain, bracket, assumptions, recurrence, branch convention, conclusion, rate,
error, stopping, arithmetic, and boundary decisions; canonical elaboration and all four mutation
classes; discovery and obligation freezes; anchor and proof-body audits; proof and composition;
readable reconstruction; trust closure; hermetic replay; deterministic evidence; independent
verification; release; and master acceptance. They prevent theorem completion but do not invalidate
a truthful `planned` intake.
