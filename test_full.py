"""Bộ test đầy đủ cho 2 đề Python (De1_HOTEN_MSSV, De2_HOTEN_MSSV).

Chạy:
    cd test_de
    python3 test_full.py            (hoặc: python3 -m unittest -v test_full)

Đặc điểm so với run_tests.py cũ:
  * Chạy chương trình TRONG tiến trình với input() giả lập -> kiểm tra được
    số lần chương trình gọi input(), có đọc thiếu / đọc thừa input hay không.
  * So khớp CHÍNH XÁC từng dòng output (không dùng 'in' trên chuỗi dài).
  * Gọi trực tiếp các hàm con (DemChuSoLe, S, TongUocSo) trên toàn bộ miền giá trị
    và so với bản tham chiếu viết độc lập.
  * Test ngẫu nhiên có seed cố định (lặp lại được).
  * Kiểm tra từ điển / lớp: kiểu dữ liệu, thứ tự giá trị, ghi đè khóa trùng,
    phân biệt hoa thường, xóa phần tử duy nhất, ...
  * Có thể trỏ sang thư mục khác bằng biến môi trường SOLUTION_ROOT
    (run_mutants.py dùng cách này).

Yêu cầu tên: hàm DemChuSoLe, S (Đề 1 câu 1); TongUocSo, S (Đề 2 câu 1);
lớp DienThoai (+ thongtindienthoai), MonHoc (+ thongtinmonhoc).
"""
import ast
import builtins
import contextlib
import datetime
import inspect
import io
import math
import os
import random
import runpy
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("SOLUTION_ROOT") or os.path.dirname(HERE)
D1 = os.path.join(ROOT, "De1_HOTEN_MSSV")
D2 = os.path.join(ROOT, "De2_HOTEN_MSSV")
CUR_YEAR = datetime.datetime.now().year


# ======================================================================
# Hạ tầng chạy chương trình với input giả lập
# ======================================================================
class InputExhausted(Exception):
    """Chương trình đòi nhập nhiều hơn số input test cung cấp."""


class Result:
    def __init__(self, g, out, prompts, left):
        self.g = g              # globals của chương trình sau khi chạy
        self.out = out          # toàn bộ stdout
        self.prompts = prompts  # danh sách prompt của từng lần gọi input()
        self.left = left        # input còn dư, chưa được dùng

    @property
    def lines(self):
        return self.out.splitlines()

    @property
    def calls(self):
        return len(self.prompts)


def run(folder, name, inputs=()):
    queue = [str(x) for x in inputs]
    prompts = []

    def fake_input(prompt=""):
        prompts.append(str(prompt))
        if not queue:
            raise InputExhausted(
                f"{name}: chương trình đòi nhập thêm ở lần {len(prompts)} (prompt={prompt!r})")
        return queue.pop(0)

    out = io.StringIO()
    real_input = builtins.input
    builtins.input = fake_input
    try:
        with contextlib.redirect_stdout(out):
            g = runpy.run_path(os.path.join(folder, name))
    finally:
        builtins.input = real_input
    return Result(g, out.getvalue(), prompts, queue)


def capture(fn, *args, **kwargs):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue().splitlines()


def dict_lines(res):
    """Các dòng output bắt đầu bằng '{' được parse thành dict."""
    return [ast.literal_eval(line) for line in res.lines if line.startswith("{")]


def norm(d):
    """Chấp nhận giá trị là list/tuple hoặc dict con (đề cho phép 'cách khác')."""
    return {k: (list(v.values()) if isinstance(v, dict) else list(v)) for k, v in d.items()}


def parse_float_line(lines, prefix):
    for line in lines:
        if line.startswith(prefix):
            return float(line[len(prefix):])
    raise AssertionError(f"Không thấy dòng bắt đầu bằng {prefix!r} trong output: {lines}")


class Base(unittest.TestCase):
    def consumed(self, res):
        self.assertEqual(
            res.left, [],
            "Chương trình chưa dùng hết input (đọc ít hơn mong đợi, dừng sớm hoặc rẽ nhánh sai)")


# ======================================================================
# Bản tham chiếu độc lập (viết khác cách làm của bài giải)
# ======================================================================
def ref_odd_digits(n):
    return sum(1 for ch in str(n) if int(ch) % 2 == 1)


def ref_s1(n):  # 1/2 + 1/4 + ... + 1/(2n)
    return math.fsum(1 / (2 * i) for i in range(1, n + 1))


def ref_divisor_sum(n):
    return sum(d for d in range(1, n + 1) if n % d == 0)


def ref_s2(n):  # 1 + 2^2 + ... + n^n
    return sum(i ** i for i in range(1, n + 1))


