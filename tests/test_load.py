import unittest
from backend.load import load_document


class MyTestCase(unittest.TestCase):
    def test_no_runtime_errors(self):
        sb330 = load_document('../sb330.txt')
        assert sb330
        assert max([len(str(c)) for c in sb330]) < 4000
        
        sb423 = load_document('../sb423.txt')
        assert sb423
        print(len(sb423))
        assert max([len(str(c)) for c in sb423]) < 4000
        
        sf_pc_html = load_document('../san_francisco-ca-2.html')
        assert sf_pc_html
        print(len(sf_pc_html))
        assert max([len(str(c)) for c in sf_pc_html]) < 4000
        
        sf_pc_txt = load_document('../san_francisco-ca-1.txt')
        assert sf_pc_txt
        print(len(sf_pc_txt))
        assert max([len(str(c)) for c in sf_pc_txt]) < 4000


if __name__ == '__main__':
    unittest.main()
