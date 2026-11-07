# Câu 2 - Đề 1
s = input("Nhập chuỗi s: ")


# a. Đếm số ký tự chữ hoa
dem = 0
for i in s:
    if i.isupper():
        dem += 1
if dem == 0:
    print("Chuỗi không có ký tự chữ hoa.")
else:
    print("Số ký tự chữ hoa:", dem)


# b. Kiểm tra chuỗi đối xứng
def DoiXung(s):
    if s == s[::-1]:
        print("Chuỗi đối xứng.")
    else:
        print("Chuỗi không đối xứng.")


DoiXung(s)

# c. Tính tổng các chữ số trong chuỗi
tong = 0
for i in s:
    if i.isdigit():
        tong += int(i)
print("Tổng các chữ số trong chuỗi:", tong)