# ======================================================================
# Cấu trúc bài thi
# ======================================================================
class TestStructure(unittest.TestCase):
    def test_moi_folder_co_dung_5_file(self):
        for folder in (D1, D2):
            with self.subTest(folder=os.path.basename(folder)):
                files = sorted(f for f in os.listdir(folder) if f.endswith(".py"))
                self.assertEqual(files, [f"cau{i}.py" for i in range(1, 6)])

    def test_bien_dich_khong_loi(self):
        for folder in (D1, D2):
            for i in range(1, 6):
                path = os.path.join(folder, f"cau{i}.py")
                with self.subTest(path=path):
                    with open(path, encoding="utf-8") as f:
                        compile(f.read(), path, "exec")


# ======================================================================
# ĐỀ 1 - CÂU 1
# ======================================================================
class De1Cau1(Base):
    F = "cau1.py"

    def test_DemChuSoLe_toan_mien(self):
        fn = run(D1, self.F, ["1"]).g["DemChuSoLe"]
        for n in list(range(0, 1501)) + [10 ** 6, 13579, 24680, 1111111, 9876543210]:
            self.assertEqual(fn(n), ref_odd_digits(n), f"n={n}")

    def test_DemChuSoLe_gia_tri_dac_biet(self):
        fn = run(D1, self.F, ["1"]).g["DemChuSoLe"]
        self.assertEqual(fn(635), 2)       # ví dụ trong đề
        self.assertEqual(fn(2468), 0)      # toàn chữ số chẵn
        self.assertEqual(fn(1357), 4)      # toàn chữ số lẻ
        self.assertEqual(fn(1000), 1)      # có chữ số 0
        self.assertEqual(fn(9), 1)

    def test_S_toan_mien(self):
        fn = run(D1, self.F, ["1"]).g["S"]
        for n in range(1, 1501):
            self.assertTrue(math.isclose(fn(n), ref_s1(n), rel_tol=1e-12, abs_tol=1e-12), f"n={n}")

    def test_S_gia_tri_dac_biet(self):
        fn = run(D1, self.F, ["1"]).g["S"]
        self.assertEqual(fn(1), 0.5)
        self.assertAlmostEqual(fn(2), 0.75)
        self.assertAlmostEqual(fn(3), 1 / 2 + 1 / 4 + 1 / 6)
        self.assertEqual(fn(0), 0)

    def test_S_tang_nghiem_ngat(self):
        fn = run(D1, self.F, ["1"]).g["S"]
        prev = 0
        for n in range(1, 301):
            cur = fn(n)
            self.assertGreater(cur, prev, f"n={n}")
            prev = cur

    def test_chuong_trinh_nhieu_gia_tri_n(self):
        for n in [1, 2, 9, 10, 99, 100, 635, 999, 1000, 1357, 1499, 1500]:
            with self.subTest(n=n):
                res = run(D1, self.F, [n])
                self.consumed(res)
                self.assertEqual(res.calls, 1)
                self.assertEqual(len(res.lines), 2)
                self.assertEqual(res.lines[0], f"Số lượng chữ số lẻ là: {ref_odd_digits(n)}")
                s = parse_float_line(res.lines, "S = ")
                self.assertTrue(math.isclose(s, ref_s1(n), rel_tol=1e-12))

    def test_nhap_lai_khi_ngoai_doan(self):
        res = run(D1, self.F, [0, -5, 1501, 99999, 1])
        self.consumed(res)
        self.assertEqual(res.calls, 5)
        self.assertEqual(res.lines[0], "Số lượng chữ số lẻ là: 1")
        self.assertEqual(parse_float_line(res.lines, "S = "), 0.5)

    def test_bien_duoc_chap_nhan_ngay(self):
        for n in (1, 1500):
            with self.subTest(n=n):
                res = run(D1, self.F, [n])
                self.assertEqual(res.calls, 1)
                self.consumed(res)

    def test_bien_ngoai_bi_tu_choi(self):
        for bad in (0, 1501, -1, 2 ** 31):
            with self.subTest(bad=bad):
                res = run(D1, self.F, [bad, 7])
                self.assertEqual(res.calls, 2)
                self.assertEqual(res.lines[0], "Số lượng chữ số lẻ là: 1")


