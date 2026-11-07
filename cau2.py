# Câu 2 - Đề 2
s = input("Nhập chuỗi s: ")

# a. Đếm số ký tự chữ thường
dem = 0
for i in s:
    if i.islower():
        dem += 1
if dem == 0:
    print("Chuỗi không có ký tự chữ thường.")
else:
    print("Số ký tự chữ thường trong chuỗi:", dem)


# b. Kiểm tra chuỗi đối xứng
def DoiXung(s):
    if s == s[::-1]:
        print("Chuỗi đối xứng.")
    else:
        print("Chuỗi không đối xứng.")


DoiXung(s)

# c. Đổi ký tự đầu tiên của mỗi từ thành chữ hoa
s = s.title()
print("Chuỗi sau khi chuyển ký tự đầu tiên của mỗi từ thành chữ hoa:", s)
