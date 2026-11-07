# Câu 1 - Đề 1
def DemChuSoLe(n):
    dem = 0
    while n != 0:
        tam = n % 10
        if tam % 2 != 0:
            dem += 1
        n //= 10
    return dem

def S(n):
    s = 0
    for i in range(1, n + 1):
        s += 1 / (2 * i)
    return s

n = int(input("Nhập giá trị 1<=n<=1500: "))
while n < 1 or n > 1500:
    n = int(input("Nhập giá trị 1<=n<=1500: "))

print("Số lượng chữ số lẻ là:", DemChuSoLe(n))
print("S =", S(n))
