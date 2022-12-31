from django.test import TestCase
from dictionary.words_operation import Corrector

class TestCorrector(TestCase):

    def setUp(self):
        self.corrector = Corrector()

    def test_check_answer(self):
        #typo
        self.assertEqual(self.corrector.check_answer('ass*ssin', 'assassin', '<', '>'),
                                                    'ass<a>ssin')
        #typo in the start
        self.assertEqual(self.corrector.check_answer('*ssassin', 'assassin', '<', '>'),
                                                    '<a>ssassin')
        #typo in the end
        self.assertEqual(self.corrector.check_answer('assassi*', 'assassin', '<', '>'),
                                                    'assassi<n>')
        #replaced symbols
        self.assertEqual(self.corrector.check_answer('asasssin', 'assassin', '<', '>'),
                                                    'as<sa>ssin')
        #replaced symbols in the start
        self.assertEqual(self.corrector.check_answer('sasassin', 'assassin', '<', '>'),
                                                    '<as>sassin')
        #replaced symbols in the end
        self.assertEqual(self.corrector.check_answer('assassni', 'assassin', '<', '>'),
                                                    'assass<in>')
        #extra symbol
        self.assertEqual(self.corrector.check_answer('ass*assin', 'assassin', '<', '>'),
                                                    'as<sa>ssin')
        #extra symbol in the start
        self.assertEqual(self.corrector.check_answer('*assassin', 'assassin', '<', '>'),
                                                    '<a>ssassin')
        #extra symbol in the end
        self.assertEqual(self.corrector.check_answer('assassin*', 'assassin', '<', '>'),
                                                    'assassi<n>')
        #doubled symbol
        self.assertEqual(self.corrector.check_answer('assaassin', 'assassin', '<', '>'),
                                                    'ass<a>ssin')
        #doubled symbol in the start
        self.assertEqual(self.corrector.check_answer('aassassin', 'assassin', '<', '>'),
                                                    '<a>ssassin')
        #doubled symbol in the end
        self.assertEqual(self.corrector.check_answer('assassinn', 'assassin', '<', '>'),
                                                    'assassi<n>')
        #passed symbol
        self.assertEqual(self.corrector.check_answer('assssin', 'assassin', '<', '>'),
                                                    'ass<a>ssin')
        #passed symbol in the start
        self.assertEqual(self.corrector.check_answer('*ssassin', 'assassin', '<', '>'),
                                                    '<a>ssassin')
        #passed symbol in the end
        self.assertEqual(self.corrector.check_answer('assassi', 'assassin', '<', '>'),
                                                    'assassi<n>')
        #tripled doubled symbols
        self.assertEqual(self.corrector.check_answer('asssassin', 'assassin', '<', '>'),
                                                    'a<ss>assin')
        #tripled doubled symbols in the start
        self.assertEqual(self.corrector.check_answer('qqqwerty', 'qqwerty', '<', '>'),
                                                    '<qq>werty')
        #tripled doubled symbols in the end
        self.assertEqual(self.corrector.check_answer('qwertyyy', 'qwertyy', '<', '>'),
                                                    'qwert<yy>')
        #similar
        self.assertEqual(self.corrector.check_answer('qwerty', 'qwerty', '<', '>'), 1)
        #two mistakes
        self.assertEqual(self.corrector.check_answer('qw*rt*', 'qwerty', '<', '>'), 0)
