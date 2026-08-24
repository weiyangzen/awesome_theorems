#!/usr/bin/env python3
"""Build deterministic lexical retrieval evidence for AimPL semantic dedupe.

Retrieval is deliberately advisory: no similarity score grants or denies credit.
Every final duplicate verdict remains a per-record review decision.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import html
import json
import math
from pathlib import Path
import re
import unicodedata


REPO_ROOT = Path(__file__).resolve().parents[4]
SOURCE_DIR = REPO_ROOT / "Docs/catalog/v5/sources/aimpl"
CURATION_DIR = REPO_ROOT / "Docs/catalog/v5/curation/aimpl_v5_5"
PARENT = REPO_ROOT / "Docs/catalog/v5/releases/5.4/Claim_Catalog.json"
CB = CURATION_DIR / "crosscheck-conjecturebench-302.jsonl"
OEIS = CURATION_DIR / "crosscheck-oeis-602.jsonl"

STOP = {
    "a", "all", "an", "and", "are", "as", "at", "be", "been", "being", "by", "can",
    "conjecture", "conjectured", "does", "every", "for", "from", "has", "have", "if",
    "in", "is", "it", "its", "let", "of", "on", "or", "problem", "prove", "show", "so",
    "such", "than", "that", "the", "then", "there", "this", "to", "under", "when", "where",
    "which", "with", "would", "stated", "following", "true", "holds", "source", "claim",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_line(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":")) + "\n").encode("utf-8")


def binding(path: Path, *, rows: int | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "path": path.relative_to(REPO_ROOT).as_posix(),
        "sha256": sha256(path),
        "size_bytes": path.stat().st_size,
    }
    if rows is not None:
        result["rows"] = rows
    return result


def normalize(value: str) -> str:
    value = html.unescape(value or "")
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.lower().replace("\\", " ")
    value = re.sub(r"<[^>]*>", " ", value)
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def features(value: str) -> Counter[str]:
    words = [w for w in normalize(value).split() if len(w) >= 2 and w not in STOP]
    result = Counter(words)
    # Adjacent content-word bigrams make names and mathematical phrases more discriminating.
    result.update("~".join(pair) for pair in zip(words, words[1:]))
    return result


def vector(counter: Counter[str], idf: dict[str, float]) -> dict[str, float]:
    return {term: (1.0 + math.log(count)) * idf.get(term, 1.0)
            for term, count in counter.items()}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    dot = sum(weight * b.get(term, 0.0) for term, weight in a.items())
    na = math.sqrt(sum(x * x for x in a.values()))
    nb = math.sqrt(sum(x * x for x in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def load_reviews() -> dict[int, dict]:
    result = {}
    for path in (CURATION_DIR / "review-a.jsonl", CURATION_DIR / "review-b.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            if row["candidate_index"] in result:
                raise ValueError(f"duplicate review for candidate {row['candidate_index']}")
            result[row["candidate_index"]] = row
    if sorted(result) != list(range(1, 60)):
        raise ValueError("review coverage is not exactly candidates 1..59")
    return result


def main() -> None:
    candidates_path = SOURCE_DIR / "candidates.jsonl"
    aimpl = [json.loads(line) for line in candidates_path.read_text(encoding="utf-8").splitlines()]
    reviews = load_reviews()
    queries = []
    for row in aimpl:
        review = reviews.get(row["candidate_index"], {})
        text = "\n".join(filter(None, [
            row["exact_source"].get("problem_name"),
            row["exact_source"].get("body_plain_text"),
            row["exact_source"].get("intro_plain_text"),
            row["context"].get("section_title"),
            row["context"].get("list_title"),
            review.get("semantic_summary"),
        ]))
        queries.append({"id": f"aimpl/{row['candidate_index']}", "index": row["candidate_index"],
                        "key": row["candidate_key"], "text": text})

    corpora: dict[str, list[dict]] = {"parent_5_4": [], "conjecturebench": [], "oeis": [], "aimpl_batch": []}
    parent = json.loads(PARENT.read_text(encoding="utf-8"))
    for row in parent["records"]:
        statement = row.get("statement") or {}
        text = "\n".join(str(x) for x in [
            row.get("display_name", ""),
            " ".join(row.get("aliases") or []),
            statement.get("natural_language") or "",
            row.get("formal_docstring") or "",
            row.get("formal_type") or "",
        ] if x)
        corpora["parent_5_4"].append({
            "id": row.get("variant_id"), "text": text,
            "label": row.get("display_name"), "claim_kind": row.get("current_claim_kind"),
            "material_status": row.get("material_status"),
        })
    for row in map(json.loads, CB.read_text(encoding="utf-8").splitlines()):
        corpora["conjecturebench"].append({
            "id": row["cb_id"],
            "text": "\n".join([row["record"].get("title", ""), row.get("exact_statement", "")]),
            "label": row["record"].get("title"),
            "claim_kind": "conjecture",
            "material_status": row["record"].get("status_observation", {}).get("state"),
        })
    for row in map(json.loads, OEIS.read_text(encoding="utf-8").splitlines()):
        locations = row.get("locations") or []
        originals = "\n".join(x.get("original_text", "") for x in locations)
        corpora["oeis"].append({
            "id": row["candidate_key"], "text": originals or row.get("normalized_text", ""),
            "label": ",".join(x.get("a_number", "") for x in locations),
            "claim_kind": "candidate", "material_status": "unreviewed_or_reviewed_elsewhere",
        })
    for query in queries:
        corpora["aimpl_batch"].append({
            "id": query["id"], "text": query["text"], "label": query["id"],
            "claim_kind": "candidate", "material_status": "same_snapshot",
        })

    all_counters = [features(q["text"]) for q in queries]
    ref_counters: dict[str, list[Counter[str]]] = {}
    for name, rows in corpora.items():
        counters = [features(row["text"]) for row in rows]
        ref_counters[name] = counters
        all_counters.extend(counters)
    document_count = len(all_counters)
    df = Counter(term for counter in all_counters for term in counter)
    idf = {term: math.log((document_count + 1) / (freq + 1)) + 1 for term, freq in df.items()}
    query_vectors = [vector(features(q["text"]), idf) for q in queries]
    corpus_vectors = {name: [vector(counter, idf) for counter in ref_counters[name]]
                      for name in corpora}

    output = []
    for query, qvec in zip(queries, query_vectors):
        matches = {}
        for name, rows in corpora.items():
            scored = []
            for row, rvec in zip(rows, corpus_vectors[name]):
                if name == "aimpl_batch" and row["id"] == query["id"]:
                    continue
                score = cosine(qvec, rvec)
                scored.append((score, row))
            scored.sort(key=lambda item: (-item[0], item[1]["id"] or ""))
            matches[name] = [{
                "score": round(score, 6),
                "id": row["id"],
                "label": row["label"],
                "claim_kind": row["claim_kind"],
                "material_status": row["material_status"],
                "text_excerpt": re.sub(r"\s+", " ", row["text"]).strip()[:800],
            } for score, row in scored[:8]]
        output.append({
            "candidate_index": query["index"], "candidate_key": query["key"],
            "query_text": query["text"], "retrieval_only_not_a_verdict": True,
            "top_matches": matches,
        })
    payload = b"".join(canonical_line(row) for row in output)
    out_path = CURATION_DIR / "cross-dedupe-retrieval.jsonl"
    out_path.write_bytes(payload)
    summary = {
        "schema_version": "awesome-theorems/aimpl-cross-dedupe-retrieval/1",
        "artifact": "Docs/catalog/v5/curation/aimpl_v5_5/cross-dedupe-retrieval-summary.json",
        "algorithm": "deterministic unigram-plus-bigram TF-IDF cosine; advisory only",
        "counts": {"aimpl_queries": len(queries), **{k: len(v) for k, v in corpora.items()}},
        "inputs": {
            "aimpl_candidates": binding(candidates_path, rows=len(aimpl)),
            "parent_5_4": binding(PARENT, rows=len(parent["records"])),
            "conjecturebench": binding(CB, rows=len(corpora["conjecturebench"])),
            "oeis_candidates": binding(OEIS, rows=len(corpora["oeis"])),
        },
        "output": {
            "path": out_path.relative_to(REPO_ROOT).as_posix(),
            "sha256": hashlib.sha256(payload).hexdigest(),
            "size_bytes": len(payload),
            "rows": len(output),
        },
        "output_sha256": hashlib.sha256(payload).hexdigest(),
        "review_boundary": "Scores retrieve candidates only; semantic equivalence requires manual review.",
    }
    (CURATION_DIR / "cross-dedupe-retrieval-summary.json").write_bytes(canonical_line(summary))
    print(f"PASS retrieval rows={len(output)} sha256={summary['output_sha256']}")


if __name__ == "__main__":
    main()