# ======================================================================
# ĐỀ 1 - CÂU 2
# ======================================================================
class De1Cau2(Base):
    F = "cau2.py"

    def expected(self, s):
        up = sum(1 for c in s if c.isupper())
        first = "Chuỗi không có ký tự chữ hoa." if up == 0 else f"Số ký tự chữ hoa: {up}"
        sym = "Chuỗi đối xứng." if s == s[::-1] else "Chuỗi không đối xứng."
        tot = sum(int(c) for c in s if c.isdigit())
        return [first, sym, f"Tổng các chữ số trong chuỗi: {tot}"]

    def check(self, s):
        res = run(D1, self.F, [s])
        self.consumed(res)
        self.assertEqual(res.calls, 1)
        self.assertEqual(res.lines, self.expected(s))

    def test_bang_gia_tri(self):
        cases = ["", " ", "Hello 123", "a1a", "ABBA", "Abba", "racecar", "A man a plan",
                 "ĐÀ NẴNG 2024", "12321", "9", "aBcDeF0Z", "Aa", "aA", "   x   ", "99 99",
                 "Python3.13", "Z", "z", "0", "1a2b3c4d5e"]
        for s in cases:
            with self.subTest(s=s):
                self.check(s)

    def test_gia_tri_cung_ngat(self):
        self.assertEqual(self.expected("Hello 123"),
                         ["Số ký tự chữ hoa: 1", "Chuỗi không đối xứng.",
                          "Tổng các chữ số trong chuỗi: 6"])
        res = run(D1, self.F, ["ĐÀ NẴNG 2024"])
        self.assertEqual(res.lines[0], "Số ký tự chữ hoa: 6")        # tiếng Việt có dấu
        self.assertEqual(res.lines[2], "Tổng các chữ số trong chuỗi: 8")

    def test_phan_biet_hoa_thuong_khi_doi_xung(self):
        self.assertIn("Chuỗi không đối xứng.", run(D1, self.F, ["Aa"]).lines)
        self.assertIn("Chuỗi không đối xứng.", run(D1, self.F, ["Abba"]).lines)
        self.assertIn("Chuỗi đối xứng.", run(D1, self.F, ["abba"]).lines)

    def test_chuoi_rong(self):
        res = run(D1, self.F, [""])
        self.assertEqual(res.lines, ["Chuỗi không có ký tự chữ hoa.", "Chuỗi đối xứng.",
                                     "Tổng các chữ số trong chuỗi: 0"])

    def test_ngau_nhien(self):
        rng = random.Random(2024)
        alphabet = "aAbB1 29ÀàĐđ"
        for _ in range(200):
            s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            with self.subTest(s=s):
                self.check(s)

    def test_chuoi_doi_xung_ngau_nhien(self):
        rng = random.Random(11)
        for _ in range(50):
            half = "".join(rng.choice("aAb12 ") for _ in range(rng.randint(0, 6)))
            s = half + (rng.choice(["", "x", "7"])) + half[::-1]
            with self.subTest(s=s):
                self.assertIn("Chuỗi đối xứng.", run(D1, self.F, [s]).lines)


# ======================================================================
# ĐỀ 1 - CÂU 3
# ======================================================================
class De1Cau3(Base):
    F = "cau3.py"

    def expected(self, lst, k):
        pe = sum(x for x in lst if x > 0 and x % 2 == 0)
        has_pe = any(x > 0 and x % 2 == 0 for x in lst)
        c = lst.count(k)
        return [
            f"Danh sách vừa nhập: {lst}",
            f"Tổng các số dương chẵn trong danh sách: {pe}" if has_pe
            else "Không có số dương chẵn trong danh sách.",
            f"Số lần xuất hiện của {k} là: {c}" if c else f"Không có phần tử {k} trong danh sách",
        ]

    def check(self, lst, k):
        res = run(D1, self.F, list(lst) + [0, k])
        self.consumed(res)
        self.assertEqual(res.calls, len(lst) + 2)
        self.assertEqual(res.lines, self.expected(list(lst), k))

    def test_bang_gia_tri(self):
        cases = [
            ([3, -2, 4, 6, 4], 4),
            ([], 5),
            ([-2, -4, -6], -4),
            ([2], 2),
            ([7, 7, 7, 7], 7),
            (list(range(1, 11)), 11),
            (list(range(1, 101)), 50),
            ([0 + 1], 0),                 # k = 0 không bao giờ có trong danh sách
            ([-1, -3, 5], 5),
            ([10, -10, 10, -10], -10),
            ([1], 1),
            ([2, 2, 2], 2),
        ]
        for lst, k in cases:
            with self.subTest(lst=lst, k=k):
                self.check(lst, k)

    def test_gia_tri_cung_ngat(self):
        self.assertEqual(self.expected([3, -2, 4, 6, 4], 4)[1],
                         "Tổng các số dương chẵn trong danh sách: 14")
        self.assertEqual(self.expected(list(range(1, 101)), 50)[1],
                         "Tổng các số dương chẵn trong danh sách: 2550")

    def test_dung_dung_khi_nhap_0(self):
        # 5, 0 -> danh sách [5]; số 7 sau đó là giá trị k chứ KHÔNG phải phần tử danh sách
        res = run(D1, self.F, [5, 0, 7])
        self.consumed(res)
        self.assertEqual(res.calls, 3)
        self.assertEqual(res.lines[0], "Danh sách vừa nhập: [5]")
        self.assertEqual(res.lines[2], "Không có phần tử 7 trong danh sách")

    def test_so_am_chan_khong_tinh(self):
        res = run(D1, self.F, [-2, -8, 0, 1])
        self.assertEqual(res.lines[1], "Không có số dương chẵn trong danh sách.")

    def test_ngau_nhien(self):
        rng = random.Random(99)
        for _ in range(150):
            lst = [rng.choice([v for v in range(-9, 10) if v != 0])
                   for _ in range(rng.randint(0, 15))]
            k = rng.randint(-9, 9)
            with self.subTest(lst=lst, k=k):
                self.check(lst, k)

    def test_danh_sach_lon(self):
        lst = [(i % 17) - 8 or 1 for i in range(2000)]
        self.check(lst, 3)


