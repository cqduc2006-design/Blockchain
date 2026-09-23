from eth_account import Account
from eth_account.messages import encode_defunct

# 1. Tạo một tài khoản Ethereum ngẫu nhiên
acct = Account.create()
print("address:", acct.address)
# TUYỆT ĐỐI không dùng khóa này cho tiền thật

# 2. Tạo thông điệp và ký (Sign)
msg = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 3")
sig = Account.sign_message(msg, acct.key)
print("r,s,v:", hex(sig.r), hex(sig.s), sig.v)

# 3. Khôi phục địa chỉ chỉ từ chữ ký (Verify/Recover)
who = Account.recover_message(msg, signature=sig.signature)
print("recovered:", who, "| match:", who == acct.address)

# 4. Giả lập việc sửa đổi thông điệp (Tamper 1 character)
bad = encode_defunct(text="I attended Session 3 / Toi da hoc Buoi 4") # Đổi Buoi 3 thành Buoi 4
tampered_who = Account.recover_message(bad, signature=sig.signature)
print("tampered ->", tampered_who)
print("tampered match:", tampered_who == acct.address)


print("___________________________________________________________________")
print("Task 1")
# Ký lần 1
sig1 = Account.sign_message(msg, acct.key)
# Ký lần 2 (cùng thông điệp, cùng khóa bí mật)
sig2 = Account.sign_message(msg, acct.key)

print("Chữ ký 1:", sig1.signature.hex())
print("Chữ ký 2:", sig2.signature.hex())
print("Chữ ký 1 và 2 giống hệt nhau:", sig1.signature == sig2.signature)