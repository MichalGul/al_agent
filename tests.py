from functions.get_files_info import get_files_info, get_file_content
from functions.config import TRUNCATE_MESSAGE, MAX_CHARACTERS
from parameterized import parameterized
import unittest

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


class TestGetFilesContent(unittest.TestCase):



    @parameterized.expand([("calculator", "main.py", "Calculator App"),
                            ("calculator", "pkg/calculator.py", "self.operators"),
                              ("calculator", "lorem.txt", "Lorem")])
    def test_read_valid(self, input1, input2, expected):
        result = get_file_content(input1, input2)

        truncate_msg_len = len(TRUNCATE_MESSAGE.format("lorem.txt", MAX_CHARACTERS))
        # print(result)
        assert len(result) <= MAX_CHARACTERS + truncate_msg_len + 1
        assert expected in result

    def test_invalid_read(self):
        result = get_file_content("calculator", "/bin/cat")
        # print(result)
        assert "Error" in result



if __name__ == "__main__":
    unittest.main()
