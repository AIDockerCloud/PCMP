#!/usr/bin/env python3
"""
PCMP (Project Context Management Protocol) SQLite Derivative Indexer
Plan A: Zero-dependency implementation using Python 3 standard library.
Generates and maintains a rebuildable index cache at ai/.cache/index.sqlite.
"""

import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import sys

# Mapping for information layering tags
TAG_NORMALIZATION = {
    "事实": "fact",
    "fact": "fact",
    "假设": "assumption",
    "assumption": "assumption",
    "提议": "proposal",
    "proposal": "proposal",
    "已确认": "accepted",
    "accepted": "accepted",
    "未决": "open",
    "open": "open",
}


def find_project_root() -> Path:
    """Locate project root by searching upwards for PROJECT_CONTEXT_ZH.md or .git."""
    curr = Path.cwd().resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "PROJECT_CONTEXT_ZH.md").exists() or (parent / "PROJECT_CONTEXT.md").exists():
            return parent
        if (parent / ".git").exists():
            return parent
    return curr


class PCMPIndex:
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir
        self.ai_dir = root_dir / "ai"
        self.cache_dir = self.ai_dir / ".cache"
        self.db_path = self.cache_dir / "index.sqlite"

    def init_db(self, reset: bool = False):
        """Initialize or reset the SQLite database schema."""
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if reset and self.db_path.exists():
            self.db_path.unlink()

        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # 1. File metadata
        cur.execute("""
            CREATE TABLE IF NOT EXISTS file_meta (
                file_path TEXT PRIMARY KEY,
                content_hash TEXT NOT NULL,
                revision INTEGER DEFAULT 1,
                pcmp_version TEXT,
                updated_at TEXT,
                last_indexed_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # 2. Decisions (ADR)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                date TEXT,
                status TEXT NOT NULL,
                confirmation_source TEXT,
                context TEXT,
                decision TEXT,
                reason TEXT,
                alternatives TEXT,
                consequences TEXT,
                raw_markdown TEXT
            );
        """)

        # 3. Issues
        cur.execute("""
            CREATE TABLE IF NOT EXISTS issues (
                id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                description TEXT,
                impact TEXT,
                workaround TEXT,
                component TEXT,
                raw_markdown TEXT
            );
        """)

        # 4. Sessions
        cur.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                date TEXT,
                agent TEXT,
                task TEXT,
                status TEXT,
                goal TEXT,
                what TEXT,
                result TEXT,
                next_action TEXT,
                raw_markdown TEXT
            );
        """)

        # 5. Tagged Items
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tagged_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                line_number INTEGER,
                tag TEXT NOT NULL,
                normalized_tag TEXT NOT NULL,
                content TEXT NOT NULL
            );
        """)

        # 6. FTS5 Virtual Table for full-text search
        try:
            cur.execute("""
                CREATE VIRTUAL TABLE IF NOT EXISTS fts_content USING fts5(
                    file_path UNINDEXED,
                    section_title,
                    body_text
                );
            """)
        except sqlite3.OperationalError:
            # Fallback if FTS5 is not compiled in sqlite3
            pass

        conn.commit()
        conn.close()

    def get_conn(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    @staticmethod
    def compute_sha256(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def parse_frontmatter(self, text: str) -> tuple[dict, str]:
        """Extract YAML-like frontmatter between leading --- delimiters."""
        metadata = {}
        body = text
        if text.startswith("---"):
            parts = text.split("---", 2)
            if len(parts) >= 3:
                fm_text = parts[1]
                body = parts[2]
                for line in fm_text.strip().splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        val = v.strip().strip('"').strip("'")
                        metadata[k.strip()] = val
        return metadata, body

    def extract_tags(self, file_path_rel: str, text: str, cur: sqlite3.Cursor):
        """Extract information layering tags [事实], [假设], [提议], [已确认], [未决] etc."""
        # Remove old tags for this file
        cur.execute("DELETE FROM tagged_items WHERE file_path = ?", (file_path_rel,))
        tag_regex = re.compile(r"\[(事实|假设|提议|已确认|未决|fact|assumption|proposal|accepted|open)\]", re.IGNORECASE)

        for line_no, line in enumerate(text.splitlines(), start=1):
            matches = tag_regex.findall(line)
            if matches:
                # Store the line content cleaned up
                content = line.strip()
                for match in set(matches):
                    norm = TAG_NORMALIZATION.get(match.lower(), match.lower())
                    cur.execute("""
                        INSERT INTO tagged_items (file_path, line_number, tag, normalized_tag, content)
                        VALUES (?, ?, ?, ?, ?)
                    """, (file_path_rel, line_no, match, norm, content))

    def index_decisions(self, text: str, cur: sqlite3.Cursor):
        """Parse ADRs from DECISIONS.md."""
        cur.execute("DELETE FROM decisions")
        # Split on ## DEC-
        pattern = re.compile(r"^##\s+(DEC-\d+)\s+[—\-]\s+(.+)$", re.MULTILINE)
        matches = list(pattern.finditer(text))

        for i, match in enumerate(matches):
            dec_id = match.group(1).strip()
            title = match.group(2).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            block = text[start:end].strip()

            date_val = ""
            status_val = "Proposed"
            conf_source = ""
            context_val = ""
            decision_val = ""
            reason_val = ""
            alt_val = ""
            conseq_val = ""

            for line in block.splitlines():
                line_s = line.strip()
                if line_s.startswith("日期:") or line_s.startswith("Date:"):
                    # e.g. 日期: 2026-10-19 | 状态: Accepted
                    if "|" in line_s:
                        parts = line_s.split("|")
                        date_val = parts[0].split(":", 1)[1].strip()
                        status_val = parts[1].split(":", 1)[1].strip()
                    else:
                        date_val = line_s.split(":", 1)[1].strip()
                elif line_s.startswith("- 确认来源:") or line_s.startswith("- Confirmation Source:"):
                    conf_source = line_s.split(":", 1)[1].strip()
                elif line_s.startswith("- 背景") or line_s.startswith("- Context:"):
                    context_val = line_s.split(":", 1)[1].strip()
                elif line_s.startswith("- 决策") or line_s.startswith("- Decision:"):
                    decision_val = line_s.split(":", 1)[1].strip()
                elif line_s.startswith("- 理由") or line_s.startswith("- Reason:"):
                    reason_val = line_s.split(":", 1)[1].strip()
                elif line_s.startswith("- 备选方案") or line_s.startswith("- Alternatives:"):
                    alt_val = line_s.split(":", 1)[1].strip()
                elif line_s.startswith("- 影响") or line_s.startswith("- Consequences:"):
                    conseq_val = line_s.split(":", 1)[1].strip()

            cur.execute("""
                INSERT OR REPLACE INTO decisions (
                    id, title, date, status, confirmation_source, context, decision, reason, alternatives, consequences, raw_markdown
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (dec_id, title, date_val, status_val, conf_source, context_val, decision_val, reason_val, alt_val, conseq_val, block))

    def index_issues(self, text: str, cur: sqlite3.Cursor):
        """Parse ISSUES.md tables or lists."""
        cur.execute("DELETE FROM issues")
        for line in text.splitlines():
            # Table row: | ISS-001 | 状态 | 描述 | ...
            if "|" in line and "ISS-" in line:
                cols = [c.strip() for c in line.split("|") if c.strip()]
                if len(cols) >= 3 and cols[0].startswith("ISS-"):
                    iss_id = cols[0]
                    status = cols[1]
                    desc = cols[2]
                    impact = cols[3] if len(cols) > 3 else ""
                    comp = cols[4] if len(cols) > 4 else ""
                    workaround = cols[5] if len(cols) > 5 else ""
                    cur.execute("""
                        INSERT OR REPLACE INTO issues (
                            id, status, description, impact, workaround, component, raw_markdown
                        ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (iss_id, status, desc, impact, workaround, comp, line.strip()))

    def index_fts(self, file_path_rel: str, text: str, cur: sqlite3.Cursor):
        """Split document by markdown headers and index into FTS5."""
        try:
            cur.execute("DELETE FROM fts_content WHERE file_path = ?", (file_path_rel,))
            sections = re.split(r"\n(?=#{1,4}\s+)", text)
            for sec in sections:
                sec = sec.strip()
                if not sec:
                    continue
                first_line, *rest = sec.splitlines()
                title = first_line.lstrip("#").strip()
                body = "\n".join(rest).strip()
                cur.execute("""
                    INSERT INTO fts_content (file_path, section_title, body_text)
                    VALUES (?, ?, ?)
                """, (file_path_rel, title, body))
        except sqlite3.OperationalError:
            pass

    def index_file(self, file_path: Path, cur: sqlite3.Cursor) -> bool:
        """Parse and index a single Markdown file."""
        if not file_path.exists() or not file_path.is_file():
            return False

        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)
            return False

        rel_path = str(file_path.relative_to(self.root_dir))
        content_hash = self.compute_sha256(content)

        # Check existing hash
        cur.execute("SELECT content_hash FROM file_meta WHERE file_path = ?", (rel_path,))
        row = cur.fetchone()
        if row and row[0] == content_hash:
            return False  # Up to date

        # Parse Frontmatter
        fm, body = self.parse_frontmatter(content)
        rev = int(fm.get("revision", 1))
        pcmp_v = fm.get("pcmp_version", "2.1")
        updated_at = fm.get("updated", "")

        # Save meta
        cur.execute("""
            INSERT OR REPLACE INTO file_meta (file_path, content_hash, revision, pcmp_version, updated_at, last_indexed_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (rel_path, content_hash, rev, pcmp_v, updated_at))

        # Tags extraction
        self.extract_tags(rel_path, content, cur)

        # FTS indexing
        self.index_fts(rel_path, content, cur)

        # Specific file parsers
        filename = file_path.name
        if filename == "DECISIONS.md":
            self.index_decisions(content, cur)
        elif filename == "ISSUES.md":
            self.index_issues(content, cur)

        return True

    def scan_and_index(self, rebuild: bool = False) -> tuple[int, int]:
        """Index all markdown files under ai/ directory and root protocol files."""
        self.init_db(reset=rebuild)
        conn = self.get_conn()
        cur = conn.cursor()

        target_files = []
        # Protocol files in root
        for root_file in ["PROJECT_CONTEXT_ZH.md", "PROJECT_CONTEXT.md", "README.md", "AGENTS.md"]:
            p = self.root_dir / root_file
            if p.exists():
                target_files.append(p)

        # All markdown files under ai/ (excluding .cache/)
        if self.ai_dir.exists():
            for p in self.ai_dir.rglob("*.md"):
                if ".cache" not in p.parts:
                    target_files.append(p)

        indexed_count = 0
        total_files = len(target_files)

        for p in target_files:
            if self.index_file(p, cur):
                indexed_count += 1

        conn.commit()
        conn.close()
        return indexed_count, total_files

    def get_stats(self) -> dict:
        if not self.db_path.exists():
            return {"status": "Database not initialized. Run --rebuild first."}

        conn = self.get_conn()
        cur = conn.cursor()

        stats = {
            "database_path": str(self.db_path.relative_to(self.root_dir)),
            "database_size_bytes": self.db_path.stat().st_size if self.db_path.exists() else 0,
        }

        for table in ["file_meta", "decisions", "issues", "sessions", "tagged_items"]:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table + "_count"] = cur.fetchone()[0]

        # Tag breakdown
        cur.execute("SELECT normalized_tag, COUNT(*) FROM tagged_items GROUP BY normalized_tag")
        stats["tags_breakdown"] = {row[0]: row[1] for row in cur.fetchall()}

        conn.close()
        return stats

    def query_decisions(self, status: str = None) -> list[dict]:
        conn = self.get_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if status:
            cur.execute("SELECT * FROM decisions WHERE LOWER(status) = LOWER(?) ORDER BY id", (status,))
        else:
            cur.execute("SELECT * FROM decisions ORDER BY id")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def query_tags(self, tag: str = None) -> list[dict]:
        conn = self.get_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        if tag:
            norm = TAG_NORMALIZATION.get(tag.lower(), tag.lower())
            cur.execute("SELECT * FROM tagged_items WHERE normalized_tag = ? ORDER BY file_path, line_number", (norm,))
        else:
            cur.execute("SELECT * FROM tagged_items ORDER BY normalized_tag, file_path, line_number")
        rows = [dict(r) for r in cur.fetchall()]
        conn.close()
        return rows

    def search_fts(self, query: str) -> list[dict]:
        conn = self.get_conn()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        results = []
        try:
            cur.execute("""
                SELECT file_path, section_title, snippet(fts_content, 2, '<b>', '</b>', '...', 20) as snippet
                FROM fts_content
                WHERE fts_content MATCH ?
                LIMIT 20
            """, (query,))
            results = [dict(r) for r in cur.fetchall()]
        except sqlite3.OperationalError:
            pass

        # If FTS returns no results (e.g. CJK terms without whitespace), fallback to LIKE search
        if not results:
            cur.execute("""
                SELECT file_path, section_title, body_text
                FROM fts_content
                WHERE body_text LIKE ? OR section_title LIKE ?
                LIMIT 20
            """, (f"%{query}%", f"%{query}%"))
            for r in cur.fetchall():
                body = r["body_text"]
                pos = body.find(query)
                if pos != -1:
                    start = max(0, pos - 40)
                    end = min(len(body), pos + len(query) + 40)
                    snippet = ("..." if start > 0 else "") + body[start:pos] + f"<b>{query}</b>" + body[pos+len(query):end] + ("..." if end < len(body) else "")
                else:
                    snippet = body[:120] + ("..." if len(body) > 120 else "")
                results.append({
                    "file_path": r["file_path"],
                    "section_title": r["section_title"],
                    "snippet": snippet
                })

        conn.close()
        return results


def main():
    parser = argparse.ArgumentParser(description="PCMP SQLite Derivative Indexer (Plan A)")
    parser.add_argument("--rebuild", action="store_true", help="Full rebuild of SQLite database")
    parser.add_argument("--update", action="store_true", help="Incremental index of modified files")
    parser.add_argument("--status", action="store_true", help="Display index cache statistics")
    parser.add_argument("--query-decisions", action="store_true", help="List architectural decision records (ADRs)")
    parser.add_argument("--query-tags", action="store_true", help="List information layering tagged items")
    parser.add_argument("--status-filter", type=str, default=None, help="Filter status for decisions or issues")
    parser.add_argument("--tag-filter", type=str, default=None, help="Filter by tag (fact/assumption/proposal/accepted/open)")
    parser.add_argument("--search", type=str, default=None, help="Full-text search across all documents")
    parser.add_argument("--json", action="store_true", help="Format output as JSON")

    args = parser.parse_args()
    root = find_project_root()
    index = PCMPIndex(root)

    if args.rebuild:
        indexed, total = index.scan_and_index(rebuild=True)
        print(f"Index fully rebuilt: {indexed}/{total} files indexed at {index.db_path}")
        return

    if args.update:
        indexed, total = index.scan_and_index(rebuild=False)
        print(f"Incremental update complete: {indexed} updated out of {total} files.")
        return

    if args.status:
        stats = index.get_stats()
        if args.json:
            print(json.dumps(stats, indent=2, ensure_ascii=False))
        else:
            print("=== PCMP SQLite Derivative Index Status ===")
            for k, v in stats.items():
                print(f"  {k}: {v}")
        return

    if args.query_decisions:
        decisions = index.query_decisions(status=args.status_filter)
        if args.json:
            print(json.dumps(decisions, indent=2, ensure_ascii=False))
        else:
            print(f"Found {len(decisions)} decision(s):")
            for d in decisions:
                print(f"  [{d['id']}] {d['title']} (Status: {d['status']}, Date: {d['date']})")
                if d.get("confirmation_source"):
                    print(f"    - Source: {d['confirmation_source']}")
                if d.get("decision"):
                    print(f"    - Decision: {d['decision']}")
        return

    if args.query_tags:
        tags = index.query_tags(tag=args.tag_filter)
        if args.json:
            print(json.dumps(tags, indent=2, ensure_ascii=False))
        else:
            print(f"Found {len(tags)} tagged item(s):")
            for t in tags:
                print(f"  [{t['normalized_tag'].upper()}] {t['file_path']}:{t['line_number']} — {t['content']}")
        return

    if args.search:
        results = index.search_fts(args.search)
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"Search results for '{args.search}':")
            for r in results:
                print(f"  [{r['file_path']}] {r['section_title']}")
                print(f"    {r['snippet']}\n")
        return

    # Default action if no flags provided: display help
    parser.print_help()


if __name__ == "__main__":
    main()
