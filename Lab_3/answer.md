Q1:
Mỗi lần thêm 1 số 0 sẽ làm khối lượng tính toán kỳ vọng tăng lên 16 lần. Do hàm băm SHA-256 sẽ có thể biểu diễn 1 ký tự dưới 16 khả năng, nên xác suất để bắt đầu bằng k số 0 sẽ là (1/16)^k. Thêm một số 0 vào chuỗi liên tiếp sẽ là (1/16)^(k+1). Kỳ vọng khi đó sẽ tăng lên 16^(k+1)/16^k = 16 lần.

Q2:
Việc kiểm tra nonce tìm được chỉ tốn đúng 1 lần gọi băm.
Khi máy đào (miner) tìm ra được một nonce hợp lệ , họ sẽ gửi kèm nonce này cùng với khối dữ liệu (block) cho mạng lưới. Bất kỳ ai trong mạng lưới muốn kiểm tra chỉ việc thực hiện một phép tính duy nhất: hashlib.sha256(data + str(12345).encode()).hexdigest() Sau đó, họ chỉ cần nhìn xem chuỗi kết quả có bắt đầu bằng đủ k số 0 hay không.

Q3:
Một proof sẽ chứa [log_2(1,000,000)] = 20 giá trị băm. Vì cấu trúc là cây nhị phân, độ dài đường dẫn từ lá lên gốc chính là chiều cao của cây
Q4:
SPV (Simplified Payment Verification) trong Bitcoin: Các "node nhẹ" (light clients/wallets) trên điện thoại không cần tải toàn bộ hàng trăm GB dữ liệu blockchain. Chúng chỉ tải block headers và dùng Merkle proof do các full node cung cấp để xác minh một giao dịch cụ thể đã thực sự được đưa vào block.
Airdrop Claims (Crypto): Khi phân phát token cho người dùng, thay vì lưu hàng nghìn địa chỉ ví hợp lệ lên smart contract (rất tốn phí gas), dự án chỉ lưu trữ Merkle Root. Người dùng tự gửi Merkle proof của địa chỉ ví mình lên để smart contract kiểm tra (verify_proof) xem họ có nằm trong danh sách hay không.

Task 1: Run twice with the same message — is the signature identical? Which RFC explains this? / Chạy hai lần cùng thông điệp — chữ ký có giống nhau không? RFC nào giải thích điều này?

Kết quả: Chữ ký tạo ra ở cả hai lần là giống hệt nhau.
Giải thích (RFC 6979): Chuẩn RFC 6979 quy định việc sử dụng thuật toán ECDSA mang tính tất định (deterministic). Thay vì sử dụng một số ngẫu nhiên (nonce) mỗi khi ký có thể dẫn đến lỗ hổng bảo mật nếu hệ thống sinh số kém, thư viện Ethereum tính toán số nonce này bằng hàm băm kết hợp giữa khóa bí mật và chính nội dung thông điệp. Vì khóa bí mật và thông điệp không thay đổi, chữ ký tạo ra ở mọi lần đều bất biến.

Task 2: Show the TA: the tampered message recovers a different address. Explain why this proves integrity. / Cho trợ giảng xem: thông điệp bị sửa khôi phục ra địa chỉ khác. Giải thích vì sao đây là bằng chứng toàn vẹn.

Tính toàn vẹn được chứng minh qua quá trình tính toán ngược của hàm recover_message. Chữ ký số nguyên bản được tạo ra từ mã băm của thông điệp gốc. Khi thông điệp bị sửa (từ "Buoi 3" thành "Buoi 4"), mã băm của nó thay đổi hoàn toàn. Thuật toán ECDSA khi nhận một mã băm sai kết hợp với chữ ký cũ sẽ khôi phục ra một khóa công khai (và địa chỉ ví) không liên quan. Việc người nhận đối chiếu thấy địa chỉ khôi phục không khớp với địa chỉ người gửi ban đầu chính là bằng chứng toán học xác nhận dữ liệu đã bị can thiệp trên đường truyền.
