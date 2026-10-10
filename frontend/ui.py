# File: frontend/ui.py

import tkinter as tk
import csv
import time
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.m1_pesanan import Array, Pesanan

data_array = Array()
id_baru = 200001


def cetak_log(pesan):
    text_log.insert(tk.END, pesan + "\n")
    text_log.see(tk.END)


def tombol_load_csv():
    global data_array
    data_array = Array()

    path_file = "data/pesanan.csv"
    if not os.path.exists(path_file):
        path_file = "pesanan.csv"

    if not os.path.exists(path_file):
        cetak_log("Error: File pesanan.csv tidak ditemukan!")
        return

    waktu_mulai = time.perf_counter()

    f = open(path_file, "r", encoding="utf-8")
    reader = csv.reader(f)
    header = next(reader)

    count = 0
    for row in reader:
        p = Pesanan(
            row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]
        )
        data_array.append(p)
        count += 1

    f.close()

    waktu_selesai = time.perf_counter()
    durasi_ms = (waktu_selesai - waktu_mulai) * 1000

    label_status.config(text="Status: " + str(count) + " data berhasil dimuat ke Array")
    cetak_log("Load CSV Selesai (" + str(count) + " data) -> Waktu: " + str(round(durasi_ms, 2)) + " ms")


def buat_pesanan_baru(prioritas):
    global id_baru
    oid = "O-" + str(id_baru)
    id_baru += 1

    nama = entry_nama.get()
    if nama == "":
        nama = "Pelanggan Baru"

    return Pesanan(oid, nama, "kafe-teknik", "mie-ayam", "12000", str(prioritas), "50000", "", "ANTRE")


def array_lihat():
    try:
        idx = int(entry_index.get())
    except:
        idx = 0

    t1 = time.perf_counter()
    p = data_array.get(idx)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    text_hasil.delete("1.0", tk.END)
    if p != None:
        text_hasil.insert(
            tk.END,
            "ARRAY Index " + str(idx) + ":\n"
            + p.oid + " | " + p.pelanggan + " | " + p.menu + " | Rp" + p.harga + " | Status: " + p.status
        )
    else:
        text_hasil.insert(tk.END, "Data tidak ditemukan!")

    cetak_log("ARRAY - Lihat index " + str(idx) + " -> Waktu: " + str(round(ms, 4)) + " ms")


def array_tambah_reguler():
    p = buat_pesanan_baru(3)
    t1 = time.perf_counter()
    data_array.append(p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    cetak_log("ARRAY - Tambah Reguler (" + p.oid + ") di belakang -> Waktu: " + str(round(ms, 4)) + " ms")


def array_tambah_prioritas():
    p = buat_pesanan_baru(2)
    posisi_tengah = data_array.size // 2

    t1 = time.perf_counter()
    data_array.insert(posisi_tengah, p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    cetak_log("ARRAY - Tambah Prioritas (" + p.oid + ") di tengah (" + str(posisi_tengah) + ") -> Waktu: " + str(round(ms, 4)) + " ms")


def array_tambah_vip():
    p = buat_pesanan_baru(1)

    t1 = time.perf_counter()
    data_array.insert(0, p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    cetak_log("ARRAY - Tambah VIP (" + p.oid + ") di depan (idx 0) -> Waktu: " + str(round(ms, 4)) + " ms")


def array_hapus():
    try:
        idx = int(entry_index.get())
    except:
        idx = 0

    t1 = time.perf_counter()
    p = data_array.delete(idx)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    if p != None:
        cetak_log("ARRAY - Hapus index " + str(idx) + " (" + p.oid + ") -> Waktu: " + str(round(ms, 4)) + " ms")
    else:
        cetak_log("ARRAY - Hapus gagal, index tidak valid!")


# UI Tkinter
root = tk.Tk()
root.title("2EZ4U Food Delivery - Focus Array")
root.geometry("850x550")

frame_atas = tk.Frame(root, bg="lightblue")
frame_atas.pack(fill=tk.X)

btn_load = tk.Button(frame_atas, text="Load Data CSV", command=tombol_load_csv, bg="green", fg="white")
btn_load.pack(side=tk.LEFT, padx=10, pady=5)

label_status = tk.Label(frame_atas, text="Status: Belum ada data", bg="lightblue")
label_status.pack(side=tk.LEFT, padx=10)

frame_utama = tk.Frame(root)
frame_utama.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

frame_kiri = tk.Frame(frame_utama, width=220, bd=2, relief=tk.GROOVE)
frame_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=5)

lbl_arr = tk.Label(frame_kiri, text="--- FITUR ARRAY ---", font=("Arial", 10, "bold"))
lbl_arr.pack(pady=10)

tk.Button(frame_kiri, text="ARRAY - LIHAT PESANAN", width=24, command=array_lihat).pack(pady=3)
tk.Button(frame_kiri, text="ARRAY - TAMBAH REGULER", width=24, command=array_tambah_reguler).pack(pady=3)
tk.Button(frame_kiri, text="ARRAY - TAMBAH PRIORITAS", width=24, command=array_tambah_prioritas).pack(pady=3)
tk.Button(frame_kiri, text="ARRAY - TAMBAH VIP", width=24, command=array_tambah_vip).pack(pady=3)
tk.Button(frame_kiri, text="ARRAY - HAPUS PESANAN", width=24, command=array_hapus).pack(pady=3)

frame_kanan = tk.Frame(frame_utama)
frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

frame_form = tk.LabelFrame(frame_kanan, text="Input Parameter")
frame_form.pack(fill=tk.X, pady=5)

tk.Label(frame_form, text="Nama Pelanggan:").grid(row=0, column=0, padx=5, pady=5)
entry_nama = tk.Entry(frame_form)
entry_nama.insert(0, "Pelanggan Baru")
entry_nama.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_form, text="Indeks Ke-i:").grid(row=0, column=2, padx=5, pady=5)
entry_index = tk.Entry(frame_form, width=10)
entry_index.insert(0, "0")
entry_index.grid(row=0, column=3, padx=5, pady=5)

text_hasil = tk.Text(frame_kanan, height=8)
text_hasil.pack(fill=tk.BOTH, expand=True, pady=5)

frame_log = tk.LabelFrame(frame_kanan, text="COMMAND LOG & WAKTU")
frame_log.pack(fill=tk.X, side=tk.BOTTOM)

text_log = tk.Text(frame_log, height=6, bg="black", fg="lime", font=("Consolas", 9))
text_log.pack(fill=tk.BOTH, expand=True)

root.mainloop()