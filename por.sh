#!/bin/bash

#cara menggunakan cukup kasih link awal aja

# Minta input URL dari pengguna
read -p "Masukkan URL: " url

# Validasi input
if [ -z "$url" ]; then
  echo "URL tidak boleh kosong."
  exit 1
fi

# Simpan URL ke dalam file history.txt dengan timestamp
echo "$(date '+%Y-%m-%d %H:%M:%S') - $url" >> history.txt

# Eksekusi perintah untuk mengambil link video dan menghapus duplikat
curl -s -A "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36" "$url" \
| grep -o 'href="/view_video.php[^"]*"' \
| sed 's/href="//;s/"$//' \
| sed 's|^|https://www.pornhub.com|' \
| sort -u > link.txt

# Periksa jika curl gagal
if [ $? -ne 0 ]; then
  echo "Gagal mengambil data dari URL."
  exit 1
fi

# Kosongkan file hasil.txt sebelum mulai
> hasil.txt

# Ambil .m3u8 720P dari setiap link video
while IFS= read -r video_url; do
    echo "Memproses: $video_url"
    curl -sA "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36" "$video_url" \
    | grep -oP 'https:\\/\\/[^"]+720P[^"]*\.m3u8[^"]*' \
    | sed 's/\\//g' >> hasil.txt
done < link.txt

echo "Selesai. Link .m3u8 disimpan di hasil.txt"
