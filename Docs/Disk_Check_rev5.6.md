# Stage1 rev-5.6 Disk and Execution-Cron Risk Assessment

> Assessment date: `2026-07-11 Asia/Shanghai`
> Repository: `awesome_theorems`
> Standard assessed: `Docs/Stage1_Blueprint_rev-5.6.md`
> Execution framework intended by the user: b3ehive `execution-cron-builder`
> Reference instance: `THM-M-0387`
> Decision: do not start an unbounded or multi-Lean-worker execution cron on the current disk

## 1. Executive Decision

`Docs/Stage1_Blueprint_rev-5.6.md` is a strong theorem-assurance specification, but it is not yet a
complete b3ehive execution cron. It does not currently provide the single authoritative 1546-target
checkbox DAG, daily todo generator, isolated automation-clone lifecycle, claim ledger, integration
queue, scheduler guard, installer, or cleanup program required by `execution-cron-builder`.

The current machine is also too close to its storage limit for unrestricted execution:

```text
Data volume capacity: 926 GiB
Data volume used:     860 GiB
Data volume available: 31 GiB (`df` rounded; APFS inspection observed about 32.9 GB)
Data volume use:       97%
Repository footprint:  12 GB
```

One incremental M0387-style validation in the existing checkout is plausible. A fresh isolated Lean
workspace, two independent runners, or concurrent workers that each materialize mathlib can exhaust
the remaining space. A full 1546-target cron must therefore remain blocked until disk budgets,
dependency sharing, workspace cleanup, and external release validation are implemented.

## 2. Execution-Skill Clarification

The intended executable-skill standard is the locally installed b3ehive
`execution-cron-builder`, not a standalone repository `SKILL.md`. A repository skill may help form
worker prompts, but it does not replace the b3ehive scheduler contract.

The b3ehive execution model requires at least:

1. exactly one authoritative blueprint requirement source;
2. an authoritative `[ ]`, `[_]`, `[x]` checklist in that blueprint;
3. a dependency DAG with stable IDs, owned paths, gates, and cycle rejection;
4. daily `todos_YYYYMMDD.md` projections;
5. isolated `.cron/automation_repo*` worker workspaces;
6. separate worker-claim and master-integration cursors;
7. `VALIDATE_ONLY=1` before enabling cron;
8. sync-first, checkpoint, validation, push, and cleanup gates;
9. bounded logs, workspace TTL, cron-root limits, and disk checks before worker spawn;
10. automatic cron removal only after both `[ ]` and `[_]` counts reach zero and validation passes.

Current rev-5.6 artifacts split normative requirements, target-set data, generated lists, and legacy
slots across several files. That separation is useful for assurance, but b3ehive still needs one
unambiguous execution-state authority. Before cron installation, the 1546-target execution DAG must
be rooted in `Docs/Stage1_Blueprint_rev-5.6.md`, while JSON and Markdown target lists remain generated
or validated projections rather than competing checkbox-state authorities.

## 3. Current Storage Measurements

Measurements taken from the repository filesystem on `2026-07-11`:

| Surface | Size | Interpretation |
|---|---:|---|
| Entire repository checkout | `12 GB` | dominated by ignored Lean dependencies |
| `Formalizations/Lean/.lake` | `8.4 GB` | Lake packages plus build state |
| `.lake/packages/mathlib` | `7.9 GB` | largest active dependency checkout |
| `Formalizations/Lean/.vendor` | `3.9 GB` | second mathlib source copy |
| `.vendor/mathlib4` | `3.9 GB` | vendored mathlib tree |
| `.lake/build` | `19 MB` | current repo-local compiled output is comparatively small |
| `THM-M-0387` dossier | `1.1 MB` | documents and structured evidence are not the main risk |
| `Docs` | `9.4 MB` | blueprint and target manifests are not the main risk |
| Available Data-volume space | about `31 GiB` | only about 2.9 GB above b3ehive's default 30 GB spawn floor |

Both `Formalizations/Lean/.lake/` and `Formalizations/Lean/.vendor/` are gitignored. A normal Git
clone does not copy them, but an unsafe `cp`, `rsync`, cache bootstrap, `lake update`, or worker-local
dependency setup can recreate them. Workspace preparation must explicitly prevent accidental
duplication.

