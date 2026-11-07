"""Kiểm tra độ mạnh của bộ test (mutation testing đơn giản).

Với mỗi 'đột biến': sao chép 2 folder bài giải sang thư mục tạm, cố tình chèn MỘT lỗi
vào một file rồi chạy test_full.py trên bản sao đó. Bộ test tốt phải THẤT BẠI (diệt được
đột biến). Nếu test vẫn đạt -> đột biến SỐNG SÓT -> test còn lỗ hổng.

Chạy:  python3 run_mutants.py
Bài giải thật KHÔNG bị sửa.
"""
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
D1, D2 = "De1_HOTEN_MSSV", "De2_HOTEN_MSSV"

# (folder, file, đoạn gốc, đoạn lỗi, mô tả lỗi)
MUTANTS = [
    # ---- Đề 1 câu 1
    (D1, "cau1.py", "n > 1500", "n >= 1500", "loại nhầm biên trên n=1500"),
    (D1, "cau1.py", "if tam % 2 != 0:", "if tam % 2 == 0:", "đếm chữ số chẵn thay vì lẻ"),
    (D1, "cau1.py", "s += 1 / (2 * i)", "s += 1 / i", "mẫu số 2i thành i"),
    (D1, "cau1.py", "for i in range(1, n + 1):", "for i in range(1, n):", "S thiếu số hạng cuối"),
    # ---- Đề 1 câu 2
    (D1, "cau2.py", "if i.isupper():", "if i.islower():", "đếm chữ thường thay vì chữ hoa"),
    (D1, "cau2.py", "if s == s[::-1]:", "if s.lower() == s[::-1].lower():", "đối xứng không phân biệt hoa thường"),
    (D1, "cau2.py", "tong += int(i)", "tong += 1", "đếm số chữ số thay vì cộng giá trị"),
    # ---- Đề 1 câu 3
    (D1, "cau3.py", "if i > 0 and i % 2 == 0:", "if i % 2 == 0:", "tính cả số chẵn âm"),
    (D1, "cau3.py", "if x == 0:", "if x <= 0:", "dừng cả khi nhập số âm"),
    # ---- Đề 1 câu 4
    (D1, "cau4.py", "while NamXuatBan > namhientai:", "while NamXuatBan >= namhientai:", "loại nhầm năm hiện tại"),
    (D1, "cau4.py", "[TenSach, TenTacGia, NhaXuatBan, NamXuatBan]", "[TenTacGia, TenSach, NhaXuatBan, NamXuatBan]", "đảo thứ tự giá trị"),
    (D1, "cau4.py", "del tudien[x]", "tudien.clear()", "xóa sạch từ điển thay vì một cuốn"),
    # ---- Đề 1 câu 5
    (D1, "cau5.py", "self.GiaBan = GiaBan", "self.GiaBan = DungLuongPin", "gán nhầm thuộc tính"),
    # ---- Đề 2 câu 1
    (D2, "cau1.py", "n > 99", "n > 100", "nới biên trên thành 100"),
    (D2, "cau1.py", "for i in range(1, n + 1):\n        if n % i == 0:",
     "for i in range(1, n):\n        if n % i == 0:", "tổng ước thiếu chính n"),
    (D2, "cau1.py", "tong += i", "tong += 1", "đếm số ước thay vì tính tổng"),
    (D2, "cau1.py", "s = s + (i ** i)", "s = s + (i ** 2)", "i^i thành i^2"),
    # ---- Đề 2 câu 2
    (D2, "cau2.py", "if i.islower():", "if i.isalpha():", "đếm mọi chữ cái thay vì chữ thường"),
    (D2, "cau2.py", "s = s.title()", "s = s.capitalize()", "chỉ viết hoa chữ đầu cả chuỗi"),
    # ---- Đề 2 câu 3
    (D2, "cau3.py", "if i > 0 and i % 2 == 0:", "if i % 2 == 0:", "tính cả số chẵn âm"),
    (D2, "cau3.py", "dem = ds.count(k)", "dem = 1 if k in ds else 0", "không đếm số lần xuất hiện"),
    # ---- Đề 2 câu 4
    (D2, "cau4.py", "[BoNho, OCung, HangSanXuat, NamSanXuat]", "[OCung, BoNho, HangSanXuat, NamSanXuat]", "đảo bộ nhớ/ổ cứng"),
    (D2, "cau4.py", "del tudien[x]", "tudien.clear()", "xóa sạch từ điển thay vì một máy"),
    # ---- Đề 2 câu 5
    (D2, "cau5.py", 'print("Số tín chỉ:", self.SoTinChi)', 'print("Số tín chỉ:", self.KhoaPhuTrach)', "in nhầm thuộc tính"),
]


def main():
    survivors = []
    for idx, (folder, name, old, new, desc) in enumerate(MUTANTS, 1):
        tmp = tempfile.mkdtemp(prefix="mutant_")
        try:
            for d in (D1, D2):
                shutil.copytree(os.path.join(ROOT, d), os.path.join(tmp, d),
                                ignore=shutil.ignore_patterns("__pycache__"))
            path = os.path.join(tmp, folder, name)
            with open(path, encoding="utf-8") as f:
                text = f.read()
            if old not in text:
                print(f"[{idx:02d}] BỎ QUA - không tìm thấy đoạn gốc trong {folder}/{name}: {old!r}")
                survivors.append((folder, name, desc + " (không áp dụng được)"))
                continue
            with open(path, "w", encoding="utf-8") as f:
                f.write(text.replace(old, new, 1))
            env = dict(os.environ, SOLUTION_ROOT=tmp)
            try:
                r = subprocess.run([sys.executable, os.path.join(HERE, "test_full.py")],
                                   env=env, capture_output=True, text=True,
                                   encoding="utf-8", timeout=180)
                killed = r.returncode != 0
            except subprocess.TimeoutExpired:
                killed = True  # treo = lỗi bị phát hiện
            status = "DIỆT ĐƯỢC" if killed else "SỐNG SÓT !!!"
            print(f"[{idx:02d}] {status:<12} {folder}/{name}: {desc}")
            if not killed:
                survivors.append((folder, name, desc))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    total = len(MUTANTS)
    print(f"\nTổng {total} đột biến: diệt {total - len(survivors)}, sống sót {len(survivors)}")
    for folder, name, desc in survivors:
        print(f"  - {folder}/{name}: {desc}")
    sys.exit(1 if survivors else 0)


if __name__ == "__main__":
    main()
