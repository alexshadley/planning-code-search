import unittest
from backend.load import load_document


class MyTestCase(unittest.TestCase):
    def test_no_runtime_errors(self):
        sb330 = load_document('../corpus/sb330.txt')
        assert sb330
        assert len(sb330) > 1
        assert max([len(str(c)) for c in sb330]) < 4000
        
        sb423 = load_document('../corpus/sb423.txt')
        assert sb423
        assert len(sb423) > 1
        assert max([len(str(c)) for c in sb423]) < 4000
        
        sf_pc_html = load_document('../corpus/san_francisco-ca-2.html')
        assert sf_pc_html
        assert len(sf_pc_html) > 1
        assert max([len(str(c)) for c in sf_pc_html]) < 4000
        
        sf_pc_txt = load_document('../corpus/san_francisco-ca-1.txt')
        assert sf_pc_txt
        assert len(sf_pc_txt) > 1
        assert max([len(str(c)) for c in sf_pc_txt]) < 4000


if __name__ == '__main__':
    unittest.main()
