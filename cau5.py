# Câu 5 - Đề 2


class MonHoc:
    def __init__(self, MaMonHoc, TenMonHoc, SoTinChi, KhoaPhuTrach):
        self.MaMonHoc = MaMonHoc
        self.TenMonHoc = TenMonHoc
        self.SoTinChi = SoTinChi
        self.KhoaPhuTrach = KhoaPhuTrach

    def thongtinmonhoc(self):
        print("Mã môn học:", self.MaMonHoc)
        print("Tên môn học:", self.TenMonHoc)
        print("Số tín chỉ:", self.SoTinChi)
        print("Khoa phụ trách:", self.KhoaPhuTrach)


CSDL = MonHoc(229008, "Cơ sở dữ liệu", 3, "Công nghệ thông tin")
TA1 = MonHoc(224604, "Tiếng Anh 1", 2, "Ngoại ngữ")
CSDL.thongtinmonhoc()
TA1.thongtinmonhoc()
