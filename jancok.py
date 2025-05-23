import requests
from bs4 import BeautifulSoup
import re
import html
import subprocess

# Meminta input URL halaman utama
url = input("Masukkan URL halaman utama (misal: https://www.pornhub.com/channels/newsensations): ")

headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
}

# File untuk menyimpan URL hasil
output_file = "url_hasil.txt"

# Ambil halaman utama
response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Ambil semua link video unik
    links = {a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('/view_video.php')}
    
    # Gabungkan link menjadi URL penuh
    full_links = ["https://www.pornhub.com" + link for link in links]
    
    # Menyimpan hasil ke file lokal
    with open(output_file, "w") as file:
        for video_link in full_links:
            video_response = requests.get(video_link, headers=headers)
            
            if video_response.status_code == 200:
                # Regex untuk menangkap URL video 1080P
                match = re.search(r'"videoUrl":"(https:\\/\\/.*?1080P_.*?\.m3u8\?[^"]+)"', video_response.text)
                
                if match:
                    url_encoded = match.group(1)
                    video_url = html.unescape(url_encoded).replace("\\/", "/")
                    file.write(f"{video_url}\n")
                    print(f"Saved: {video_url}")
                else:
                    #file.write(f"Video URL 1080P tidak ditemukan untuk {video_link}\n")
                    print(f"Not found for: {video_link}")
            else:
                print(f"Failed to access: {video_link}")
    
    print("Hasil berhasil disimpan ke file 'url_hasil.txt'. Sekarang, mengupload ke Termbin...")

    # Menjalankan perintah 'cat url_hasil.txt | nc termbin.com 9999' menggunakan subprocess
    try:
        # Menggunakan subprocess untuk menjalankan perintah netcat
        subprocess.run(f"cat {output_file} | nc termbin.com 9999", shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error uploading to Termbin: {e}")
else:
    print("Failed to retrieve the main page. Status code:", response.status_code)