# Câu 3 - Đề 2

# a. Nhập danh sách, dừng khi nhập 0
ds = []
while True:
    x = int(input("Nhập danh sách: "))
    if x == 0:
        break
    ds.append(x)
print("Danh sách vừa nhập:", ds)

# b. In các số dương chẵn
DuongChan = []
for i in ds:
    if i > 0 and i % 2 == 0:
        DuongChan.append(i)
if DuongChan:
    print("Các số dương chẵn có trong danh sách:", DuongChan)
else:
    print("Không có số dương chẵn trong danh sách.")

# c. Đếm số lần xuất hiện của k
k = int(input("Nhập k: "))
dem = ds.count(k)
if dem == 0:
    print(f"{k} không có trong danh sách")
else:
    print(f"{k} xuất hiện {dem} lần")
