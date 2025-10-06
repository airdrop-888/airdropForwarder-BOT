# forwarder_bot.py

import logging
from datetime import datetime, timezone  # BARU: Import library untuk menangani waktu
from telethon import TelegramClient, events # <--- PASTIKAN BARIS INI ADA

# --- KONFIGURASI ---
# Ganti nilai-nilai di bawah ini dengan informasi Anda sendiri.

# 1. Kredensial API dari my.telegram.org
API_ID = 28450000  # Ganti dengan API ID Anda
API_HASH = '77dc7875353...' # Ganti dengan API Hash Anda

# 2. Nama file sesi
SESSION_NAME = 'my_user_session'

# 3. ID Channel Sumber (gunakan ID numerik, bukan @username)
SOURCE_CHANNELS = [
    -10022...,  # Contoh untuk https://t.me/NTExhaust
    -10022...,  # Contoh untuk https://t.me/AirdropInsiderID
    -10022...,  # Contoh untuk https://t.me/getairdrop_id
    -10022...,  # Contoh untuk https://t.me/airdropcloudJP
    -10022...,  # Contoh untuk https://t.me/AirdropFamilyIDN
    -10022...,  # Contoh untuk https://t.me/airdropfind
]

# 4. ID Channel Tujuan (gunakan ID numerik)
DESTINATION_CHANNEL = -10022...,  # Contoh untuk https://t.me/airdroplocked

# --- AKHIR DARI KONFIGURASI ---


# Konfigurasi logging untuk melihat output di terminal
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# BARU: Variabel global untuk menyimpan waktu bot dimulai
START_TIME = None

# Inisialisasi Telegram Client
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


# Event Handler untuk Pesan Baru
@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def forwarder_handler(event):
    """Fungsi ini menangani pesan baru dan meneruskannya."""
    try:
        # BARU: Cek apakah pesan ini dibuat SEBELUM bot dimulai
        # event.message.date adalah timezone-aware, jadi kita bandingkan dengan START_TIME
        if event.message.date < START_TIME:
            # Jika pesan lebih tua, abaikan dan jangan lakukan apa-apa
            logger.info(f"Melewatkan pesan lama dari channel {event.chat_id}")
            return

        # Log informasi tentang pesan yang masuk (ini adalah pesan baru)
        logger.info(f"Pesan baru terdeteksi dari channel ID: {event.chat_id}")
        
        # Meneruskan pesan ke channel tujuan
        await client.forward_messages(DESTINATION_CHANNEL, event.message)
        
        # Log konfirmasi bahwa pesan telah diteruskan
        logger.info(f"Pesan berhasil diteruskan ke channel ID: {DESTINATION_CHANNEL}")

    except Exception as e:
        # Tangani kemungkinan error saat proses penerusan pesan
        logger.error(f"Terjadi error saat meneruskan pesan: {e}")


async def main():
    """Fungsi utama untuk menjalankan bot."""
    global START_TIME  # BARU: Gunakan variabel START_TIME global

    # Menghubungkan client ke server Telegram
    await client.start()
    logger.info("Client berhasil terhubung ke Telegram.")

    # BARU: Setel waktu mulai SETELAH client berhasil terhubung
    # Menggunakan timezone.utc agar konsisten dengan waktu dari Telegram
    START_TIME = datetime.now(timezone.utc)
    
    # Menampilkan informasi bahwa bot telah berjalan
    print("=========================================")
    print("  Bot Auto-Forwarder Berhasil Dijalankan!  ")
    print("=========================================")
    print(f"Memantau {len(SOURCE_CHANNELS)} channel sumber.")
    print(f"Meneruskan pesan ke channel tujuan dengan ID: {DESTINATION_CHANNEL}")
    print("HANYA pesan baru yang muncul setelah saat ini yang akan diteruskan.")
    print("Bot akan terus berjalan. Tekan CTRL+C untuk berhenti.")
    
    # Menjaga skrip tetap berjalan
    await client.run_until_disconnected()


if __name__ == '__main__':
    try:
        client.loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("Bot dihentikan secara manual.")