# ======================================================================
# ĐỀ 1 - CÂU 4
# ======================================================================
def d1_run(n_inputs, books, delete):
    seq = list(n_inputs)
    for ma, ten, tg, nxb, nam in books:
        seq += [ma, ten, tg, nxb]
        seq += list(nam) if isinstance(nam, (list, tuple)) else [nam]
    seq.append(delete)
    return run(D1, "cau4.py", seq)


def d1_expected(books):
    exp = {}
    for ma, ten, tg, nxb, nam in books:
        year = nam[-1] if isinstance(nam, (list, tuple)) else nam
        exp[ma] = [ten, tg, nxb, int(year)]
    return exp


class De1Cau4(Base):
    def check(self, books, delete, n_inputs=None):
        n_inputs = n_inputs if n_inputs is not None else [len(books)]
        res = d1_run(n_inputs, books, delete)
        self.consumed(res)
        before = d1_expected(books)
        after = {k: v for k, v in before.items() if k != delete}
        self.assertEqual([norm(d) for d in dict_lines(res)], [before, after])
        found = f"Cuốn sách có mã số {delete} đã được xóa."
        missing = "Không tìm thấy cuốn sách cần xóa."
        self.assertIn(found if delete in before else missing, res.lines)
        self.assertNotIn(missing if delete in before else found, res.lines)
        self.assertEqual(len(res.lines), 3)
        return res

    B = [("S01", "Python", "An", "NXB A", 2020), ("S02", "Java", "Bình", "NXB B", 2018)]

    def test_xoa_sach_ton_tai(self):
        self.check(self.B, "S01")
        self.check(self.B, "S02")

    def test_xoa_sach_khong_ton_tai(self):
        self.check(self.B, "S99")
        self.check(self.B, "")

    def test_n_khong_hop_le_phai_nhap_lai(self):
        self.check(self.B, "S01", n_inputs=[0, -3, 2])

    def test_nam_xuat_ban_bang_nam_hien_tai_duoc_chap_nhan(self):
        self.check([("S01", "A", "B", "C", CUR_YEAR)], "S01")

    def test_nam_xuat_ban_tuong_lai_phai_nhap_lai(self):
        books = [("S01", "A", "B", "C", [CUR_YEAR + 1, CUR_YEAR + 100, CUR_YEAR])]
        res = self.check(books, "S01")
        self.assertEqual(res.calls, 1 + 4 + 3 + 1)

    def test_nam_xuat_ban_la_so_nguyen(self):
        res = d1_run([1], [("S01", "A", "B", "C", "1999")], "x")
        year = norm(dict_lines(res)[0])["S01"][3]
        self.assertIs(type(year), int)

    def test_nam_xuat_ban_cu(self):
        self.check([("S01", "A", "B", "C", 1900), ("S02", "A", "B", "C", 1)], "S02")

    def test_ma_trung_bi_ghi_de(self):
        books = [("S01", "Cũ", "A", "X", 2000), ("S01", "Mới", "B", "Y", 2001)]
        res = self.check(books, "S01")
        self.assertEqual(norm(dict_lines(res)[0]), {"S01": ["Mới", "B", "Y", 2001]})

    def test_phan_biet_hoa_thuong_ma_sach(self):
        res = self.check([("S01", "A", "B", "C", 2000)], "s01")
        self.assertEqual(len(dict_lines(res)[1]), 1)

    def test_xoa_cuon_duy_nhat(self):
        res = self.check([("S01", "A", "B", "C", 2000)], "S01")
        self.assertEqual(dict_lines(res)[1], {})
        self.assertIn("{}", res.lines)

    def test_tieng_viet_co_dau(self):
        books = [("MS-001", "Lập trình Python", "Nguyễn Văn Ánh", "NXB Giáo Dục", 2022),
                 ("MS-002", "Cơ sở dữ liệu", "Trần Thị Bích", "NXB Đại học Quốc gia", 2019)]
        self.check(books, "MS-002")

    def test_ma_co_khoang_trang(self):
        self.check([("S 01", "A B", "C D", "E F", 2000)], "S 01")

    def test_nhieu_cuon_sach_ngau_nhien(self):
        rng = random.Random(7)
        books = [(f"S{i:03d}", f"Sách {i}", f"TG{rng.randint(1, 9)}", f"NXB{rng.randint(1, 5)}",
                  rng.randint(1950, CUR_YEAR)) for i in range(30)]
        for code in ("S000", "S015", "S029", "S030"):
            with self.subTest(code=code):
                self.check(books, code)


