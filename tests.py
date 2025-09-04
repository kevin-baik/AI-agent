from functions.get_files_info import get_files_info, get_file_content

def tests():
    # get_files_info tests
    """
    test_cases = [
        ("calculator", "."),
        ("calculator", "pkg"),
        ("calculator", "/bin"),
        ("calculator", "../")
    ]

    for test in test_cases:
        print(f"Result for '{test[1]}' directory")
        print(f"{get_files_info(*test)}")
    """
    
    # get_file_content
    test_cases = [
        #("calculator", "lorem.txt"),
        ("calculator", "main.py"),
        ("calculator", "pkg/calculator.py"),
        ("calculator", "/bin/cat"),
        ("calculator", "pkg/does_not_exist.py")
    ]

    for test in test_cases:
        result = get_file_content(*test)
        print(result)

if __name__ == "__main__":
    tests()
