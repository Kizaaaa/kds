# Simulasi Interaksi Predator-Mangsa dalam Ekosistem Laut Berbasis Pemodelan Komputasional

Penelitian ini mengembangkan model Agent-Based Modeling (ABM) untuk mensimulasikan interaksi predator-mangsa dalam ekosistem laut pada ruang dua dimensi toroidal di mana setiap sel grid (misalnya 50×50) hanya dapat dihuni satu agen. Agen mangsa bergerak secara acak dan bereproduksi setelah interval tertentu, sedangkan agen predator bergerak menuju mangsa untuk memperoleh energi, kehilangan energi setiap langkah, dan mati jika energinya habis; reproduksi predator terjadi ketika interval dan energi mencukupi. Dengan memvariasikan kepadatan makanan, ukuran ruang, interval reproduksi, energi awal predator, dan komposisi populasi awal, simulasi menunjukkan bahwa peningkatan ketersediaan makanan dan ruang yang lebih luas meredam fluktuasi populasi, interval reproduksi pendek pada mangsa memicu ledakan populasi diikuti oleh kolaps predator, serta terdapat ambang rasio mangsa:predator di mana ekosistem hanya mencapai stabilitas jika kondisi tersebut terpenuhi. 

## Prerequisite

- Python

## Cara Menjalankan

1. clone repository ini

```sh
git clone https://github.com/Kizaaaa/kds.git
```

2. Cukup jalankan file `main.py`

```sh
py main.py
```

## Anggota Kelompok

| NIM | Nama |
|-|-|
| 13522059 | Dzaky Satrio Nugroho |
| 13522105 | Fabian Radenta Bangun |
| 13522119 | Indraswara Galih Jayanegara |