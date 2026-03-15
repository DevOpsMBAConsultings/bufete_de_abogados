from odoo.tests.common import TransactionCase

class TestLegalAdvice(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestLegalAdvice, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({'name': 'Test Client'})
        cls.lawyer = cls.env['lawyer'].create({'name': 'Test Lawyer'})
        cls.practice_area = cls.env['practice.area'].create({'name': 'Civil'})

    def test_advice_to_case_conversion(self):
        """Test the conversion of Legal Advice to a Case record"""
        advice = self.env['legal.advice'].create({
            'partner_id': self.partner.id,
            'lawyer_id': self.lawyer.id,
            'practice_area_id': self.practice_area.id,
            'description': 'Test legal issue',
            'advice_given': 'Take no action.',
        })

        # Confirm advice
        advice.action_confirm()
        self.assertEqual(advice.state, 'confirmed')

        # Create case
        action = advice.action_create_case()
        case_id = action['res_id']
        case = self.env['lawyer.case'].browse(case_id)

        # Verify case details
        self.assertEqual(case.partners_id, self.partner)
        self.assertEqual(case.assigned_lawyer, self.lawyer)
        self.assertEqual(case.case_type_id, self.practice_area)
        self.assertEqual(case.description, 'Take no action.')
        self.assertEqual(advice.state, 'converted')
        self.assertEqual(advice.case_id, case)
