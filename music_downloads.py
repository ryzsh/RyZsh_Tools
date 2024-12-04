import os
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

# Lokasi folder untuk menyimpan hasil unduhan
download_folder = "/storage/117B-0D1C/Downloads/music"

# Fungsi untuk mencari lagu berdasarkan kata kunci
def search_songs(query, max_results=90):
    print(f"Mencari lagu untuk '{query}'...")
    search = VideosSearch(query, limit=max_results)
    results = search.result()["result"]
    return [
        {
            "title": result["title"],
            "duration": result["duration"],
            "url": result["link"]
        }
        for result in results
    ]

# Fungsi untuk menampilkan daftar hasil pencarian
def display_results(results):
    print("\nHasil pencarian:")
    for i, song in enumerate(results, start=1):
        print(f"{i}. {song['title']} ({song['duration']})")
    print("\nPilih nomor lagu (pisahkan dengan koma untuk memilih banyak lagu, atau ketik 'q' untuk keluar):")

# Fungsi untuk mengunduh lagu menggunakan yt-dlp
def download_songs(selected_songs):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "quiet": False,
    }

    with YoutubeDL(ydl_opts) as ydl:
        for song in selected_songs:
            print(f"Mengunduh: {song['title']}...")
            ydl.download([song["url"]])
    print("\nProses unduhan selesai!")

def main():
    query = input("Masukkan nama lagu atau artis: ")
    results = search_songs(query)
    if not results:
        print("Tidak ada hasil ditemukan.")
        return
    
    display_results(results)
    choice = input("> ").strip()
    if choice.lower() == 'q':
        print("Keluar.")
        return
    
    try:
        indices = [int(i) - 1 for i in choice.split(",") if i.strip().isdigit()]
        selected_songs = [results[i] for i in indices if 0 <= i < len(results)]
        if not selected_songs:
            print("Pilihan tidak valid.")
            return
        download_songs(selected_songs)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()
