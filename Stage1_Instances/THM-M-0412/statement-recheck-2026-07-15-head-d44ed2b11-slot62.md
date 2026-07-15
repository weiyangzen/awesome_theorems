# THM-M-0412 statement recheck at `d44ed2b11`: blocked

Item: `S56-M-0412-STATEMENT`

Base revision: `d44ed2b11fb201a761afad9b133caa8bc97fd710` (tree
`9602084a1c32fa6685f1c60eff540528226decff`). Rechecked on 2026-07-15
(`Asia/Shanghai`) in the Stage1 rev-5.6 slot62 worker clone.

## Decision

The requested deliverable, "Elaborate the exact Lean 4 target with the minimal pinned imports," is
blocked. Its prerequisite `S56-M-0412-INTAKE` is unfinished provisional state `[_]`, not
master-accepted state `[x]`. Independently, the first statement-content gate fails at
`exact_source_statement_identity`.

The authoritative repository record supplies only the Chinese label `皮尔斯猜想` ("Pierce
conjecture"), attribution to Trygve Nagell, year 1948, and the gloss `某些三次曲线的整数点`
("integer points on certain cubic curves"). It supplies no original-language title, immutable
primary publication, theorem/page locator, equation or curve family, domains, parameters, ordered
binders, hypotheses, conclusion, proof boundary, corrections, or degenerate cases. The intake
dossier deliberately records `unresolved_source_identity` and a provisional `H5 / M4 / R4` vector.

Since the preceding recheck base `cb7809d0317a837cb067c0d3fe417c84f167b350`, the target manifest,
catalog, Stage0 entry, execution skill, intake dossier, legacy Lean module, toolchain, dependency
lock, and statement probe are unchanged. Blueprint and execution-DAG changes concern unrelated
targets. The only new THM-M-0412 files are the integrated preceding recheck artifacts, which
preserve rather than resolve this blocker.

The legacy `S1_M_021.lean` module cannot fill the gap. Its `NagellLutzBranchData` stores the
equation, hypotheses, and conclusions as abstract propositions, and `StatementShape` assumes source
and audit predicates instead of stating a concrete arithmetic claim. Its prose proposes a
Nagell-Lutz identity correction, but the rev-5.6 intake has no source-backed approval of that
replacement. Selecting Nagell-Lutz, a Ramanujan-Nagell equation, Markov's equation, Siegel
finiteness, an arbitrary cubic, or one selected Nagell paper would substitute proposition-changing
mathematics.

Consequently the canonical human statement, Lean target, minimal imports, elaborated-expression
hash, target environment fingerprint, checked transports, and all four required mutation classes
remain undefined. Lifecycle stays `planned`, item state stays `[ ]`, and no statement receipt,
worker `[_]`, debt change, proof, audit completion, theorem completion, or master acceptance is
claimed.

## Pinned Lean Surface Replay

`StatementProbe.lean` remains deliberately limited to the adjacent interface. From
`Formalizations/Lean`, this command succeeded against the existing pinned artifacts:

```text
LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean
```

It elaborated six `WeierstrassCurve` APIs. Stdout was 618 bytes with SHA-256
`52574dd9f0f5feda16279f9af5344d9218c0c6089ce238abe2bcc0c9f2628cbb`; stderr was empty with
SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Its only direct
import, `Mathlib.AlgebraicGeometry.EllipticCurve.Affine.Point`, cannot be certified minimal for an
undefined target. The replay receives no canonical-target, transport, anchor-audit, or proof
credit.

The environment was Lean `4.29.0` at commit
`98dc76e3c0a9b856c9b98726b713fb04fab16740`, Lake `5.0.0-src+98dc76e`, and mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` (tree
`bdc39a3123201dae413a9d9be56ec242c19e5c2b`). The mathlib package worktree was clean. The
automation-provided untracked `.lake` symlink was reused read-only; no update, build, clone, fetch,
or other dependency mutation ran.

## Commands And Results

| Command or check | Exit | Exact result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups, 41 legacy rows, 300 legacy slots, 1546 uniform-L0 Lean 4 targets, and execution-skill presence passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all `L0/rework_required` |
| `python3 scripts/stage1_target.py show THM-M-0412` | 0 | rank 21; planned; legacy artifacts unaccepted; theorem incomplete |
| `git status --short --untracked-files=all`; `git rev-parse HEAD 'HEAD^{tree}'` (pre-edit) | 0 | only the automation-provided `Formalizations/Lean/.lake` symlink was untracked; base identities matched this record |
| scoped authoritative-input diff from `cb7809d0317a837cb067c0d3fe417c84f167b350` to HEAD | 0 | no target manifest, catalog, Stage0, skill, intake, legacy Lean, toolchain, dependency-lock, or statement-probe change; no exact proposition was added |
| repository source-boundary inspection | 0 | matches remained sparse metadata, blocker records, or the rejected legacy correction; no exact proposition was found |
| from `Formalizations/Lean`: `LC_ALL=C TZ=UTC lake env lean ../../Stage1_Instances/THM-M-0412/StatementProbe.lean` | 0 | six adjacent APIs elaborated; stream sizes and hashes recorded above; no canonical target or proof body |
| from `Formalizations/Lean`: `lake env lean --version`; `lake --version` | 0 | pinned Lean and Lake identities recorded above |
| mathlib package status and `git rev-parse HEAD 'HEAD^{tree}'` | 0 | package clean at the recorded immutable revision and tree |

The companion JSON records these checks and the final JSON parse, target-scoped invariant,
prohibited-construct, whitespace, change-scope, and self-test-absence validations. The recheck format
has no published strict repository schema or independent validator, so these checks do not create a
node-specific completion receipt.

## Retry Condition And Status Boundary

Retry only after the intake is master accepted with a source-resolved claim and accountable
reviewers preserve and hash an immutable primary or approved authoritative source, reconcile the
label, attribution, and date, and independently approve one exact claim with every incorporated
definition, binder, hypothesis, conclusion, correction, proof boundary, and degenerate case. A
later statement worker can then encode exactly that claim, minimize its pinned imports, serialize
and hash the elaborated expression and environment, compile every credited transport, and run the
removed-hypothesis, changed-domain, changed-binder-scope, and boundary-case mutations.

This is a current-HEAD target-scoped blocker handoff, not a completed statement node. Because the
positive deliverable did not pass, `.stage1-worker-selftest.json` is intentionally absent.
