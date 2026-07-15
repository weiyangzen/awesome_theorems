# THM-M-0412 statement recheck at `e73a459aa`: blocked

Item: `S56-M-0412-STATEMENT`

Closed rev-5.6 terminal intent: `audit` (mapped from the scheduler's `statement` phase; this run
classifies the source/statement blocker and adds no proof content).

Base revision: `e73a459aa33f8b656019c9c36e3d5dfc84dffc30` (tree
`81105927f8e46d0076dd20433240ecf0fd185cea`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in the Stage1 rev-5.6 slot80 worker clone.

## Decision

The requested deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports," is
first blocked because `S56-M-0412-INTAKE` is only provisional and not master accepted. Independently,
the first content gate fails at `exact_source_statement_identity`. The authoritative record supplies
only the label `皮尔斯猜想` ("Pierce conjecture"), attribution to Trygve Nagell, year 1948, and the
gloss `某些三次曲线的整数点` ("integer points on certain cubic curves"). It supplies no
original-language title, immutable primary publication, theorem/page locator, equation or curve
family, domains, parameters, ordered binders, hypotheses, conclusion, correction history, proof
boundary, or degenerate cases. The intake dependency remains provisional (`[_]`) and deliberately
records `unresolved_source_identity`; it has no master-accepted receipt.

Since the prior recheck base `43f55bb87aa8883be277a6660f49c6f8ba647082`, the target manifest,
catalog, Stage0 entry, execution skill, intake dossier, legacy Lean module, toolchain, and dependency
lock are unchanged. Blueprint and DAG changes are state integrations for unrelated targets. The
only THM-M-0412 additions are the integrated prior recheck artifacts, which preserve the same
blocker and do not supply a theorem identity.

The legacy `S1_M_021.lean` module remains ineligible. Its `NagellLutzBranchData` uses abstract
proposition fields, and its conditional `StatementShape` assumes source and audit predicates rather
than encoding a concrete arithmetic claim. Selecting Nagell-Lutz, the Ramanujan-Nagell equation,
Markov's equation, Siegel finiteness, an arbitrary cubic, or a selected Nagell paper would substitute
proposition-changing mathematics.

Accordingly the canonical human claim, Lean expression, minimal imports, elaborated-expression
hash, target environment fingerprint, checked transports, and the four required mutation classes
remain undefined. The state stays `[ ]`, lifecycle stays `planned`, and the intake's provisional
root-vector projection stays `H5 / M4 / R4`. No statement receipt, proof, audit completion, theorem completion, debt
change, worker `[_]`, or master acceptance is claimed.

## Pinned Lean Surface Replay

`StatementProbe.lean` remains only an adjacent-interface probe. From `Formalizations/Lean`, this
command succeeded against the existing pinned artifacts:

```text
LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean
```

It elaborated six `WeierstrassCurve` APIs with stdout SHA-256
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb` and empty stderr
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This confirms
only that the pinned environment is usable; it receives no canonical-target, import-minimality,
transport, anchor-audit, or proof credit.

The replay used Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and the clean
mathlib package revision `8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The automation-provided `.lake` symlink was
reused read-only. No dependency update, build, clone, fetch, or other `.lake` mutation was run.

## Commands And Results

| Command or check | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy slot `S1-M-021`; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit status contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink; base identities matched this record |
| scoped diff from `43f55bb87aa8883be277a6660f49c6f8ba647082` to HEAD | 0 | authoritative target inputs unchanged; unrelated blueprint/DAG state integrations and the prior integrated recheck account for the reviewed delta |
| repo-local exact-topic and source-boundary inspection | 0 | matches remain sparse metadata, blocker records, or the rejected legacy correction; no exact proposition was found |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated; hashes recorded above; no canonical target, transport, or proof body |
| from `Formalizations/Lean`: `lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib package status and revision/tree checks | 0 | package worktree clean at the recorded immutable revision and tree |
| final preflight replay attempted from `Formalizations/Lean` with repository-root relative Python paths | 2 | working-directory mistake: the two Python paths were absent there; the earlier root runs passed and the commands were then replayed from the repository root |

Final JSON parsing, target-scoped invariant assertions, prohibited-construct scanning, scoped
whitespace checks, and self-test-absence checks are recorded in the companion JSON after replay.
The recheck format has no published strict repository schema or independent validator; these local
checks therefore do not make the artifact a node-specific receipt or accepted evidence.

## Retry Condition And Status Boundary

Retry only after accountable reviewers preserve and hash an immutable primary or approved
authoritative source, reconcile the label, author, and date, and independently approve one exact
claim with every incorporated definition, binder, hypothesis, conclusion, correction, proof
boundary, and degenerate case. A fresh statement worker can then encode that same claim, minimize
its pinned imports, serialize and hash the elaborated expression and environment, compile every
credited transport, and run the removed-hypothesis, changed-domain, changed-binder-scope, and
boundary-case mutations.

This is a current-HEAD target-scoped blocker handoff, not a completed statement node. Because the
positive statement deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent
and no worker `[_]` state is requested.