# ======================================================================
# ĐỀ 1 - CÂU 5
# ======================================================================
class De1Cau5(Base):
    def test_output_chinh_xac(self):
        res = run(D1, "cau5.py")
        self.assertEqual(res.lines, [
            "Mã máy: DT01", "Tên máy: iPhone 15 Pro", "Hãng sản xuất: Apple",
            "Dung lượng pin: 3274", "Giá bán: 28990000",
            "Mã máy: DT02", "Tên máy: Galaxy S24 Ultra", "Hãng sản xuất: Samsung",
            "Dung lượng pin: 5000", "Giá bán: 29990000",
        ])
        self.assertEqual(res.calls, 0)

    def test_chu_ky_ham_khoi_tao(self):
        cls = run(D1, "cau5.py").g["DienThoai"]
        self.assertEqual(list(inspect.signature(cls.__init__).parameters),
                         ["self", "MaMay", "TenMay", "HangSanXuat", "DungLuongPin", "GiaBan"])

    def test_thuoc_tinh_va_phuong_thuc(self):
        cls = run(D1, "cau5.py").g["DienThoai"]
        a = cls("A1", "Máy A", "Hãng A", 1000, 1)
        b = cls("B2", "Máy B", "Hãng B", 2000, 2)
        self.assertEqual(vars(a), {"MaMay": "A1", "TenMay": "Máy A", "HangSanXuat": "Hãng A",
                                   "DungLuongPin": 1000, "GiaBan": 1})
        self.assertEqual(vars(b), {"MaMay": "B2", "TenMay": "Máy B", "HangSanXuat": "Hãng B",
                                   "DungLuongPin": 2000, "GiaBan": 2})
        self.assertEqual(capture(a.thongtindienthoai), [
            "Mã máy: A1", "Tên máy: Máy A", "Hãng sản xuất: Hãng A",
            "Dung lượng pin: 1000", "Giá bán: 1"])
        # tạo b không được làm đổi a
        self.assertEqual(a.MaMay, "A1")

    def test_goi_bang_tham_so_ten(self):
        cls = run(D1, "cau5.py").g["DienThoai"]
        o = cls(GiaBan=5, DungLuongPin=4, HangSanXuat="H", TenMay="T", MaMay="M")
        self.assertEqual(capture(o.thongtindienthoai), [
            "Mã máy: M", "Tên máy: T", "Hãng sản xuất: H", "Dung lượng pin: 4", "Giá bán: 5"])

    def test_kieu_du_lieu_giu_nguyen(self):
        cls = run(D1, "cau5.py").g["DienThoai"]
        o = cls("X", "Y", "Z", 3274, 28990000)
        self.assertIs(type(o.DungLuongPin), int)
        self.assertIs(type(o.GiaBan), int)


# ======================================================================
# ĐỀ 2 - CÂU 1
# ======================================================================
class De2Cau1(Base):
    F = "cau1.py"

    def test_TongUocSo_toan_mien(self):
        fn = run(D2, self.F, ["1"]).g["TongUocSo"]
        for n in range(1, 100):
            self.assertEqual(fn(n), ref_divisor_sum(n), f"n={n}")

    def test_TongUocSo_gia_tri_cung(self):
        fn = run(D2, self.F, ["1"]).g["TongUocSo"]
        known = {1: 1, 6: 12, 12: 28, 28: 56, 60: 168, 64: 127, 97: 98, 99: 156}
        for n, v in known.items():
            self.assertEqual(fn(n), v, f"n={n}")

    def test_S_chinh_xac_toan_mien(self):
        fn = run(D2, self.F, ["1"]).g["S"]
        for n in range(1, 100):
            v = fn(n)
            self.assertEqual(v, ref_s2(n), f"n={n}")
            self.assertIs(type(v), int, f"n={n}")

    def test_S_gia_tri_cung(self):
        fn = run(D2, self.F, ["1"]).g["S"]
        for n, v in {1: 1, 2: 5, 3: 32, 4: 288, 5: 3413}.items():
            self.assertEqual(fn(n), v)
        self.assertEqual(fn(0), 0)

    def test_chuong_trinh_nhieu_gia_tri_n(self):
        for n in [1, 2, 6, 12, 28, 50, 60, 64, 97, 98, 99]:
            with self.subTest(n=n):
                res = run(D2, self.F, [n])
                self.consumed(res)
                self.assertEqual(res.calls, 1)
                self.assertEqual(res.lines, [f"Tổng các ước số là: {ref_divisor_sum(n)}",
                                             f"S = {ref_s2(n)}"])

    def test_nhap_lai_khi_ngoai_doan(self):
        res = run(D2, self.F, [0, 100, -1, 1000, 99])
        self.consumed(res)
        self.assertEqual(res.calls, 5)
        self.assertEqual(res.lines[0], "Tổng các ước số là: 156")

    def test_bien(self):
        for n in (1, 99):
            with self.subTest(n=n):
                res = run(D2, self.F, [n])
                self.assertEqual(res.calls, 1)
                self.consumed(res)
        res = run(D2, self.F, [100, 1])
        self.assertEqual(res.calls, 2)
        self.assertEqual(res.lines[0], "Tổng các ước số là: 1")


