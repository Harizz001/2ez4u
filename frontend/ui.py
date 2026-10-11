import tkinter as tk
import csv
import time
import os
import sys

# Jalur ke folder backend agar bisa mengimpor modul dari sana
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from backend.m1_pesanan import Array, LinkList, Pesanan

# Variabel global untuk menyimpan data pesanan
data_array = Array()
data_ll = LinkList()
id_baru = 200001
fitur_aktif = "LIHAT"  # Default fitur yang aktif


def cetak_log(pesan):
    text_log.insert(tk.END, pesan + "\n")
    text_log.see(tk.END)


def tombol_load_csv():
    global data_array, data_ll
    data_array = Array()
    data_ll = LinkList()

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
        data_ll.append(p)
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

def pilih_fitur(kode_fitur):
    global fitur_aktif
    fitur_aktif = kode_fitur

    lbl_nama.grid_forget()
    entry_nama.grid_forget()
    lbl_index.grid_forget()
    entry_index.grid_forget()

    # Array
    if kode_fitur == "ARR_LIHAT_INDEKS":
        lbl_judul_fitur.config(text="Array: lihat pesanan berdasarkan Indeks (i)")
        lbl_sub_fitur.config(text="get: mengambil data pesanan pada indeks posisi tertentu")
        lbl_index.config(text="Indeks ke-i:")
        lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_index.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="CARI", bg="#0056b3", fg="white")

    elif kode_fitur == "ARR_LIHAT_OID":
        lbl_judul_fitur.config(text="Array: lihat pesanan berdasarkan OID")
        lbl_sub_fitur.config(text="cari_by_oid: pencarian linier berdasarkan ID Pesanan (contoh: O-000005)")
        lbl_index.config(text="OID Pesanan:")
        lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_index.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="CARI", bg="#0056b3", fg="white")

    elif kode_fitur == "ARR_TAMBAH_REGULER":
        lbl_judul_fitur.config(text="Array: pesanan REGULER, masuk paling belakang")
        lbl_sub_fitur.config(text="append: pesanan biasa, mengantre di barisan paling belakang")
        lbl_index.grid_remove()
        entry_index.grid_remove()
        lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="TAMBAH", bg="#0056b3", fg="white")

    elif kode_fitur == "ARR_TAMBAH_PRIORITAS":
        lbl_judul_fitur.config(text="Array: pesanan PRIORITAS, menyerobot ke tengah")
        lbl_sub_fitur.config(text="insert: disisipkan tepat di pertengahan barisan")
        lbl_index.grid_remove()
        entry_index.grid_remove()
        lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="TAMBAH", bg="#0056b3", fg="white")

    elif kode_fitur == "ARR_TAMBAH_VIP":
        lbl_judul_fitur.config(text="Array: pesanan VIP, langsung ke urutan pertama")
        lbl_sub_fitur.config(text="insert: disisipkan paling depan (indeks 0)")
        lbl_index.grid_remove()
        entry_index.grid_remove()
        lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="TAMBAH", bg="#0056b3", fg="white")

    elif kode_fitur == "ARR_HAPUS":
        lbl_judul_fitur.config(text="Array: hapus pesanan ke-i")
        lbl_sub_fitur.config(text="delete: mencabut pesanan dari barisan pada indeks tertentu")
        lbl_nama.grid_remove()
        entry_nama.grid_remove()
        lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_index.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="HAPUS", bg="#c0392b", fg="white")

    # Linked List
    elif kode_fitur == "LL_LIHAT_INDEKS":
        lbl_judul_fitur.config(text="LinkedList: lihat pesanan berdasarkan Indeks (i)")
        lbl_sub_fitur.config(text="get: menelusuri node dari head sampai indeks posisi tertentu")
        lbl_index.config(text="Indeks ke-i:")
        lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_index.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="CARI", bg="#27ae60", fg="white")

    elif kode_fitur == "LL_LIHAT_OID":
        lbl_judul_fitur.config(text="LinkedList: lihat pesanan berdasarkan OID")
        lbl_sub_fitur.config(text="cari_by_oid: menelusuri node berdasarkan ID Pesanan (contoh: O-000005)")
        lbl_index.config(text="OID Pesanan:")
        lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_index.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="CARI", bg="#27ae60", fg="white")

    elif kode_fitur == "LL_TAMBAH_REGULER":
        lbl_judul_fitur.config(text="LinkedList: pesanan REGULER, masuk paling belakang")
        lbl_sub_fitur.config(text="append: langsung disambung via tail pointer")
        lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="TAMBAH", bg="#27ae60", fg="white")

    elif kode_fitur == "LL_TAMBAH_PRIORITAS":
        lbl_judul_fitur.config(text="LinkedList: pesanan PRIORITAS, menyerobot ke tengah")
        lbl_sub_fitur.config(text="insert: menelusuri hingga pertengahan lalu menyambung pointer")
        lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="TAMBAH", bg="#27ae60", fg="white")

    elif kode_fitur == "LL_TAMBAH_VIP":
        lbl_judul_fitur.config(text="LinkedList: pesanan VIP, langsung ke urutan pertama")
        lbl_sub_fitur.config(text="insert: langsung mengubah penunjuk head")
        lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="TAMBAH", bg="#27ae60", fg="white")

    elif kode_fitur == "LL_HAPUS":
        lbl_judul_fitur.config(text="LinkedList: hapus pesanan ke-i")
        lbl_sub_fitur.config(text="delete: menelusuri node lalu melepas sambungan pointer")
        lbl_index.config(text="Indeks ke-i:")
        lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_index.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        btn_eksekusi.config(text="HAPUS", bg="#c0392b", fg="white")

