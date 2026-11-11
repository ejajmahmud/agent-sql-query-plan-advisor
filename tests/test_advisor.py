"""Unit tests for agent-sql-query-plan-advisor."""
import unittest
from agent_sql_query_plan_advisor.advisor import SQLQueryAdvisor

class TestSQLQueryAdvisor(unittest.TestCase):
    def setUp(self):
        self.advisor = SQLQueryAdvisor()

    def test_composite_index_recommendation(self):
        q = "SELECT id FROM users WHERE email = 'test@example.com' ORDER BY joined_at"
        res = self.advisor.analyze_query(q)
        self.assertTrue(res.has_full_scan_risk)
        self.assertIn("CREATE INDEX idx_users_", res.recommended_index_ddl)
        self.assertIn("email, joined_at", res.recommended_index_ddl)
