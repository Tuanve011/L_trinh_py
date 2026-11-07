# Câu 5 - Đề 1


class DienThoai:
    def __init__(self, MaMay, TenMay, HangSanXuat, DungLuongPin, GiaBan):
        self.MaMay = MaMay
        self.TenMay = TenMay
        self.HangSanXuat = HangSanXuat
        self.DungLuongPin = DungLuongPin
        self.GiaBan = GiaBan

    def thongtindienthoai(self):
        print("Mã máy:", self.MaMay)
        print("Tên máy:", self.TenMay)
        print("Hãng sản xuất:", self.HangSanXuat)
        print("Dung lượng pin:", self.DungLuongPin)
        print("Giá bán:", self.GiaBan)


DT1 = DienThoai("DT01", "iPhone 15 Pro", "Apple", 3274, 28990000)
DT2 = DienThoai("DT02", "Galaxy S24 Ultra", "Samsung", 5000, 29990000)
DT1.thongtindienthoai()
DT2.thongtindienthoai()
