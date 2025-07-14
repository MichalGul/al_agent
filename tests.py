from functions.get_files_info import get_files_info
import unittest
from parameterized import parameterized


class TestGetFilesInfo(unittest.TestCase):

    @parameterized.expand([("calculator", ".", "main.py"), ("calculator", "pkg", "render.py")])
    def test_valid_params(self, input1, input2, expected):
        result = get_files_info(input1, input2)
        print(result)
        assert expected in result

    @parameterized.expand([("calculator", "/bin", 1), ("calculator", "/user", 1), ("calculator", "../", 1)])
    def test_invalid_params(self, input1, input2, expected):
        result = get_files_info(input1, input2)
        print(result)
        assert "Error:" in result

if __name__ == "__main__":
    unittest.main()
