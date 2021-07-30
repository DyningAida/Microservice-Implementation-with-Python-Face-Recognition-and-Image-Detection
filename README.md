# UAS AI - Identifikasi Gambar 
# (Dyning Aida Batrishya 1184030)
---
Aplikasi ini menggunakan framework flask dengan menggunakan library opencv dan pillow untuk melakukan pemrosesan pada gambarnya, dan beberapa library pendukung lain seperti pymysql untuk connect ke database mysql, numpy, dan sebagainya.


Cara kerja :
1. untuk generate datasetnya, dilakukan dengan menjalankan input.py dengan memasukkan npm sebagai idnya, kemudian foto akan diambil sebanyak maksimal 30 foto dengan nama mhs_npm_urutan.jpg
2. setelah itu, jalankan train.py untuk mengubah foto yang disimpan menjadi file training.xml, file training.xml ini nantilah yang akan dibaca ketika identifikasi foto
3. jika melakukan penambahan foto pada input.py, hapus file training.xml terlebih dahulu, lalu jalankan lagi train.pynya
4. program aplikasi ada di file app.py
5. untuk menjalankan aplikasinya berikut merupakan fitur-fiturnya, di antaranya :
- Cek profile - jika menekan button ini, apabila foto user telah terdaftar di dataset aplikasi, maka akan ditampilkan profil user sesuai dengan yang terdaftar
- Daftarkan foto - button ini diperlukan apabila foto user belum terdaftar di aplikasi, sehingga harus mendaftarkan foto terlebih dahulu dengan cara login sesuai akun di SIAP, kemudian jika sudah diautentikasi, maka aplikasi akan memulai merekam wajah dan kemudian akan redirect ke halaman cek profil sesuai npm yang baru saja mendaftarkan foto
- Cek foto - button ini akan mengarahkan pada halaman untuk upload foto, pada fitur ini user dapat memasukkan foto, kemudian aplikasi akan mengidentifikasi foto tersebut sesuai dengan data foto yang telah tersimpan untuk kemudian akan ditampilkan NPM yang dimiliki oleh foto tersebut.