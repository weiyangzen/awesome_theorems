# THM-M-1565 statement-phase blocker

- Item: `S56-M-1565-STATEMENT`
- Base revision: `06c00fe91e7aaf5b2f85417e17db5492134dae54`
- Attempt date: 2026-07-12 (Asia/Shanghai)
- Verdict: blocked; no statement receipt or theorem-completion claim

## First failed gate

The exact-statement gate in section 5.1 of `Docs/Stage1_Blueprint_rev-5.6.md` cannot be
truthfully entered from the accepted intake. The repository source says only "Hairer regularity
structures" and "theory of singular SPDEs". This names a framework, not one proposition. The
intake consequently leaves the canonical source root open among Hairer's Theorems 3.10, 8.24,
10.7, or a named SPDE application. Those results have different domains, hypotheses, and
conclusions. Selecting one without an accepted scope decision would substitute a narrower theorem
for the metadata target.

The leading candidate, Theorem 3.10 in Martin Hairer's *A theory of regularity structures*, also
cannot be encoded exactly using a pre-existing pinned Lean API. Its statement quantifies over a
regularity structure and model and uses modelled-distribution spaces, scaled distribution spaces,
the reconstruction operator, compact-set seminorms, equations (3.3)--(3.5), uniqueness for
positive gamma, and two-model stability. A scoped search of pinned mathlib found no implementation
of regularity structures, modelled distributions, or this reconstruction theorem. Introducing
opaque predicates or a structure field asserting reconstruction would merely assume the target;
reducing the result to existence or uniqueness alone would weaken it. Both are prohibited.

Therefore there is no exact Lean declaration to elaborate, no honest minimal-import claim, and no
expression or environment fingerprint. Removed-hypothesis, changed-domain, changed-binder-scope,
and boundary mutation tests cannot be defined before the canonical binders and premises exist.
The machine boundary remains `M4`, and the statement phase is not self-tested.

## Evidence inspected

The author PDF revision dated 2015-06-08 was available as `/tmp/structure.pdf`, SHA-256
`95f8c90a73b2a33bd480a8381ffdb8749724cca939e46787ae40478f052c33da`. Its Theorem 3.10,
pp. 31--32, was inspected directly. It requires the complete conclusion described above, including
both stability estimates; the introductory loose reconstruction statement is not an exact
substitute.

The existing toolchain is Lean 4.29.0 at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, with pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`. The worker's `.lake` symlink was used read-only. No
`lake update`, `lake build`, clone, fetch, or dependency mutation was performed.

## Commands and exact results

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | `check_stage1_standard: ok (15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, execution skill present)` |
| `python3 scripts/stage1_target.py check` | 0 | `stage1_target: ok (1546 unique targets, ranks 1..1546, all L0/rework_required)` |
| `python3 scripts/stage1_target.py show THM-M-1565` | 0 | rank 576; `planned`; `L0`; legacy artifacts unaccepted; theorem incomplete |
| `git rev-parse HEAD` | 0 | `06c00fe91e7aaf5b2f85417e17db5492134dae54` |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C /home/sansha-2/external/awesome_theorems/Formalizations/Lean/.lake/packages/mathlib rev-parse HEAD` | 0 | `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `sha256sum Formalizations/Lean/lean-toolchain Formalizations/Lean/lake-manifest.json /tmp/structure.pdf` | 0 | `651c8acc...b1d2`, `321626c8...8b81`, and `95f8c90a...33da` |
| `pdftotext -layout /tmp/structure.pdf /tmp/structure.txt` and a scoped search for `Theorem 3.10` | 0 | exact source statement and equations (3.3)--(3.5) inspected |
| scoped case-insensitive `rg` over pinned mathlib `Mathlib/**/*.lean` for `regularity structure`, `modelled distribution`, `reconstruction theorem`, and `singular spde` | 0 | no matches |

## Unblocking condition

An independent statement owner must first approve one exact source theorem and edition as the
canonical interpretation of the broad repository label. If Theorem 3.10 is selected, the statement
work then needs source-faithful Lean definitions for every incorporated object and bound, followed
by exact elaboration, serialization, checked transports, and all four mutation classes. Until
those prerequisites are met, no `.stage1-worker-selftest.json` is warranted.
