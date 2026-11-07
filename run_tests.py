"""Chạy thử tất cả các câu của 2 đề bằng input giả lập và kiểm tra output.

Cách chạy:  python3 run_tests.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
passed = 0
failed = 0


def run(folder, cau, inputs):
    path = os.path.join(ROOT, folder, cau)
    r = subprocess.run(
        [sys.executable, "-I", path],
        input="\n".join(inputs) + "\n",
        capture_output=True,
        text=True,
        timeout=10,
    )
    return r.stdout + r.stderr, r.returncode


def check(name, folder, cau, inputs, expected):
    global passed, failed
    out, code = run(folder, cau, inputs)
    missing = [e for e in expected if e not in out]
    if code == 0 and not missing:
        passed += 1
        print(f"[PASS] {name}")
    else:
        failed += 1
        print(f"[FAIL] {name} (exit={code}) thiếu: {missing}")
        print("---- output ----")
        print(out)
        print("----------------")


D1, D2 = "De1_HOTEN_MSSV", "De2_HOTEN_MSSV"


def tong_nghich_dao(n):
    # Cộng tuần tự bằng += (sum() của Python 3.12+ dùng cộng bù nên lệch chữ số cuối)
    s = 0
    for i in range(1, n + 1):
        s += 1 / (2 * i)
    return s


# ---------------- ĐỀ 1 ----------------
check("De1 Câu 1: n=635 (nhập sai 2000, 0 trước), 2 chữ số lẻ",
      D1, "cau1.py", ["2000", "0", "635"],
      ["Số lượng chữ số lẻ là: 2", f"S = {tong_nghich_dao(635)}"])
check("De1 Câu 1: n=3, S = 1/2+1/4+1/6",
      D1, "cau1.py", ["3"],
      ["Số lượng chữ số lẻ là: 1", f"S = {1/2 + 1/4 + 1/6}"])
check("De1 Câu 1: n=1500 (biên trên)",
      D1, "cau1.py", ["1500"], ["Số lượng chữ số lẻ là: 2"])
check("De1 Câu 2: 'Hello 123' (1 hoa, không đối xứng, tổng chữ số 6)",
      D1, "cau2.py", ["Hello 123"],
      ["Số ký tự chữ hoa: 1", "Chuỗi không đối xứng.", "Tổng các chữ số trong chuỗi: 6"])
check("De1 Câu 2: 'a1a' (0 hoa, đối xứng, tổng 1)",
      D1, "cau2.py", ["a1a"],
      ["Chuỗi không có ký tự chữ hoa.", "Chuỗi đối xứng.", "Tổng các chữ số trong chuỗi: 1"])
check("De1 Câu 3: [3,-2,4,6,4], k=4",
      D1, "cau3.py", ["3", "-2", "4", "6", "4", "0", "4"],
      ["Danh sách vừa nhập: [3, -2, 4, 6, 4]",
       "Tổng các số dương chẵn trong danh sách: 14",
       "Số lần xuất hiện của 4 là: 2"])
check("De1 Câu 3: không có dương chẵn, k không tồn tại",
      D1, "cau3.py", ["1", "-4", "3", "0", "9"],
      ["Không có số dương chẵn trong danh sách.", "Không có phần tử 9 trong danh sách"])
check("De1 Câu 4: 2 sách, năm sai 2999 → nhập lại, xóa mã S01",
      D1, "cau4.py",
      ["0", "2",
       "S01", "Python", "An", "NXB A", "2999", "2020",
       "S02", "Java", "Binh", "NXB B", "2018",
       "S01"],
      ["Cuốn sách có mã số S01 đã được xóa.", "'S02': ['Java', 'Binh', 'NXB B', 2018]",
       "Năm xuất bản không hợp lệ"])
check("De1 Câu 4: xóa mã không tồn tại",
      D1, "cau4.py",
      ["1", "S01", "Python", "An", "NXB A", "2020", "S99"],
      ["Không tìm thấy cuốn sách cần xóa."])
check("De1 Câu 5: 2 đối tượng DienThoai",
      D1, "cau5.py", [],
      ["Mã máy: DT01", "Tên máy: iPhone 15 Pro", "Hãng sản xuất: Apple",
       "Dung lượng pin: 3274", "Giá bán: 28990000",
       "Mã máy: DT02", "Tên máy: Galaxy S24 Ultra", "Hãng sản xuất: Samsung",
       "Dung lượng pin: 5000", "Giá bán: 29990000"])

# ---------------- ĐỀ 2 ----------------
check("De2 Câu 1: n=12 → tổng ước 28 (nhập sai 100, 0 trước)",
      D2, "cau1.py", ["100", "0", "12"],
      ["Tổng các ước số là: 28", f"S = {sum(i**i for i in range(1, 13))}"])
check("De2 Câu 1: n=3 → S = 1+4+27 = 32",
      D2, "cau1.py", ["3"], ["Tổng các ước số là: 4", "S = 32"])
check("De2 Câu 1: n=99 (biên trên)",
      D2, "cau1.py", ["99"], ["Tổng các ước số là: 156"])
check("De2 Câu 2: 'hello World' (9 thường, không đối xứng, Title)",
      D2, "cau2.py", ["hello World"],
      ["Số ký tự chữ thường trong chuỗi: 9", "Chuỗi không đối xứng.", "Hello World"])
check("De2 Câu 2: 'ABA' (0 thường, đối xứng)",
      D2, "cau2.py", ["ABA"],
      ["Chuỗi không có ký tự chữ thường.", "Chuỗi đối xứng."])
check("De2 Câu 3: [3,-2,4,6,4], k=4",
      D2, "cau3.py", ["3", "-2", "4", "6", "4", "0", "4"],
      ["Danh sách vừa nhập: [3, -2, 4, 6, 4]",
       "Các số dương chẵn có trong danh sách: [4, 6, 4]",
       "4 xuất hiện 2 lần"])
check("De2 Câu 3: không có dương chẵn, k không tồn tại",
      D2, "cau3.py", ["1", "-4", "3", "0", "9"],
      ["Không có số dương chẵn trong danh sách.", "9 không có trong danh sách"])
check("De2 Câu 4: 2 máy tính, xóa PC01",
      D2, "cau4.py",
      ["2",
       "PC01", "8", "512", "Dell", "2022",
       "PC02", "16", "1024", "HP", "2023",
       "PC01"],
      ["Máy tính có số hiệu PC01 đã được xóa.", "'PC02': [16, 1024, 'HP', 2023]"])
check("De2 Câu 4: xóa số hiệu không tồn tại",
      D2, "cau4.py",
      ["1", "PC01", "8", "512", "Dell", "2022", "PC99"],
      ["Không có máy tính cần xóa."])
check("De2 Câu 5: 2 đối tượng MonHoc",
      D2, "cau5.py", [],
      ["Mã môn học: 229008", "Tên môn học: Cơ sở dữ liệu", "Số tín chỉ: 3",
       "Khoa phụ trách: Công nghệ thông tin",
       "Mã môn học: 224604", "Tên môn học: Tiếng Anh 1", "Số tín chỉ: 2",
       "Khoa phụ trách: Ngoại ngữ"])

print(f"\nKẾT QUẢ: {passed} đạt, {failed} lỗi, tổng {passed + failed} test")
sys.exit(1 if failed else 0)
