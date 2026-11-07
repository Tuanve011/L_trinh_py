# Câu 4 - Đề 2

# a. Nhập thông tin máy tính, lưu vào từ điển
n = int(input("Nhập số lượng máy tính: "))
tudien = {}
for i in range(n):
    SoHieu = input("Nhập số hiệu máy tính: ")
    BoNho = int(input("Nhập dung lượng bộ nhớ: "))
    OCung = int(input("Nhập dung lượng ổ cứng: "))
    HangSanXuat = input("Nhập hãng sản xuất: ")
    NamSanXuat = int(input("Nhập năm sản xuất: "))
    tudien[SoHieu] = [BoNho, OCung, HangSanXuat, NamSanXuat]
print(tudien)

# b. Xóa máy tính theo số hiệu
x = input("Nhập số hiệu máy tính cần tìm: ")
if x in tudien:
    del tudien[x]
    print(f"Máy tính có số hiệu {x} đã được xóa.")
else:
    print("Không có máy tính cần xóa.")
print(tudien)