## 4. M0387 Reference Behavior

`THM-M-0387/run_local_validation.sh` currently performs seven stages:

1. build statement/reduction and branch modules;
2. build the Stage1 integration wrapper;
3. compile the theorem-folder sample;
4. build the shared aggregator;
5. run the full local Lake build;
6. compile the Python dossier validator;
7. run dossier lint plus exact Lean probes.

The existing checkout reuses its `8.4 GB` Lake dependency closure, and its current `.lake/build`
directory is only `19 MB`. This explains why an incremental M0387 validation can succeed without a
large immediate increase. It does not establish that a cold isolated validation is cheap: a new
workspace that materializes the same dependency closure may require roughly `8 GB`, and copying the
vendor tree can bring the workspace footprint toward `12 GB` before logs, archives, or build peaks.

## 5. Risk by Execution Mode

The following ranges are engineering estimates based on the current M0387 footprint. They are
capacity-planning bounds, not measured guarantees for every theorem.

| Execution mode | Plausible additional peak | Disk-full risk now |
|---|---:|---|
| Documentation or manifest-only work | below `100 MB` | low |
| One target, incremental checks in current checkout | about `0.1-1 GB` | low to medium |
| One isolated clone with a shared read-only dependency store | about `0.1-2 GB` | medium |
| One fully independent Lean dependency workspace | about `8-12 GB` | high |
| Two fully independent Lean runners | about `16-24 GB` | very high |
| Two runners plus offline archive and cold-build transients | about `21-35+ GB` | critical |
| Multiple workers each running `lake update` independently | approximately `N x 8-12 GB` | near-certain exhaustion |
| Per-theorem retained dependency/build closure for all 1546 targets | terabyte scale | impossible locally |

Qualitative probability estimates under the current 31-33 GB free-space condition:

| Scenario | Estimated probability of filling or crossing a dangerous disk threshold |
|---|---:|
| Single incremental M0387-style audit/build | `20-35%` |
| One complete isolated empty-cache Lean runner | `60-75%` |
| Two independent runners executing concurrently | `85-95%` |
| Ordinary multi-worker execution across the full target list | approximately `100%` over time |

These probabilities reflect uncertainty in temporary files, dependency materialization, APFS
behavior, and theorem-specific build growth. They are not formal statistical measurements. The
capacity argument is nevertheless decisive: two 8-12 GB workspaces plus an archive can consume most
or all of the space currently available.

## 6. Why rev-5.6 Amplifies Peak Usage

The release protocol in rev-5.6 correctly requires stronger evidence than an incremental build:

- an immutable new checkout;
- empty user/package/build caches;
- a cold build with outbound network denied;
- a restorable dependency/source archive and SBOM/license material;
- two independently provisioned runners;
- no shared writable dependency or build cache;
- deterministic evidence bundles and independent verification.

On one constrained machine, a literal implementation creates several simultaneous storage surfaces:

```text
main development dependency closure
+ runner A dependency/build closure
+ runner B dependency/build closure
+ offline source/dependency archive
+ receipts, logs, temporary files, and validation outputs
```

The current free space does not safely accommodate that release topology. Ordinary development may
reuse a read-only content-addressed dependency store, but such reuse must not be misrepresented as
independent release verification. Release runners should be placed on separate CI runners, another
host, or an external volume with an explicit capacity budget.

## 7. b3ehive Guard Requirements

The installed b3ehive `execution-cron-builder` defaults include:

```text
MIN_FREE_GB=30
DANGER_FREE_GB=15
MAX_LOG_MB=20
MAX_KEEPALIVE_MB=5
LOG_RETENTION_DAYS=3
WORKSPACE_TTL_HOURS=48
MAX_CRON_ROOT_GB=30
```

At approximately 31-33 GB free, this machine begins only 1-3 GB above the default worker-spawn
floor. One complete Lean dependency workspace would push it below `MIN_FREE_GB`; an archive or
second workspace could push it toward or below `DANGER_FREE_GB`.

For this repository, the guard must:

1. inspect the filesystem that actually contains the repository, preferably
   `/System/Volumes/Data`, rather than trusting a misleading volume presentation;
