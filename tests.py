from functions.get_files_info import get_files_info, get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file


from functions.config import TRUNCATE_MESSAGE, MAX_CHARACTERS
from parameterized import parameterized
import unittest

# class TestGetFilesInfo(unittest.TestCase):

#     @parameterized.expand([("calculator", ".", "main.py"), ("calculator", "pkg", "render.py")])
#     def test_valid_params(self, input1, input2, expected):
#         result = get_files_info(input1, input2)
#         print(result)
#         assert expected in result

#     @parameterized.expand([("calculator", "/bin", 1), ("calculator", "/user", 1), ("calculator", "../", 1)])
#     def test_invalid_params(self, input1, input2, expected):
#         result = get_files_info(input1, input2)
#         print(result)
#         assert "Error:" in result


# class TestGetFilesContent(unittest.TestCase):


#     @parameterized.expand([("calculator", "main.py", "Calculator App"),
#                             ("calculator", "pkg/calculator.py", "self.operators"),
#                               ("calculator", "lorem.txt", "Lorem")])
#     def test_read_valid(self, input1, input2, expected):
#         result = get_file_content(input1, input2)

#         truncate_msg_len = len(TRUNCATE_MESSAGE.format("lorem.txt", MAX_CHARACTERS))
#         # print(result)
#         assert len(result) <= MAX_CHARACTERS + truncate_msg_len + 1
#         assert expected in result

#     def test_invalid_read(self):
#         result = get_file_content("calculator", "/bin/cat")
#         # print(result)
#         assert "Error" in result


class TestWriteToFiles(unittest.TestCase):



    @parameterized.expand([("calculator", "lorem1.txt", "wait, this isn't lorem ipsum", "Successfully wrote"),
                            ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet", "Successfully wrote")])
    def test_write_valid(self, input1, input2, input3, expected):
        result = write_file(input1, input2, input3)
        print(result)
        assert expected in result

    def test_invalid_write(self):
        result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
        print(result)
        assert "Error" in result



class TestExecutePythonFile(unittest.TestCase):

    
    @parameterized.expand([("calculator", "main.py", "Calculator App"),
                            ("calculator", "tests.py", "Ran")])
    def test_valid_run(self, input1, input2, expected):
        result = run_python_file(input1, input2)
        print(result)
        assert expected in result

    @parameterized.expand([("calculator", "../main.py", "Error:"),
                            ("calculator", "nonexistent.py", "Error:")])
    def test_invalid_run(self, input1, input2, expected):
        result = run_python_file(input1, input2)
        print(result)
        assert expected in result


if __name__ == "__main__":
    unittest.main()