# ======================================================================
# ĐỀ 2 - CÂU 2
# ======================================================================
class De2Cau2(Base):
    F = "cau2.py"

    def expected(self, s):
        low = sum(1 for c in s if c.islower())
        first = ("Chuỗi không có ký tự chữ thường." if low == 0
                 else f"Số ký tự chữ thường trong chuỗi: {low}")
        sym = "Chuỗi đối xứng." if s == s[::-1] else "Chuỗi không đối xứng."
        third = "Chuỗi sau khi chuyển ký tự đầu tiên của mỗi từ thành chữ hoa: " + s.title()
        return [first, sym, third]

    def check(self, s):
        res = run(D2, self.F, [s])
        self.consumed(res)
        self.assertEqual(res.calls, 1)
        self.assertEqual(res.lines, self.expected(s))

    def test_bang_gia_tri(self):
        cases = ["hello World", "ABA", "", " ", "xin chào việt nam", "hELLO wORLD", "123 abc",
                 "ĐÀ nẵng", "a", "abba", "Abba", "  hai  khoang  trang  ", "mixed123case",
                 "ABC", "abc", "Aa", "level", "12321", "x y z"]
        for s in cases:
            with self.subTest(s=s):
                self.check(s)

    def test_gia_tri_cung_ngat(self):
        res = run(D2, self.F, ["xin chào việt nam"])
        self.assertEqual(res.lines[0], "Số ký tự chữ thường trong chuỗi: 14")
        self.assertTrue(res.lines[2].endswith(": Xin Chào Việt Nam"))
        res = run(D2, self.F, ["hello World"])
        self.assertEqual(res.lines[0], "Số ký tự chữ thường trong chuỗi: 9")
        self.assertTrue(res.lines[2].endswith(": Hello World"))

    def test_chi_dem_chu_thuong_khong_dem_ky_tu_khac(self):
        res = run(D2, self.F, ["ABC 123 !@#"])
        self.assertEqual(res.lines[0], "Chuỗi không có ký tự chữ thường.")
        res = run(D2, self.F, ["aB1 c!"])
        self.assertEqual(res.lines[0], "Số ký tự chữ thường trong chuỗi: 2")

    def test_ngau_nhien(self):
        rng = random.Random(2025)
        alphabet = "aAbB1 29ÀàĐđ"
        for _ in range(200):
            s = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 12)))
            with self.subTest(s=s):
                self.check(s)


# ======================================================================
# ĐỀ 2 - CÂU 3
# ======================================================================
class De2Cau3(Base):
    F = "cau3.py"

    def expected(self, lst, k):
        pe = [x for x in lst if x > 0 and x % 2 == 0]
        c = lst.count(k)
        return [
            f"Danh sách vừa nhập: {lst}",
            f"Các số dương chẵn có trong danh sách: {pe}" if pe
            else "Không có số dương chẵn trong danh sách.",
            f"{k} xuất hiện {c} lần" if c else f"{k} không có trong danh sách",
        ]

    def check(self, lst, k):
        res = run(D2, self.F, list(lst) + [0, k])
        self.consumed(res)
        self.assertEqual(res.calls, len(lst) + 2)
        self.assertEqual(res.lines, self.expected(list(lst), k))

    def test_bang_gia_tri(self):
        cases = [
            ([3, -2, 4, 6, 4], 4), ([], 5), ([-2, -4, -6], -4), ([2], 2), ([7, 7, 7, 7], 7),
            (list(range(1, 11)), 11), (list(range(1, 101)), 50), ([1], 0), ([-1, -3, 5], 5),
            ([10, -10, 10, -10], -10), ([6, 4, 2], 2), ([8, 8], 8),
        ]
        for lst, k in cases:
            with self.subTest(lst=lst, k=k):
                self.check(lst, k)

    def test_giu_thu_tu_nhap(self):
        res = run(D2, self.F, [8, 2, 6, 4, 0, 2])
        self.assertEqual(res.lines[1], "Các số dương chẵn có trong danh sách: [8, 2, 6, 4]")

    def test_giu_so_trung(self):
        res = run(D2, self.F, [4, 4, 4, 0, 4])
        self.assertEqual(res.lines[1], "Các số dương chẵn có trong danh sách: [4, 4, 4]")
        self.assertEqual(res.lines[2], "4 xuất hiện 3 lần")

    def test_dung_dung_khi_nhap_0(self):
        res = run(D2, self.F, [5, 0, 7])
        self.consumed(res)
        self.assertEqual(res.calls, 3)
        self.assertEqual(res.lines[0], "Danh sách vừa nhập: [5]")
        self.assertEqual(res.lines[2], "7 không có trong danh sách")

    def test_ngau_nhien(self):
        rng = random.Random(100)
        for _ in range(150):
            lst = [rng.choice([v for v in range(-9, 10) if v != 0])
                   for _ in range(rng.randint(0, 15))]
            k = rng.randint(-9, 9)
            with self.subTest(lst=lst, k=k):
                self.check(lst, k)