2. check available bytes before scheduler work, before every worker spawn, and immediately before
   any `lake update`, cold build, archive creation, or independent-runner provisioning;
3. reserve predicted task peak space and require the post-task estimate to remain above the danger
   floor;
4. block with `blocked_disk_space` or `blocked_disk_budget`, never continue optimistically;
5. bound and tail worker, scheduler, and keepalive logs;
6. delete only stale, non-live workspaces and record every janitor decision;
7. prevent lock, tmux, PID, or claim references from pointing to a workspace before deleting it;
8. exclude `.lake`, `.vendor`, `.git`, build output, logs, and archives from naive workspace copies;
9. deduplicate immutable dependency archives by content/revision rather than by theorem;
10. remove per-target build caches after accepted evidence has been reduced to required receipts.

## 8. Recommended Operating Limits

Until more space is available, the safe posture is stricter than the generic b3ehive defaults:

```text
MIN_FREE_GB=35
DANGER_FREE_GB=20
MAX_CRON_ROOT_GB=8
WORKSPACE_TTL_HOURS=12
MAX_LOG_MB=10
MAX_KEEPALIVE_MB=2
LOG_RETENTION_DAYS=1
LEAN_WORKER_CONCURRENCY=1
FULL_COLD_BUILD_CONCURRENCY=1
RELEASE_RUNNER_CONCURRENCY=0 locally
```

Because the current free space is below the proposed `MIN_FREE_GB=35`, validation-only mode should
report a disk block instead of installing or starting the cron. This is the desired fail-closed
result.

Recommended capacity milestones:

| Available space | Permitted posture |
|---:|---|
| below `35 GB` | validation-only; no new Lean worker |
| `35-60 GB` | one bounded incremental worker; no full local release |
| `60-100 GB` | one isolated development worker with aggressive cleanup |
| above `100 GB` | safer local cold runs, still avoid duplicated multi-runner archives |
| `120 GB+` or external runners | practical strict dual-runner release work |

## 9. Required Remediation Before Cron Installation

1. Use b3ehive `execution-cron-builder`, not the repository helper skill, to construct the cron.
2. Make `Docs/Stage1_Blueprint_rev-5.6.md` the single authoritative execution-checklist source.
3. Bootstrap the 1546-target DAG with `[ ]`, `[_]`, `[x]`, stable IDs, dependencies, owned paths,
   validation gates, and explicit parent/child closure rules.
4. Keep `Docs/Stage1_Targets_rev-5.6.json` and generated lists as projections or membership inputs,
   not alternative execution cursors.
5. Implement the disk guard and run `VALIDATE_ONLY=1`; require it to block at the current capacity.
6. Free at least `60 GB` before isolated development execution and preferably `100 GB` before local
   cold-build work.
7. Place strict dual-runner release verification on external CI, a second machine, or a sufficiently
   large external volume.
8. Use one shared read-only immutable dependency store for ordinary development workers, with
   separate per-worker build directories and no claim of release independence.
9. Never preserve a complete mathlib checkout or build cache per theorem.
10. Start with one Lean worker and increase concurrency only from measured peak-space receipts.

## 10. Final Assessment

### Execution readiness

The assurance specification is advanced, but the repository has not yet been transformed into a
b3ehive-compliant execution cron. It should be classified as `cron_not_bootstrapped`, not as an
active executable blueprint.

### Disk readiness

The current machine is at `97%` Data-volume usage with only about `31-33 GB` available. Incremental
single-target work can be attempted carefully, but an unrestricted execution cron, duplicated Lean
dependencies, or local dual-runner release validation has a high to critical disk-exhaustion risk.

### Go/no-go

```text
Documentation and structural validation: GO
One incremental Lean validation with live disk checks: CONDITIONAL GO
One fresh independent dependency workspace: HIGH-RISK / normally NO-GO
Two local independent runners: NO-GO
Unbounded 1546-target execution cron: NO-GO
b3ehive VALIDATE_ONLY after guard construction: GO, expected to block on disk threshold
```

The cron must not be installed or enabled until its validation-only guard proves bounded workspace,
log, dependency, and cleanup behavior and the machine has sufficient free capacity for the selected
execution mode.
