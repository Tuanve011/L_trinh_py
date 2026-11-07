# Câu 3 - Đề 1
danhsach = []
while True:
    x = int(input("Nhập danh sách: "))
    if x == 0:
        break
    danhsach.append(x)
print("Danh sách vừa nhập:", danhsach)

tong = 0
for i in danhsach:
    if i > 0 and i % 2 == 0:
        tong += i
if tong != 0:
    print("Tổng các số dương chẵn trong danh sách:", tong)
else:
    print("Không có số dương chẵn trong danh sách.")

k = int(input("Nhập k: "))
dem = 0
for i in danhsach:
    if i == k:
        dem += 1
if dem == 0:
    print("Không có phần tử", k, "trong danh sách")
else:
    print("Số lần xuất hiện của", k, "là:", dem)
