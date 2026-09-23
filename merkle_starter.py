import hashlib

def H(b: bytes) -> bytes:
    return hashlib.sha256(b).digest()

def merkle_root(leaves: list[bytes]) -> bytes:
    """TODO 1: dựng cây từ dưới lên, trả về băm gốc."""
    if not leaves:
        return b""
    
    current_level = leaves
    while len(current_level) > 1:
        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            if i + 1 == len(current_level):
                right = left
            else:
                right = current_level[i + 1]
            next_level.append(H(left + right))
        current_level = next_level
        
    return current_level[0]

def merkle_proof(leaves: list[bytes], index: int) -> list[tuple[bytes, bool]]:
    """TODO 2: trả về [(sibling_digest, sibling_is_left), ...] từ lá lên gốc."""
    proof = []
    current_level = leaves
    curr_idx = index
    
    while len(current_level) > 1:
        if curr_idx % 2 == 1:
            sibling = current_level[curr_idx - 1]
            is_left = True
        else:
            if curr_idx + 1 == len(current_level):
                sibling = current_level[curr_idx]
            else:
                sibling = current_level[curr_idx + 1]
            is_left = False
            
        proof.append((sibling, is_left))

        next_level = []
        for i in range(0, len(current_level), 2):
            left = current_level[i]
            right = left if i + 1 == len(current_level) else current_level[i + 1]
            next_level.append(H(left + right))
            
        current_level = next_level
        curr_idx = curr_idx // 2 
        
    return proof

def verify_proof(leaf_hash: bytes, proof: list[tuple[bytes, bool]], root: bytes) -> bool:
    """TODO 3: tính ngược lên gốc rồi so sánh."""
    curr_hash = leaf_hash
    for sibling_hash, is_left in proof:
        if is_left:
            curr_hash = H(sibling_hash + curr_hash)
        else:
            curr_hash = H(curr_hash + sibling_hash)
            
    return curr_hash == root


# --- TEST CODE ---
txs = [b"tx0", b"tx1", b"tx2", b"tx3", b"tx4", b"tx5", b"tx6", b"tx7"]
leaves = [H(t) for t in txs]
root = merkle_root(leaves)
print("root", root.hex())

# CHECK 1: proof đúng cho mọi lá
ok = all(verify_proof(leaves[i], merkle_proof(leaves, i), root) for i in range(8))
print("CHECK 1 (all 8 proofs valid):", "OK" if ok else "FAIL")

# CHECK 2: proof có đúng log2(8)=3 phần tử 
print("CHECK 2 (proof length == 3):", "OK" if len(merkle_proof(leaves, 4)) == 3 else "FAIL")

# CHECK 3: lá bị sửa phải trượt
fake = H(b"tx4: A->B 999999 coin")
print("CHECK 3 (tampered leaf fails):", "OK" if not verify_proof(fake, merkle_proof(leaves, 4), root) else "FAIL")

# CHECK 4: số lá lẻ (7) vẫn chạy
l7 = leaves[:7]
r7 = merkle_root(l7)
print("CHECK 4 (odd count works):", "OK" if all(verify_proof(l7[i], merkle_proof(l7, i), r7) for i in range(7)) else "FAIL")