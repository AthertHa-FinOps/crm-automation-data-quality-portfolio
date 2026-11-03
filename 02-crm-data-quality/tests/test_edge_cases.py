"""Edge cases for email-based review. Original source and CRM files stay unchanged."""
import sys
import unittest
from pathlib import Path

CASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(CASE))
from run_analysis import review


def lead(lead_id, email, last_name='Patel', phone='416-555-0105'):
    return {
        'lead_id': lead_id, 'first_name': 'Ava', 'last_name': last_name,
        'email': email, 'phone': phone, 'lead_source': 'Form',
        'city': 'Stouffville', 'province': 'ON', 'created_date': '2026-11-03'
    }


def crm(crm_id, email, last_name='Patel', phone='416-555-0105'):
    return {
        'crm_id': crm_id, 'first_name': 'Ava', 'last_name': last_name,
        'email': email, 'phone': phone, 'lead_source': 'Form',
        'city': 'Stouffville', 'province': 'ON', 'created_date': '2026-11-03'
    }


class EdgeCases(unittest.TestCase):
    def test_shared_email_does_not_authorize_merge(self):
        source = [lead('L1','family@example.com')]
        rows, controls, _ = review(source, [
            crm('C1','family@example.com'), crm('C2',' FAMILY@example.com ')
        ])
        self.assertEqual(len(rows), 2)
        self.assertEqual(controls['duplicate_email_groups'], 1)
        self.assertTrue(all('POTENTIAL_DUPLICATE' in row['review_flags'] for row in rows))
        self.assertEqual({row['crm_id'] for row in rows}, {'C1','C2'})

    def test_ambiguous_source_is_not_presented_as_unique_match(self):
        source = [lead('L1','shared@example.com'), lead('L2','SHARED@example.com')]
        rows, _, _ = review(source,[crm('C1',' shared@example.com ')])
        self.assertEqual(rows[0]['source_match'], 'AMBIGUOUS_EMAIL')
        self.assertIn('AMBIGUOUS_SOURCE', rows[0]['review_flags'])

    def test_invalid_and_missing_email_cannot_establish_identity(self):
        source = [lead('L1','valid@example.com')]
        rows, _, _ = review(source,[crm('C1',''),crm('C2','bad@@example.com')])
        self.assertEqual([x['source_match'] for x in rows],
                         ['UNVERIFIABLE_EMAIL','UNVERIFIABLE_EMAIL'])
        self.assertIn('MISSING_EMAIL', rows[0]['review_flags'])
        self.assertIn('INVALID_EMAIL', rows[1]['review_flags'])

    def test_phone_format_only_is_not_a_conflict(self):
        source = [lead('L1','valid@example.com',phone='416-555-0105')]
        rows, _, _ = review(source,[crm('C1','VALID@example.com',phone='+1 (416) 555-0105')])
        self.assertEqual(rows[0]['source_match'], 'ONE_EMAIL_MATCH')
        self.assertNotIn('PHONE_CONFLICT', rows[0]['review_flags'])

    def test_conflicting_names_flag_review_without_overwrite(self):
        source = [lead('L1','valid@example.com',last_name='Patel')]
        original = crm('C1','valid@example.com',last_name='Patei')
        rows, _, _ = review(source,[original])
        self.assertIn('LAST_NAME_CONFLICT', rows[0]['review_flags'])
        self.assertEqual(rows[0]['last_name'], 'Patei')
        self.assertEqual(original['last_name'], 'Patei')


if __name__ == '__main__':
    unittest.main()