def eksekusi_fitur():
    # Eksekusi Array
    if fitur_aktif == "ARR_LIHAT_INDEKS":
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
                "ARRAY Indeks ke-" + str(idx) + ":\n"
                + "OID       : " + p.oid + "\n"
                + "Pelanggan : " + p.pelanggan + "\n"
                + "Resto     : " + p.resto + "\n"
                + "Menu      : " + p.menu + "\n"
                + "Harga     : Rp" + str(p.harga) + "\n"
                + "Status    : " + p.status
            )
        else:
            text_hasil.insert(tk.END, "Data tidak ditemukan pada indeks " + str(idx) + "!")

        cetak_log("ARRAY - Lihat Indeks " + str(idx) + " -> Waktu: " + str(round(ms, 4)) + " ms")

    elif fitur_aktif == "ARR_LIHAT_OID":
        target_oid = entry_index.get().strip()

        t1 = time.perf_counter()
        p, idx = data_array.cari_by_oid(target_oid)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000

        text_hasil.delete("1.0", tk.END)
        if p != None:
            text_hasil.insert(
                tk.END,
                "Ditemukan pada Indeks ke-" + str(idx) + ":\n"
                + "OID       : " + p.oid + "\n"
                + "Pelanggan : " + p.pelanggan + "\n"
                + "Resto     : " + p.resto + "\n"
                + "Menu      : " + p.menu + "\n"
                + "Harga     : Rp" + str(p.harga) + "\n"
                + "Status    : " + p.status
            )
        else:
            text_hasil.insert(tk.END, "Pesanan dengan OID '" + target_oid + "' tidak ditemukan!")

        cetak_log("ARRAY - Cari OID '" + target_oid + "' -> Waktu: " + str(round(ms, 4)) + " ms")

    elif fitur_aktif == "ARR_TAMBAH_REGULER":
        p = buat_pesanan_baru(3)
        t1 = time.perf_counter()
        data_array.append(p)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000

        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(tk.END, "Berhasil menambahkan pesanan REGULER di posisi paling belakang:\n" + str(p.oid) + " - " + str(p.pelanggan))
        cetak_log("ARRAY - Tambah Reguler (" + p.oid + ") di belakang -> Waktu: " + str(round(ms, 4)) + " ms")

    elif fitur_aktif == "ARR_TAMBAH_PRIORITAS":
        p = buat_pesanan_baru(2)
        posisi_tengah = data_array.size // 2

        t1 = time.perf_counter()
        data_array.insert(posisi_tengah, p)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000

        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(tk.END, "Berhasil menambahkan pesanan PRIORITAS di indeks " + str(posisi_tengah) + ":\n" + str(p.oid) + " - " + str(p.pelanggan))
        cetak_log("ARRAY - Tambah Prioritas (" + p.oid + ") di tengah (" + str(posisi_tengah) + ") -> Waktu: " + str(round(ms, 4)) + " ms")

    elif fitur_aktif == "ARR_TAMBAH_VIP":
        p = buat_pesanan_baru(1)

        t1 = time.perf_counter()
        data_array.insert(0, p)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000

        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(tk.END, "Berhasil menambahkan pesanan VIP di indeks 0:\n" + str(p.oid) + " - " + str(p.pelanggan))
        cetak_log("ARRAY - Tambah VIP (" + p.oid + ") di depan (idx 0) -> Waktu: " + str(round(ms, 4)) + " ms")

    elif fitur_aktif == "ARR_HAPUS":
        try:
            idx = int(entry_index.get())
        except:
            idx = 0

        t1 = time.perf_counter()
        p = data_array.delete(idx)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000

        text_hasil.delete("1.0", tk.END)
        if p != None:
            text_hasil.insert(tk.END, "Berhasil menghapus pesanan di indeks " + str(idx) + ":\n" + str(p.oid) + " - " + str(p.pelanggan))
            cetak_log("ARRAY - Hapus index " + str(idx) + " (" + p.oid + ") -> Waktu: " + str(round(ms, 4)) + " ms")
        else:
            text_hasil.insert(tk.END, "Gagal menghapus, indeks tidak valid!")
            cetak_log("ARRAY - Hapus gagal, index tidak valid!")

    #Eksekusi Linked List
    elif fitur_aktif == "LL_LIHAT_INDEKS":
        try:
            idx = int(entry_index.get())
        except:
            idx = 0
        t1 = time.perf_counter()
        p = data_ll.get(idx)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000
        text_hasil.delete("1.0", tk.END)
        if p != None:
            text_hasil.insert(
                tk.END,
                "LINKEDLIST Indeks ke-"
                + str(idx)
                + ":\n"
                + "OID       : "
                + p.oid
                + "\nPelanggan : "
                + p.pelanggan
                + "\nMenu      : "
                + p.menu
                + "\nHarga     : Rp"
                + str(p.harga)
                + "\nStatus    : "
                + p.status,
            )
        else:
            text_hasil.insert(
                tk.END, "Data tidak ditemukan pada indeks " + str(idx) + "!"
            )
        cetak_log(
            "LINKEDLIST - Lihat Indeks "
            + str(idx)
            + " -> Waktu: "
            + str(round(ms, 4))
            + " ms"
        )

    elif fitur_aktif == "LL_LIHAT_OID":
        target_oid = entry_index.get().strip()
        t1 = time.perf_counter()
        p, idx = data_ll.cari_by_oid(target_oid)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000
        text_hasil.delete("1.0", tk.END)
        if p != None:
            text_hasil.insert(
                tk.END,
                "Ditemukan pada Indeks ke-"
                + str(idx)
                + ":\n"
                + "OID       : "
                + p.oid
                + "\nPelanggan : "
                + p.pelanggan
                + "\nMenu      : "
                + p.menu
                + "\nHarga     : Rp"
                + str(p.harga)
                + "\nStatus    : "
                + p.status,
            )
        else:
            text_hasil.insert(
                tk.END,
                "Pesanan dengan OID '" + target_oid + "' tidak ditemukan!",
            )
        cetak_log(
            "LINKEDLIST - Cari OID '"
            + target_oid
            + "' -> Waktu: "
            + str(round(ms, 4))
            + " ms"
        )

    elif fitur_aktif == "LL_TAMBAH_REGULER":
        p = buat_pesanan_baru(3)
        t1 = time.perf_counter()
        data_ll.append(p)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000
        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(
            tk.END,
            "Berhasil menambahkan pesanan REGULER di posisi paling belakang:\n"
            + str(p.oid)
            + " - "
            + str(p.pelanggan),
        )
        cetak_log(
            "LINKEDLIST - Tambah Reguler ("
            + p.oid
            + ") di belakang -> Waktu: "
            + str(round(ms, 4))
            + " ms"
        )

    elif fitur_aktif == "LL_TAMBAH_PRIORITAS":
        p = buat_pesanan_baru(2)
        posisi_tengah = data_ll.size // 2
        t1 = time.perf_counter()
        data_ll.insert(posisi_tengah, p)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000
        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(
            tk.END,
            "Berhasil menambahkan pesanan PRIORITAS di indeks "
            + str(posisi_tengah)
            + ":\n"
            + str(p.oid)
            + " - "
            + str(p.pelanggan),
        )
        cetak_log(
            "LINKEDLIST - Tambah Prioritas ("
            + p.oid
            + ") di tengah -> Waktu: "
            + str(round(ms, 4))
            + " ms"
        )

    elif fitur_aktif == "LL_TAMBAH_VIP":
        p = buat_pesanan_baru(1)
        t1 = time.perf_counter()
        data_ll.insert(0, p)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000
        text_hasil.delete("1.0", tk.END)
        text_hasil.insert(
            tk.END,
            "Berhasil menambahkan pesanan VIP di indeks 0:\n"
            + str(p.oid)
            + " - "
            + str(p.pelanggan),
        )
        cetak_log(
            "LINKEDLIST - Tambah VIP ("
            + p.oid
            + ") di depan (0) -> Waktu: "
            + str(round(ms, 4))
            + " ms"
        )

    elif fitur_aktif == "LL_HAPUS":
        try:
            idx = int(entry_index.get())
        except:
            idx = 0
        t1 = time.perf_counter()
        p = data_ll.delete(idx)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000
        text_hasil.delete("1.0", tk.END)
        if p != None:
            text_hasil.insert(
                tk.END,
                "Berhasil menghapus pesanan di indeks "
                + str(idx)
                + ":\n"
                + str(p.oid)
                + " - "
                + str(p.pelanggan),
            )
            cetak_log(
                "LINKEDLIST - Hapus index "
                + str(idx)
                + " ("
                + p.oid
                + ") -> Waktu: "
                + str(round(ms, 4))
                + " ms"
            )
        else:
            text_hasil.insert(
                tk.END, "Gagal menghapus, indeks tidak valid!"
            )
            cetak_log("LINKEDLIST - Hapus gagal, index tidak valid!")

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

