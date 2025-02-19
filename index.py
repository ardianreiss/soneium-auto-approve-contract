from web3 import Web3
import json

# Koneksi ke node Ethereum
infura_url = 'SONEIUM_RPC'  # Ganti dengan RPC Soneium
web3 = Web3(Web3.HTTPProvider(infura_url))

# Verifikasi koneksi
if not web3.is_connected():
    print("Tidak dapat terhubung ke node Ethereum")
    exit()

# Alamat kontrak
contract_address = 'YOUR_CONTRACT_ADDRESS'  # Ganti dengan alamat kontrak Anda

# Muat ABI dari file JSON
with open('contract_abi.json', 'r') as abi_file:
    contract_abi = json.load(abi_file)

# Inisialisasi kontrak
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Alamat dan kunci pribadi pengirim
sender_address = 'YOUR_WALLET_ADDRESS'  # Ganti dengan alamat dompet Anda
private_key = 'YOUR_PRIVATE_KEY'  # Ganti dengan kunci pribadi Anda

# Alamat penerima dan jumlah yang akan disetujui
spender_address = 'SPENDER_ADDRESS'  # Ganti dengan alamat penerima
amount = web3.to_wei(1, 'ether')  # Ganti dengan jumlah yang ingin Anda setujui

# Buat transaksi
nonce = web3.eth.get_transaction_count(sender_address)
txn = contract.functions.approve(spender_address, amount).build_transaction({
    'chainId': 1,  # Ganti dengan Chain ID Soneium
    'gas': 28000,
    'gasPrice': web3.to_wei('0.0017', 'gwei'),
    'nonce': nonce,
})

# Tanda tangani transaksi
signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

# Kirim transaksi
txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)

# Cetak hash transaksi
print(f'Transaksi berhasil dikirim dengan hash: {txn_hash.hex()}')
