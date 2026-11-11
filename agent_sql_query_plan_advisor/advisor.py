"""Core SQL Query Plan Advisor implementation."""
import re
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class QueryAnalysis:
    has_full_scan_risk: bool
    recommended_index_ddl: Optional[str]
    identified_filters: List[str]
    speedup_potential: str

class SQLQueryAdvisor:
    """Analyzes SQL queries for missing index risks and generates targeted DDL recommendations."""
    
    def analyze_query(self, sql_query: str) -> QueryAnalysis:
        query_clean = " ".join(sql_query.split())
        
        # Extract table name
        table_match = re.search(r"\bFROM\s+([a-zA-Z0-9_]+)", query_clean, re.IGNORECASE)
        table_name = table_match.group(1) if table_match else "target_table"

        # Extract WHERE filter columns
        where_match = re.search(r"\bWHERE\s+(.+?)(?:\s+ORDER\s+BY|\s+GROUP\s+BY|\s+LIMIT|$)", query_clean, re.IGNORECASE)
        filters = []
        if where_match:
            where_clause = where_match.group(1)
            # Find column names preceding operators
            col_matches = re.findall(r"([a-zA-Z0-9_]+)\s*(?:=|!=|<|>|LIKE|IN)", where_clause, re.IGNORECASE)
            filters = list(dict.fromkeys(col_matches))

        # Extract ORDER BY columns
        order_match = re.search(r"\bORDER\s+BY\s+([a-zA-Z0-9_,\s]+)(?:\s+LIMIT|$)", query_clean, re.IGNORECASE)
        order_cols = []
        if order_match:
            order_cols = [c.strip().split()[0] for c in order_match.group(1).split(",") if c.strip()]

        # Determine composite index columns
        index_cols = list(dict.fromkeys(filters + order_cols))
        has_risk = len(index_cols) > 0
        ddl = None
        speedup = "1x"

        if has_risk:
            cols_str = ", ".join(index_cols)
            idx_name = f"idx_{table_name}_{'_'.join(index_cols)[:24]}"
            ddl = f"CREATE INDEX {idx_name} ON {table_name} ({cols_str});"
            speedup = "100x - 500x"

        return QueryAnalysis(
            has_full_scan_risk=has_risk,
            recommended_index_ddl=ddl,
            identified_filters=filters,
            speedup_potential=speedup
        )
