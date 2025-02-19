from web3 import Web3
import json
import time

# Koneksi ke node Ethereum
infura_url = 'https://rpc.soneium.org'  # Ganti dengan URL node Ethereum Anda
web3 = Web3(Web3.HTTPProvider(infura_url))

# Verifikasi koneksi
if not web3.is_connected():
    print("Tidak dapat terhubung ke node Ethereum")
    exit()

# Alamat dan kunci pribadi pengirim
sender_address = 'YOUR_SENDER_ADDRESS'  # Ganti dengan alamat dompet Anda
private_key = 'YOUR_PRIVATE_KEY'  # Ganti dengan kunci pribadi Anda

# Alamat penerima dan jumlah yang akan disetujui
spender_address = 'YOUR_SPENDER_ADDRESS'  # Ganti dengan alamat penerima
amount = web3.to_wei(1, 'ether')  # Ganti dengan jumlah yang ingin Anda setujui

# Daftar kontrak
contracts = [
    {
        'address': 'CONTRACT_ADDRESS1',  # Ganti dengan alamat kontrak pertama
        'abi_path': 'data/contract_abi.json'  # Ganti path sesuai lokasi file ABI 
    },
    {
        'address': 'CONTRACT_ADDRESS2',  # Ganti dengan alamat kontrak pertama
        'abi_path': 'data/contract_abi.json'  # Ganti path sesuai lokasi file ABI 
    },
    # Tambahkan lebih banyak kontrak jika diperlukan
]

# Fungsi untuk memuat ABI dari file JSON
def load_abi(abi_path):
    with open(abi_path, 'r') as abi_file:
        return json.load(abi_file)

# Jumlah transaksi yang diinginkan
desired_tx_count = 66 

# Iterasi melalui daftar kontrak
nonce = web3.eth.get_transaction_count(sender_address)
tx_count = 0

for contract_info in contracts:
    if tx_count >= desired_tx_count:
        break

    contract_address = contract_info['address']
    contract_abi = load_abi(contract_info['abi_path'])

    # Inisialisasi kontrak
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)

    while tx_count < desired_tx_count:
        # Ambil harga gas yang disarankan oleh jaringan
        gas_price = web3.eth.gas_price

        # Buat transaksi
        txn = contract.functions.approve(spender_address, amount).build_transaction({
            'chainId': 1868,  # Ganti dengan Chain ID Soneium
            'gas': 30000,  # Anda bisa mencoba mengurangi nilai ini
            'gasPrice': gas_price,  # Gunakan harga gas yang disarankan
            'nonce': nonce,
        })

        # Tanda tangani transaksi
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=private_key)

        # Kirim transaksi
        try:
            txn_hash = web3.eth.send_raw_transaction(signed_txn.raw_transaction)
            print(f'Transaksi {tx_count + 1} untuk kontrak {contract_address} berhasil dikirim dengan hash: {txn_hash.hex()}')
            nonce += 1  # Increment nonce after successful transaction
            tx_count += 1  # Increment transaction count
        except Exception as e:
            print(f'Gagal mengirim transaksi untuk kontrak {contract_address}: {e}')

        # Jeda 1 menit sebelum mengirim transaksi berikutnya
        time.sleep(60)
