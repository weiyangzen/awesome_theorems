# THM-M-0412 statement recheck at `43f55bb87`: blocked

Item: `S56-M-0412-STATEMENT`

Base revision: `43f55bb87aa8883be277a6660f49c6f8ba647082` (tree
`8e624c67ebaa9cd00a352276e1fca6d17c18e0b9`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in the Stage1 rev-5.6 slot77 worker clone.

## Decision

The positive deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports," is
still blocked at `exact_source_statement_identity`. The authoritative repository record supplies
only the label `皮尔斯猜想` ("Pierce conjecture"), attribution to Trygve Nagell, year 1948, and the
gloss `某些三次曲线的整数点` ("integer points on certain cubic curves"). It still supplies no
original-language title, immutable primary publication, theorem/page locator, equation or curve
family, domains, parameters, ordered binders, hypotheses, conclusion, correction history, proof
boundary, or degenerate cases. The intake dependency remains provisional (`[_]`) and deliberately
records `unresolved_source_identity`; it has no master-accepted receipt.

HEAD integrates the previous current-snapshot blocker, but it does not resolve the target. Between
the previous evidence base `8f3190fed598f6cb4547035d0d96d460ba5fc5cc` and this base, the target
manifest, catalog, Stage0 entry, execution skill, intake dossier, legacy Lean module, toolchain, and
dependency lock are unchanged. The rev-5.6 blueprint and DAG changes concern unrelated targets;
the only THM-M-0412 additions are the integrated prior recheck artifacts.

Fresh bounded bibliographic discovery also did not establish the catalog identity. The zbMATH Open
API returned 184 Nagell records. The inspected results include several concrete cubic/genus-one
works from 1925 onward and a 1950 article on the number of solutions of certain cubic Diophantine
equations, but no source selecting an exact 1948 Pierce proposition. Its explicit 1948 Nagell source
hit is the unrelated equation `x^2 + 7 = 2^n`. OpenAlex's 65-work Nagell inventory likewise has no
1948 item and Crossref's 1948 author/date response contained only false-positive non-Nagell works.
Search failures and incomplete indexes are preserved: this is bounded negative discovery, not an
absence proof. It is enough only to show that no newly inspected source authorizes a target choice.

The legacy `S1_M_021.lean` correction to Nagell-Lutz remains an unsupported lineage hypothesis. Its
`StatementShape` quantifies over abstract proposition fields and assumes source/audit predicates; it
does not encode a concrete arithmetic claim or prove identity with this catalog item. Choosing
Nagell-Lutz, the Ramanujan-Nagell equation, Markov's equation, Siegel finiteness, an arbitrary cubic,
or any one of Nagell's discovered cubic papers would substitute proposition-changing mathematics.

Accordingly the canonical human statement, Lean expression, minimal imports, elaborated-expression
hash, environment fingerprint, checked transports, and all four required mutation classes remain
undefined. The state stays `[ ]`, lifecycle stays `planned`, and provisional root vector stays
`H5 / M4 / R4`. No proof, audit completion, theorem completion, node receipt, or master acceptance
is claimed.

## Pinned Lean Surface Replay

`StatementProbe.lean` is deliberately only an adjacent-interface probe. From
`Formalizations/Lean`, this command succeeded:

```text
LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean
```

It elaborated six `WeierstrassCurve` APIs with stdout SHA-256
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb` and empty stderr
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This earns no
canonical-target, import-minimality, transport, anchor-audit, or proof credit.

The replay used Lean `4.29.0` at commit `98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake
`5.0.0-src+98dc76e`, and the existing clean mathlib package revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). No dependency mutation, update, build, clone,
or fetch was performed.

## Commands And Results

| Command or bounded check | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups; 1546 uniform-L0 Lean 4 targets; execution skill present |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all; git rev-parse HEAD 'HEAD^{tree}'` | 0 | pre-edit tree contained only the automation-provided untracked `Formalizations/Lean/.lake` symlink; base identities matched this record |
| scoped diff from `8f3190fed598f6cb4547035d0d96d460ba5fc5cc` to HEAD | 0 | authoritative target inputs unchanged; unrelated checklist/DAG states and the prior integrated recheck account for the reviewed delta |
| repo-local exact-topic search | 0 | only sparse catalog projections, blocker records, or the rejected legacy correction; no exact proposition |
| pinned mathlib search for `Pierce`, `Nagell`, and `Lutz` | 0 | only unrelated author/reference matches; no exact target |
| bounded zbMATH, OpenAlex, Crossref, and web discovery | mixed | no exact catalog identity or 1948 cubic proposition established; incomplete and timed-out sources were not treated as exhaustive |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated; hashes recorded above; no canonical target or proof body |
| from `Formalizations/Lean`: `lake env lean --version && lake --version` | 0 | pinned Lean and Lake versions recorded above |
| mathlib package status and revision/tree checks | 0 | package worktree clean at the recorded immutable revision and tree |

Final structured-artifact parsing, target-scoped invariants, prohibited-construct scanning, scoped
whitespace checks, and self-test-absence checks are recorded in the companion JSON after the final
artifact replay.

## Retry Condition And Status Boundary

Retry only after accountable reviewers preserve and hash an immutable primary or approved
authoritative source, reconcile the label/author/date, and independently approve one exact claim
with every incorporated definition, binder, hypothesis, conclusion, correction, proof boundary, and
degenerate case. A fresh worker can then encode that same claim, minimize pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This is a fresh target-scoped blocker handoff, not a completed statement node. Because the positive
statement deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent and no
worker `[_]` state is requested.
