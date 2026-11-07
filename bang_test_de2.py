tests = {
    "Cau1": [
        {"input": "1\n", "expected": ["Tổng các ước số là: 1", "S = 1"]},
        {"input": "2\n", "expected": ["Tổng các ước số là: 3", "S = 5"]},
        {"input": "3\n", "expected": ["Tổng các ước số là: 4", "S = 32"]},
        {"input": "6\n", "expected": ["Tổng các ước số là: 12", "S = 50069"]},
        {"input": "12\n", "expected": ["Tổng các ước số là: 28", "S = 9211817190184"]},
        {"input": "50\n", "expected": ["Tổng các ước số là: 93"]},
        {"input": "99\n", "expected": ["Tổng các ước số là: 156"]},
        {"input": "0\n100\n-5\n12\n", "expected": ["Tổng các ước số là: 28", "S = 9211817190184"]}
    ],
    "Cau2": [
        {"input": "\n", "expected": ["Chuỗi không có ký tự chữ thường.", "Chuỗi đối xứng.", "Chuỗi sau khi chuyển ký tự đầu tiên của mỗi từ thành chữ hoa: "]},
        {"input": "hello World\n", "expected": ["Số ký tự chữ thường trong chuỗi: 9", "Chuỗi không đối xứng.", "Chuỗi sau khi chuyển ký tự đầu tiên của mỗi từ thành chữ hoa: Hello World"]},
        {"input": "ABA\n", "expected": ["Chuỗi không có ký tự chữ thường.", "Chuỗi đối xứng.", "Chuỗi sau khi chuyển ký tự đầu tiên của mỗi từ thành chữ hoa: Aba"]},
        {"input": "xin chào việt nam\n", "expected": ["Số ký tự chữ thường trong chuỗi: 14", "Chuỗi không đối xứng.", "Chuỗi sau khi chuyển ký tự đầu tiên của mỗi từ thành chữ hoa: Xin Chào Việt Nam"]},
        {"input": "level\n", "expected": ["Số ký tự chữ thường trong chuỗi: 5", "Chuỗi đối xứng.", "Chuỗi sau khi chuyển ký tự đầu tiên của mỗi từ thành chữ hoa: Level"]},
        {"input": "ABC 123 !@#\n", "expected": ["Chuỗi không có ký tự chữ thường.", "Chuỗi không đối xứng."]}
    ],
    "Cau3": [
        {"input": "3\n-2\n4\n6\n4\n0\n4\n", "expected": ["Danh sách vừa nhập: [3, -2, 4, 6, 4]", "Các số dương chẵn có trong danh sách: [4, 6, 4]", "4 xuất hiện 2 lần"]},
        {"input": "0\n5\n", "expected": ["Danh sách vừa nhập: []", "Không có số dương chẵn trong danh sách.", "5 không có trong danh sách"]},
        {"input": "-2\n-4\n-6\n0\n-4\n", "expected": ["Danh sách vừa nhập: [-2, -4, -6]", "Không có số dương chẵn trong danh sách.", "-4 xuất hiện 1 lần"]},
        {"input": "2\n4\n6\n0\n2\n", "expected": ["Danh sách vừa nhập: [2, 4, 6]", "Các số dương chẵn có trong danh sách: [2, 4, 6]", "2 xuất hiện 1 lần"]}
    ],
    "Cau4": [
        {"input": "2\nPC01\n8\n512\nDell\n2022\nPC02\n16\n1024\nHP\n2023\nPC01\n", "expected": ["Máy tính có số hiệu PC01 đã được xóa.", "{'PC02': [16, 1024, 'HP', 2023]}"]},
        {"input": "2\nPC01\n8\n512\nDell\n2022\nPC02\n16\n1024\nHP\n2023\nPC02\n", "expected": ["Máy tính có số hiệu PC02 đã được xóa.", "{'PC01': [8, 512, 'Dell', 2022]}"]},
        {"input": "2\nPC01\n8\n512\nDell\n2022\nPC02\n16\n1024\nHP\n2023\nPC99\n", "expected": ["Không có máy tính cần xóa."]},
        {"input": "0\nPC01\n", "expected": ["{}", "Không có máy tính cần xóa."]}
    ],
    "Cau5": [
        {"input": "\n", "expected": ["Mã môn học: 229008", "Tên môn học: Cơ sở dữ liệu", "Số tín chỉ: 3", "Khoa phụ trách: Công nghệ thông tin", "Mã môn học: 224604", "Tên môn học: Tiếng Anh 1", "Số tín chỉ: 2", "Khoa phụ trách: Ngoại ngữ"]}
    ]
}
