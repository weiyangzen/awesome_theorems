# ConjectureBench v5.5 candidate audit

This directory contains the complete strict audit of the 302 ConjectureBench records at commit `357bcb1a1daf93917d42e8206ceaa55645729a09`, with an audit cutoff of 2026-08-10.

The result is **178 pending, 124 rejected, 0 accepted, and 0 strict-conjecture credits**. No release entry was added. Release 5.4 is a protected input and was not modified.

The defensible residual upper bound is 190 records. Earlier bounds of 161, 162, and 172 are withdrawn: a stable source path and declaration name did not establish exact proposition identity when declaration text changed. The 70 prior exclusions comprise 67 byte-identical Lean surface declarations and three later solved-status records. Surface-declaration equality does not assert equality of fully elaborated kernel expressions across dependency revisions.

Source-recorded status dates are preserved in every final row. Later cutoff drift is stored separately in `status_drift_evidence`. Acceptance would require a complete atomic proposition, high or medium importance, exact pinned source evidence, independently verified current-open status, source-specific rights and attribution, and comprehensive proposition-level semantic deduplication. No row supplied the complete packet.

The Bespoke Labs record layer is CC-BY-4.0 with attribution. Upstream wording is not relicensed or inherited; use remains limited to pointers or independently written summaries until a source-specific rights review is complete.

Authoritative outputs:

- `strict-review-ledger-302.jsonl` — SHA-256 `4d13d77513ee7064fbe7bfa0cbd996cb491363afa17297a2a185cb1927407600`
- `final-audit-summary.json` — SHA-256 `318e323f87dcf07450074a83492801a54fd1a33b2597004c4737722e2c6bec66`
- `final-ledger-validation.json` — SHA-256 `4d12feab6b33d47e7efc52af187e87f179600ee890d3f30ef45e28d60a34c4bb`

Rebuild and independently check from the repository root:

```bash
python3 Docs/catalog/v5/tools/build_conjecturebench_audit_v5_5.py
python3 Docs/catalog/v5/tools/check_conjecturebench_audit_v5_5.py
python3 -m unittest Docs.catalog.v5.tests.test_conjecturebench_audit_v5_5
```