# ======================================================================
# ĐỀ 2 - CÂU 4
# ======================================================================
def d2_run(n, pcs, delete):
    seq = [n]
    for so_hieu, bo_nho, o_cung, hang, nam in pcs:
        seq += [so_hieu, bo_nho, o_cung, hang, nam]
    seq.append(delete)
    return run(D2, "cau4.py", seq)


def d2_expected(pcs):
    exp = {}
    for so_hieu, bo_nho, o_cung, hang, nam in pcs:
        exp[so_hieu] = [int(bo_nho), int(o_cung), hang, int(nam)]
    return exp


class De2Cau4(Base):
    def check(self, pcs, delete, n=None):
        n = len(pcs) if n is None else n
        res = d2_run(n, pcs, delete)
        self.consumed(res)
        before = d2_expected(pcs)
        after = {k: v for k, v in before.items() if k != delete}
        self.assertEqual([norm(d) for d in dict_lines(res)], [before, after])
        found = f"Máy tính có số hiệu {delete} đã được xóa."
        missing = "Không có máy tính cần xóa."
        self.assertIn(found if delete in before else missing, res.lines)
        self.assertNotIn(missing if delete in before else found, res.lines)
        self.assertEqual(len(res.lines), 3)
        return res

    P = [("PC01", 8, 512, "Dell", 2022), ("PC02", 16, 1024, "HP", 2023)]

    def test_xoa_may_ton_tai(self):
        self.check(self.P, "PC01")
        self.check(self.P, "PC02")

    def test_xoa_may_khong_ton_tai(self):
        self.check(self.P, "PC99")
        self.check(self.P, "")

    def test_khong_co_may_nao(self):
        res = self.check([], "PC01", n=0)
        self.assertEqual(res.calls, 2)
        self.assertEqual(dict_lines(res), [{}, {}])

    def test_kieu_du_lieu_so_nguyen(self):
        res = d2_run(1, [("PC01", "08", "0512", "Dell", "2022")], "x")
        v = norm(dict_lines(res)[0])["PC01"]
        self.assertEqual(v, [8, 512, "Dell", 2022])
        self.assertTrue(all(type(x) is int for x in (v[0], v[1], v[3])))

    def test_so_hieu_trung_bi_ghi_de(self):
        pcs = [("PC01", 4, 128, "Acer", 2015), ("PC01", 32, 2048, "Asus", 2024)]
        res = self.check(pcs, "PC01")
        self.assertEqual(norm(dict_lines(res)[0]), {"PC01": [32, 2048, "Asus", 2024]})

    def test_phan_biet_hoa_thuong(self):
        res = self.check([("PC01", 8, 512, "Dell", 2022)], "pc01")
        self.assertEqual(len(dict_lines(res)[1]), 1)

    def test_xoa_may_duy_nhat(self):
        res = self.check([("PC01", 8, 512, "Dell", 2022)], "PC01")
        self.assertEqual(dict_lines(res)[1], {})

    def test_chi_xoa_dung_mot_may(self):
        pcs = [(f"PC{i:02d}", 8, 256, "Dell", 2020) for i in range(5)]
        res = self.check(pcs, "PC02")
        self.assertEqual(len(dict_lines(res)[1]), 4)

    def test_nhieu_may_ngau_nhien(self):
        rng = random.Random(8)
        pcs = [(f"PC{i:03d}", rng.choice([4, 8, 16, 32]), rng.choice([256, 512, 1024]),
                rng.choice(["Dell", "HP", "Asus", "Lenovo"]), rng.randint(2000, 2025))
               for i in range(40)]
        for code in ("PC000", "PC020", "PC039", "PC040"):
            with self.subTest(code=code):
                self.check(pcs, code)