frame_kiri = tk.Frame(frame_utama, width=250, bd=1, relief=tk.SOLID)
frame_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

# --- KELOMPOK M1: DATA PESANAN ---
lbl_m1 = tk.Label(frame_kiri, text="M1 - DATA PESANAN", font=("Arial", 8, "bold"), fg="#555555", anchor="w")
lbl_m1.pack(fill=tk.X, padx=8, pady=(8, 2))

# Tombol Fitur Array
tk.Button(frame_kiri, 
    text="ARRAY - LIHAT (INDEKS)", 
    anchor="w", font=("Arial", 9), 
    bg="#f8f9fa", 
    bd=1, 
    command=lambda: pilih_fitur("ARR_LIHAT_INDEKS")
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(frame_kiri, 
    text="ARRAY - LIHAT (OID)", 
    anchor="w", 
    font=("Arial", 9), 
    bg="#f8f9fa", 
    bd=1, 
    command=lambda: pilih_fitur("ARR_LIHAT_OID")
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(frame_kiri,
    text="ARRAY - TAMBAH PESANAN REGULER", 
    anchor="w", 
    font=("Arial", 9), 
    bg="#f8f9fa", 
    bd=1, 
    command=lambda: pilih_fitur("ARR_TAMBAH_REGULER")
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(frame_kiri,
    text="ARRAY - TAMBAH PESANAN PRIORITAS", 
    anchor="w", 
    font=("Arial", 9), 
    bg="#f8f9fa", 
    bd=1, 
    command=lambda: pilih_fitur("ARR_TAMBAH_PRIORITAS")
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(frame_kiri,
    text="ARRAY - TAMBAH PESANAN VIP", 
    anchor="w", 
    font=("Arial", 9), 
    bg="#f8f9fa", 
    bd=1, 
    command=lambda: pilih_fitur("ARR_TAMBAH_VIP")
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(frame_kiri, 
    text="ARRAY - HAPUS PESANAN", 
    anchor="w", 
    font=("Arial", 9), 
    bg="#f8f9fa", 
    bd=1, 
    command=lambda: pilih_fitur("ARR_HAPUS")
).pack(fill=tk.X, padx=8, pady=1)

# Tombol Fitur Linked List
tk.Button(frame_kiri,
    text="LINKEDLIST - LIHAT (INDEKS)",
    anchor="w",
    font=("Arial", 9),
    bg="#f8f9fa",
    bd=1,
    command=lambda: pilih_fitur("LL_LIHAT_INDEKS"),
).pack(fill=tk.X, padx=8, pady=(6, 1))
tk.Button(
    frame_kiri,
    text="LINKEDLIST - LIHAT (OID)",
    anchor="w",
    font=("Arial", 9),
    bg="#f8f9fa",
    bd=1,
    command=lambda: pilih_fitur("LL_LIHAT_OID"),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text="LINKEDLIST - TAMBAH REGULER",
    anchor="w",
    font=("Arial", 9),
    bg="#f8f9fa",
    bd=1,
    command=lambda: pilih_fitur("LL_TAMBAH_REGULER"),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text="LINKEDLIST - TAMBAH PRIORITAS",
    anchor="w",
    font=("Arial", 9),
    bg="#f8f9fa",
    bd=1,
    command=lambda: pilih_fitur("LL_TAMBAH_PRIORITAS"),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text="LINKEDLIST - TAMBAH VIP",
    anchor="w",
    font=("Arial", 9),
    bg="#f8f9fa",
    bd=1,
    command=lambda: pilih_fitur("LL_TAMBAH_VIP"),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text="LINKEDLIST - HAPUS PESANAN",
    anchor="w",
    font=("Arial", 9),
    bg="#f8f9fa",
    bd=1,
    command=lambda: pilih_fitur("LL_HAPUS"),
).pack(fill=tk.X, padx=8, pady=1)

frame_kanan = tk.Frame(frame_utama)
frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

lbl_judul_fitur = tk.Label(frame_kanan, text="Array: lihat pesanan ke-i", font=("Arial", 11, "bold"), anchor="w")
lbl_judul_fitur.pack(fill=tk.X, pady=(5,0))

lbl_sub_fitur = tk.Label(frame_kanan, text="get: mengambil data pesanan pada indeks tertentu", font=("Arial", 9, "italic"),fg="gray", anchor="w")
lbl_sub_fitur.pack(fill=tk.X, pady=(0,5))

frame_form = tk.Frame(frame_kanan, bd=1, relief=tk.SOLID)
frame_form.pack(fill=tk.X, pady=5)

lbl_nama = tk.Label(frame_form, text="Nama pelanggan:")
entry_nama = tk.Entry(frame_form, width=30)
entry_nama.insert(0, "Pelanggan Baru")

lbl_index = tk.Label(frame_form, text="Indeks ke-i:")
entry_index = tk.Entry(frame_form, width=15)
entry_index.insert(0, "0")

btn_eksekusi = tk.Button(
    frame_form, text="LIHAT", font=("Arial", 9, "bold"), width=12, command=eksekusi_fitur
)
btn_eksekusi.grid(row=0, column=2, padx=15, pady=5)

text_hasil = tk.Text(frame_kanan, height=8)
text_hasil.pack(fill=tk.BOTH, expand=True, pady=5)

frame_log = tk.LabelFrame(frame_kanan, text="COMMAND LOG & WAKTU")
frame_log.pack(fill=tk.X, side=tk.BOTTOM)

text_log = tk.Text(frame_log, height=6, bg="black", fg="lime", font=("Consolas", 9))
text_log.pack(fill=tk.BOTH, expand=True)

pilih_fitur("ARR_LIHAT_INDEKS")  # Set default fitur aktif ke LIHAT

root.mainloop()