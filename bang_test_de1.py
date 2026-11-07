tests = {
    "Cau1": [
        {"input": "1\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 0.5]]},
        {"input": "2\n", "expected": ["Số lượng chữ số lẻ là: 0"], "approx": [["S =", 0.75]]},
        {"input": "3\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 0.9166666666666666]]},
        {"input": "9\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 1.4144841269841268]]},
        {"input": "10\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 1.4644841269841269]]},
        {"input": "99\n", "expected": ["Số lượng chữ số lẻ là: 2"], "approx": [["S =", 2.5886887588198104]]},
        {"input": "100\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 2.5936887588198103]]},
        {"input": "500\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 3.39641171499526]]},
        {"input": "999\n", "expected": ["Số lượng chữ số lẻ là: 3"], "approx": [["S =", 3.7422354302751715]]},
        {"input": "1500\n", "expected": ["Số lượng chữ số lẻ là: 2"], "approx": [["S =", 3.9453846741440652]]},
        {"input": "0\n-10\n1501\n7\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 1.2964285714285713]]},
        {"input": "2026\n100\n", "expected": ["Số lượng chữ số lẻ là: 1"], "approx": [["S =", 2.5936887588198103]]}
    ],
    "Cau2": [
        {"input": "\n", "expected": ["Chuỗi không có ký tự chữ hoa.", "Chuỗi đối xứng.", "Tổng các chữ số trong chuỗi: 0"]},
        {"input": "   \n", "expected": ["Chuỗi không có ký tự chữ hoa.", "Chuỗi đối xứng.", "Tổng các chữ số trong chuỗi: 0"]},
        {"input": "Hello 123\n", "expected": ["Số ký tự chữ hoa: 1", "Chuỗi không đối xứng.", "Tổng các chữ số trong chuỗi: 6"]},
        {"input": "a1a\n", "expected": ["Chuỗi không có ký tự chữ hoa.", "Chuỗi đối xứng.", "Tổng các chữ số trong chuỗi: 1"]},
        {"input": "ABBA\n", "expected": ["Số ký tự chữ hoa: 4", "Chuỗi đối xứng.", "Tổng các chữ số trong chuỗi: 0"]},
        {"input": "Python 2026\n", "expected": ["Số ký tự chữ hoa: 1", "Chuỗi không đối xứng.", "Tổng các chữ số trong chuỗi: 10"]},
        {"input": "12321\n", "expected": ["Chuỗi không có ký tự chữ hoa.", "Chuỗi đối xứng.", "Tổng các chữ số trong chuỗi: 9"]},
        {"input": "Lập Trình Python\n", "expected": ["Số ký tự chữ hoa: 3", "Chuỗi không đối xứng.", "Tổng các chữ số trong chuỗi: 0"]}
    ],
    "Cau3": [
        {"input": "3\n-2\n4\n6\n4\n0\n4\n", "expected": ["Danh sách vừa nhập: [3, -2, 4, 6, 4]", "Tổng các số dương chẵn trong danh sách: 14", "Số lần xuất hiện của 4 là: 2"]},
        {"input": "0\n5\n", "expected": ["Danh sách vừa nhập: []", "Không có số dương chẵn trong danh sách.", "Không có phần tử 5 trong danh sách"]},
        {"input": "-2\n-4\n-6\n0\n-4\n", "expected": ["Danh sách vừa nhập: [-2, -4, -6]", "Không có số dương chẵn trong danh sách.", "Số lần xuất hiện của -4 là: 1"]},
        {"input": "1\n2\n3\n4\n5\n6\n0\n2\n", "expected": ["Danh sách vừa nhập: [1, 2, 3, 4, 5, 6]", "Tổng các số dương chẵn trong danh sách: 12", "Số lần xuất hiện của 2 là: 1"]},
        {"input": "7\n9\n11\n0\n8\n", "expected": ["Danh sách vừa nhập: [7, 9, 11]", "Không có số dương chẵn trong danh sách.", "Không có phần tử 8 trong danh sách"]}
    ],
    "Cau4": [
        {"input": "2\nS01\nPython\nAn\nNXB A\n2020\nS02\nJava\nBình\nNXB B\n2018\nS01\n", "expected": ["Cuốn sách có mã số S01 đã được xóa.", "{'S02': ['Java', 'Bình', 'NXB B', 2018]}"]},
        {"input": "2\nS01\nPython\nAn\nNXB A\n2020\nS02\nJava\nBình\nNXB B\n2018\nS02\n", "expected": ["Cuốn sách có mã số S02 đã được xóa.", "{'S01': ['Python', 'An', 'NXB A', 2020]}"]},
        {"input": "1\nS01\nA\nB\nC\n2100\n2022\nS01\n", "expected": ["Cuốn sách có mã số S01 đã được xóa."]},
        {"input": "1\nS01\nA\nB\nC\n2020\nS99\n", "expected": ["Không tìm thấy cuốn sách cần xóa."]}
    ],
    "Cau5": [
        {"input": "\n", "expected": ["Mã máy: DT01", "Tên máy: iPhone 15 Pro", "Hãng sản xuất: Apple", "Dung lượng pin: 3274", "Giá bán: 28990000", "Mã máy: DT02", "Tên máy: Galaxy S24 Ultra", "Hãng sản xuất: Samsung", "Dung lượng pin: 5000", "Giá bán: 29990000"]}
    ]
}