# ======================================================================
# ĐỀ 2 - CÂU 5
# ======================================================================
class De2Cau5(Base):
    def test_output_chinh_xac(self):
        res = run(D2, "cau5.py")
        self.assertEqual(res.lines, [
            "Mã môn học: 229008", "Tên môn học: Cơ sở dữ liệu", "Số tín chỉ: 3",
            "Khoa phụ trách: Công nghệ thông tin",
            "Mã môn học: 224604", "Tên môn học: Tiếng Anh 1", "Số tín chỉ: 2",
            "Khoa phụ trách: Ngoại ngữ",
        ])
        self.assertEqual(res.calls, 0)

    def test_chu_ky_ham_khoi_tao(self):
        cls = run(D2, "cau5.py").g["MonHoc"]
        self.assertEqual(list(inspect.signature(cls.__init__).parameters),
                         ["self", "MaMonHoc", "TenMonHoc", "SoTinChi", "KhoaPhuTrach"])

    def test_thuoc_tinh_va_phuong_thuc(self):
        cls = run(D2, "cau5.py").g["MonHoc"]
        a = cls(1, "Môn A", 2, "Khoa A")
        b = cls(2, "Môn B", 4, "Khoa B")
        self.assertEqual(vars(a), {"MaMonHoc": 1, "TenMonHoc": "Môn A",
                                   "SoTinChi": 2, "KhoaPhuTrach": "Khoa A"})
        self.assertEqual(vars(b), {"MaMonHoc": 2, "TenMonHoc": "Môn B",
                                   "SoTinChi": 4, "KhoaPhuTrach": "Khoa B"})
        self.assertEqual(capture(a.thongtinmonhoc), [
            "Mã môn học: 1", "Tên môn học: Môn A", "Số tín chỉ: 2", "Khoa phụ trách: Khoa A"])
        self.assertEqual(a.TenMonHoc, "Môn A")

    def test_goi_bang_tham_so_ten(self):
        cls = run(D2, "cau5.py").g["MonHoc"]
        o = cls(KhoaPhuTrach="K", SoTinChi=3, TenMonHoc="T", MaMonHoc="M")
        self.assertEqual(capture(o.thongtinmonhoc), [
            "Mã môn học: M", "Tên môn học: T", "Số tín chỉ: 3", "Khoa phụ trách: K"])

    def test_kieu_du_lieu_giu_nguyen(self):
        cls = run(D2, "cau5.py").g["MonHoc"]
        o = cls(229008, "CSDL", 3, "CNTT")
        self.assertIs(type(o.MaMonHoc), int)
        self.assertIs(type(o.SoTinChi), int)


# ======================================================================
# Chạy thật bằng tiến trình riêng với stdin thật (end-to-end)
# ======================================================================
E2E_INPUTS = {
    (D1, "cau1.py"): ["635"],
    (D1, "cau2.py"): ["Hello 123"],
    (D1, "cau3.py"): ["3", "4", "0", "4"],
    (D1, "cau4.py"): ["1", "S01", "A", "B", "C", "2020", "S01"],
    (D1, "cau5.py"): [],
    (D2, "cau1.py"): ["12"],
    (D2, "cau2.py"): ["hello World"],
    (D2, "cau3.py"): ["3", "4", "0", "4"],
    (D2, "cau4.py"): ["1", "PC1", "8", "256", "Dell", "2022", "PC1"],
    (D2, "cau5.py"): [],
}


class EndToEnd(unittest.TestCase):
    def test_chay_tung_file_bang_stdin_that(self):
        for (folder, name), inputs in E2E_INPUTS.items():
            label = f"{os.path.basename(folder)}/{name}"
            with self.subTest(file=label):
                r = subprocess.run(
                    [sys.executable, "-X", "utf8", os.path.join(folder, name)],
                    input="\n".join(inputs) + "\n", capture_output=True,
                    text=True, encoding="utf-8", timeout=15)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(r.stderr, "")
                self.assertTrue(r.stdout.strip(), "không in ra gì")

    def test_dau_nhac_nhap_hien_thi_that(self):
        r = subprocess.run(
            [sys.executable, "-X", "utf8", os.path.join(D1, "cau1.py")],
            input="2000\n635\n", capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertEqual(r.stdout.count("Nhập giá trị 1<=n<=1500: "), 2)
        self.assertIn("Số lượng chữ số lẻ là: 2", r.stdout)

    def test_input_sai_dinh_dang_khong_duoc_bat(self):
        # Đề không yêu cầu xử lý nhập chữ thay cho số: chương trình báo ValueError là chấp nhận được.
        r = subprocess.run(
            [sys.executable, "-X", "utf8", os.path.join(D1, "cau1.py")],
            input="abc\n", capture_output=True, text=True, encoding="utf-8", timeout=15)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ValueError", r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
