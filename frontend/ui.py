import csv
import os
import sys
import time
import tkinter as tk
from tkinter import ttk

# Import Backend M1 & M2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.m1_pesanan import Array, LinkList, Pesanan
from backend.m2_antrean import ke_postfix, hitung_postfix

# Global Variable M1
data_array = Array()
data_ll = LinkList()

id_baru = 200001
fitur_aktif = 'ARR_LIHAT_INDEKS'


def cetak_log(pesan):
  text_log.insert(tk.END, pesan + '\n')
  text_log.see(tk.END)


def tombol_load_csv():
  global data_array, data_ll, q_naif, q_circ, undo_stack, redo_stack
  data_array = Array()
  data_ll = LinkList()
  q_naif = AntreanNaif()
  q_circ = AntreanMelingkar()
  undo_stack = Stack()
  redo_stack = Stack()

  path_file = 'data/pesanan.csv'
  if not os.path.exists(path_file):
    path_file = 'pesanan.csv'

  if not os.path.exists(path_file):
    cetak_log('Error: File pesanan.csv tidak ditemukan!')
    return

  t1 = time.perf_counter()
  f = open(path_file, 'r', encoding='utf-8')
  reader = csv.reader(f)
  header = next(reader)

  count = 0
  for row in reader:
    p = Pesanan(
        row[0],
        row[1],
        row[2],
        row[3],
        row[4],
        row[5],
        row[6],
        row[7],
        row[8],
    )
    data_array.append(p)
    data_ll.append(p)

    # Masukkan otomatis pesanan berstatus ANTRE ke dalam dua antrean
    if p.status == 'ANTRE':
      q_naif.enqueue(p)
      q_circ.enqueue(p)

    count += 1

  f.close()
  t2 = time.perf_counter()
  ms = (t2 - t1) * 1000

  label_status.config(
      text=f'Status: {count} data dimuat | Antrean ANTRE: {q_circ.size()}'
  )
  cetak_log(f'Load CSV Selesai ({count} data) -> Waktu: {round(ms, 2)} ms')


def buat_pesanan_baru(prioritas):
  global id_baru
  oid = 'O-' + str(id_baru)
  id_baru += 1
  nama = entry_nama.get() if entry_nama.get() != '' else 'Pelanggan Baru'
  return Pesanan(
      oid,
      nama,
      'kafe-teknik',
      'roti-bakar',
      '12000',
      str(prioritas),
      '08:00:00',
      '-',
      'ANTRE',
  )


def pilih_fitur(kode_fitur):
  global fitur_aktif
  fitur_aktif = kode_fitur

  lbl_nama.grid_forget()
  entry_nama.grid_forget()
  lbl_index.grid_forget()
  entry_index.grid_forget()

  # --- M1 FITUR ---
  if kode_fitur == 'ARR_LIHAT_INDEKS':
    lbl_judul_fitur.config(text='Array: lihat pesanan berdasarkan Indeks (i)')
    lbl_sub_fitur.config(
        text='get: mengambil data pesanan pada indeks posisi tertentu'
    )
    lbl_index.config(text='Indeks ke-i:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='CARI', bg='#0056b3', fg='white')

  elif kode_fitur == 'ARR_LIHAT_OID':
    lbl_judul_fitur.config(text='Array: lihat pesanan berdasarkan OID')
    lbl_sub_fitur.config(text='cari_by_oid: pencarian linier berdasarkan ID')
    lbl_index.config(text='OID Pesanan:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='CARI', bg='#0056b3', fg='white')

  elif kode_fitur == 'ARR_TAMBAH_REGULER':
    lbl_judul_fitur.config(text='Array: pesanan REGULER, masuk paling belakang')
    lbl_sub_fitur.config(
        text='append: pesanan biasa, mengantre di barisan paling belakang'
    )
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='TAMBAH', bg='#0056b3', fg='white')

  elif kode_fitur == 'ARR_TAMBAH_PRIORITAS':
    lbl_judul_fitur.config(
        text='Array: pesanan PRIORITAS, menyerobot ke tengah'
    )
    lbl_sub_fitur.config(text='insert: disisipkan tepat di pertengahan barisan')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='TAMBAH', bg='#0056b3', fg='white')

  elif kode_fitur == 'ARR_TAMBAH_VIP':
    lbl_judul_fitur.config(
        text='Array: pesanan VIP, langsung ke urutan pertama'
    )
    lbl_sub_fitur.config(text='insert: disisipkan paling depan (indeks 0)')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='TAMBAH', bg='#0056b3', fg='white')

  elif kode_fitur == 'ARR_HAPUS':
    lbl_judul_fitur.config(text='Array: hapus pesanan ke-i')
    lbl_sub_fitur.config(
        text='delete: mencabut pesanan dari barisan pada indeks tertentu'
    )
    lbl_index.config(text='Indeks ke-i:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='HAPUS', bg='#c0392b', fg='white')

  elif kode_fitur == 'LL_LIHAT_INDEKS':
    lbl_judul_fitur.config(
        text='LinkedList: lihat pesanan berdasarkan Indeks (i)'
    )
    lbl_sub_fitur.config(
        text='get: menelusuri node dari head sampai indeks posisi tertentu'
    )
    lbl_index.config(text='Indeks ke-i:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='CARI', bg='#27ae60', fg='white')

  elif kode_fitur == 'LL_LIHAT_OID':
    lbl_judul_fitur.config(text='LinkedList: lihat pesanan berdasarkan OID')
    lbl_sub_fitur.config(
        text='cari_by_oid: menelusuri node berdasarkan ID Pesanan'
    )
    lbl_index.config(text='OID Pesanan:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='CARI', bg='#27ae60', fg='white')

  elif kode_fitur == 'LL_TAMBAH_REGULER':
    lbl_judul_fitur.config(
        text='LinkedList: pesanan REGULER, masuk paling belakang'
    )
    lbl_sub_fitur.config(text='append: langsung disambung via tail pointer')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='TAMBAH', bg='#27ae60', fg='white')

  elif kode_fitur == 'LL_TAMBAH_PRIORITAS':
    lbl_judul_fitur.config(
        text='LinkedList: pesanan PRIORITAS, menyerobot ke tengah'
    )
    lbl_sub_fitur.config(
        text='insert: menelusuri hingga pertengahan lalu menyambung pointer'
    )
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='TAMBAH', bg='#27ae60', fg='white')

  elif kode_fitur == 'LL_TAMBAH_VIP':
    lbl_judul_fitur.config(
        text='LinkedList: pesanan VIP, langsung ke urutan pertama'
    )
    lbl_sub_fitur.config(text='insert: langsung mengubah penunjuk head')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='TAMBAH', bg='#27ae60', fg='white')

  elif kode_fitur == 'LL_HAPUS':
    lbl_judul_fitur.config(text='LinkedList: hapus pesanan ke-i')
    lbl_sub_fitur.config(
        text='delete: menelusuri node lalu melepas sambungan pointer'
    )
    lbl_index.config(text='Indeks ke-i:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    btn_eksekusi.config(text='HAPUS', bg='#c0392b', fg='white')

  # --- M2 FITUR ---
  elif kode_fitur == "M2_POSTFIX":
        lbl_judul_fitur.config(text="Stack: hitung struk lewat postfix")
        lbl_sub_fitur.config(
            text="Struk ditulis infix, lalu dihitung dua tahap dengan stack (Infix -> Postfix -> Evaluasi)"
        )
        lbl_nama.config(text="Struk belanja (infix):")
        lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky="w")
        entry_nama.delete(0, tk.END)
        entry_nama.insert(0, "(3*12000)+(2*8500)-5000")
        btn_eksekusi.config(text="HITUNG", bg="#0056b3", fg="white")


def eksekusi_fitur():
  global q_naif, q_circ, undo_stack, redo_stack

  # --- EKSEKUSI M1 ---
  if fitur_aktif == 'ARR_LIHAT_INDEKS':
    try:
      idx = int(entry_index.get())
    except:
      idx = 0
    t1 = time.perf_counter()
    p = data_array.get(idx)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    if p != None:
      text_hasil.insert(
          tk.END,
          f'ARRAY Indeks ke-{idx}:\nOID       : {p.oid}\nPelanggan :'
          f' {p.pelanggan}\nMenu      : {p.menu}\nHarga     :'
          f' Rp{p.harga}\nStatus    : {p.status}',
      )
    else:
      text_hasil.insert(
          tk.END, f'Data tidak ditemukan pada indeks {idx}!'
      )
    cetak_log(f'ARRAY - Lihat Indeks {idx} -> Waktu: {round(ms, 4)} ms')

  elif fitur_aktif == 'ARR_LIHAT_OID':
    target_oid = entry_index.get().strip()
    t1 = time.perf_counter()
    p, idx = data_array.cari_by_oid(target_oid)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    if p != None:
      text_hasil.insert(
          tk.END,
          f'Ditemukan pada Indeks ke-{idx}:\nOID       : {p.oid}\nPelanggan :'
          f' {p.pelanggan}\nMenu      : {p.menu}\nHarga     :'
          f' Rp{p.harga}\nStatus    : {p.status}',
      )
    else:
      text_hasil.insert(
          tk.END, f"Pesanan dengan OID '{target_oid}' tidak ditemukan!"
      )
    cetak_log(f"ARRAY - Cari OID '{target_oid}' -> Waktu: {round(ms, 4)} ms")

  elif fitur_aktif == 'ARR_TAMBAH_REGULER':
    p = buat_pesanan_baru(3)
    t1 = time.perf_counter()
    data_array.append(p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        'Berhasil menambahkan pesanan REGULER di posisi paling belakang:\n'
        f'{p.oid} - {p.pelanggan}',
    )
    cetak_log(
        f'ARRAY - Tambah Reguler ({p.oid}) di belakang -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  elif fitur_aktif == 'ARR_TAMBAH_PRIORITAS':
    p = buat_pesanan_baru(2)
    pos = data_array.size // 2
    t1 = time.perf_counter()
    data_array.insert(pos, p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        f'Berhasil menambahkan pesanan PRIORITAS di indeks {pos}:\n{p.oid} -'
        f' {p.pelanggan}',
    )
    cetak_log(
        f'ARRAY - Tambah Prioritas ({p.oid}) di tengah -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  elif fitur_aktif == 'ARR_TAMBAH_VIP':
    p = buat_pesanan_baru(1)
    t1 = time.perf_counter()
    data_array.insert(0, p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        f'Berhasil menambahkan pesanan VIP di indeks 0:\n{p.oid} - {p.pelanggan}',
    )
    cetak_log(
        f'ARRAY - Tambah VIP ({p.oid}) di depan (0) -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  elif fitur_aktif == 'ARR_HAPUS':
    try:
      idx = int(entry_index.get())
    except:
      idx = 0
    t1 = time.perf_counter()
    p = data_array.delete(idx)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    if p != None:
      text_hasil.insert(
          tk.END,
          f'Berhasil menghapus pesanan di indeks {idx}:\n{p.oid} - {p.pelanggan}',
      )
      cetak_log(
          f'ARRAY - Hapus index {idx} ({p.oid}) -> Waktu: {round(ms, 4)} ms'
      )
    else:
      text_hasil.insert(tk.END, 'Gagal menghapus, indeks tidak valid!')

  elif fitur_aktif == 'LL_LIHAT_INDEKS':
    try:
      idx = int(entry_index.get())
    except:
      idx = 0
    t1 = time.perf_counter()
    p = data_ll.get(idx)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    if p != None:
      text_hasil.insert(
          tk.END,
          f'LINKEDLIST Indeks ke-{idx}:\nOID       : {p.oid}\nPelanggan :'
          f' {p.pelanggan}\nMenu      : {p.menu}\nHarga     :'
          f' Rp{p.harga}\nStatus    : {p.status}',
      )
    else:
      text_hasil.insert(
          tk.END, f'Data tidak ditemukan pada indeks {idx}!'
      )
    cetak_log(f'LINKEDLIST - Lihat Indeks {idx} -> Waktu: {round(ms, 4)} ms')

  elif fitur_aktif == 'LL_LIHAT_OID':
    target_oid = entry_index.get().strip()
    t1 = time.perf_counter()
    p, idx = data_ll.cari_by_oid(target_oid)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    if p != None:
      text_hasil.insert(
          tk.END,
          f'Ditemukan pada Indeks ke-{idx}:\nOID       : {p.oid}\nPelanggan :'
          f' {p.pelanggan}\nMenu      : {p.menu}\nHarga     :'
          f' Rp{p.harga}\nStatus    : {p.status}',
      )
    else:
      text_hasil.insert(
          tk.END, f"Pesanan dengan OID '{target_oid}' tidak ditemukan!"
      )
    cetak_log(f"LINKEDLIST - Cari OID '{target_oid}' -> Waktu: {round(ms, 4)} ms")

  elif fitur_aktif == 'LL_TAMBAH_REGULER':
    p = buat_pesanan_baru(3)
    t1 = time.perf_counter()
    data_ll.append(p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        'Berhasil menambahkan pesanan REGULER di posisi paling belakang:\n'
        f'{p.oid} - {p.pelanggan}',
    )
    cetak_log(
        f'LINKEDLIST - Tambah Reguler ({p.oid}) di belakang -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  elif fitur_aktif == 'LL_TAMBAH_PRIORITAS':
    p = buat_pesanan_baru(2)
    pos = data_ll.size // 2
    t1 = time.perf_counter()
    data_ll.insert(pos, p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        f'Berhasil menambahkan pesanan PRIORITAS di indeks {pos}:\n{p.oid} -'
        f' {p.pelanggan}',
    )
    cetak_log(
        f'LINKEDLIST - Tambah Prioritas ({p.oid}) di tengah -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  elif fitur_aktif == 'LL_TAMBAH_VIP':
    p = buat_pesanan_baru(1)
    t1 = time.perf_counter()
    data_ll.insert(0, p)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        f'Berhasil menambahkan pesanan VIP di indeks 0:\n{p.oid} - {p.pelanggan}',
    )
    cetak_log(
        f'LINKEDLIST - Tambah VIP ({p.oid}) di depan (0) -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  elif fitur_aktif == 'LL_HAPUS':
    try:
      idx = int(entry_index.get())
    except:
      idx = 0
    t1 = time.perf_counter()
    p = data_ll.delete(idx)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000
    text_hasil.delete('1.0', tk.END)
    if p != None:
      text_hasil.insert(
          tk.END,
          f'Berhasil menghapus pesanan di indeks {idx}:\n{p.oid} - {p.pelanggan}',
      )
      cetak_log(
          f'LINKEDLIST - Hapus index {idx} ({p.oid}) -> Waktu: {round(ms, 4)} ms'
      )
    else:
      text_hasil.insert(tk.END, 'Gagal menghapus, indeks tidak valid!')

  elif fitur_aktif == "M2_POSTFIX":
        expr = entry_nama.get().strip()
        t1 = time.perf_counter()
        postfix_tokens, log_1 = ke_postfix(expr)
        total, log_2 = hitung_postfix(postfix_tokens)
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000

        # 1. Tampilkan Ringkasan Teks Atas
        text_ringkasan = (
            f"Struk : {expr}\n"
            f"Postfix: {' '.join(postfix_tokens)}\n"
            f"TOTAL : Rp {total:,}"
        )
        lbl_ringkasan.config(text=text_ringkasan)

        # 2. Sembunyikan Text biasa & Tampilkan Tabel Treeview
        text_hasil.pack_forget()
        frame_tabel.pack(fill=tk.BOTH, expand=True, pady=5)

        # 3. Konfigurasi Kolom Tabel
        kolom = ("langkah", "token", "tindakan", "stack", "output")
        tree_hasil["columns"] = kolom

        tree_hasil.heading("langkah", text="langkah", anchor="w")
        tree_hasil.heading("token", text="token", anchor="w")
        tree_hasil.heading("tindakan", text="tindakan", anchor="w")
        tree_hasil.heading("stack", text="stack", anchor="w")
        tree_hasil.heading("output", text="output", anchor="w")

        tree_hasil.column("langkah", width=70, minwidth=60)
        tree_hasil.column("token", width=60, minwidth=50)
        tree_hasil.column("tindakan", width=280, minwidth=200)
        tree_hasil.column("stack", width=120, minwidth=100)
        tree_hasil.column("output", width=200, minwidth=150)

        # 4. Bersihkan data tabel lama
        for item in tree_hasil.get_children():
            tree_hasil.delete(item)

        # 5. Isi Tahap 1: Konversi Infix ke Postfix (1.1, 1.2, dst)
        idx = 1
        for tkn, tin, stk, out in log_1:
            lbl_step = f"1.{idx}" if idx != len(log_1) else "1.akhir"
            tree_hasil.insert("", tk.END, values=(lbl_step, tkn, tin, stk, out))
            idx += 1

        # 6. Isi Tahap 2: Evaluasi Postfix (2.1, 2.2, dst)
        idx_eval = 1
        for tkn, tin, stk in log_2:
            tree_hasil.insert("", tk.END, values=(f"2.{idx_eval}", tkn, tin, stk, stk))
            idx_eval += 1

        cetak_log(f"M2 - Stack Postfix (Mesin Kasir) -> Waktu: {round(ms, 4)} ms")
# --- UI SETUP TKINTER ---
root = tk.Tk()
root.title('2EZ4U Food Delivery')
root.geometry('900x600')

frame_atas = tk.Frame(root, bg='lightblue')
frame_atas.pack(fill=tk.X)

btn_load = tk.Button(
    frame_atas,
    text='Load Data CSV',
    command=tombol_load_csv,
    bg='green',
    fg='white',
)
btn_load.pack(side=tk.LEFT, padx=10, pady=5)

label_status = tk.Label(frame_atas, text='Status: Belum ada data', bg='lightblue')
label_status.pack(side=tk.LEFT, padx=10)

frame_utama = tk.Frame(root)
frame_utama.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

frame_kiri = tk.Frame(frame_utama, width=260, bd=1, relief=tk.SOLID)
frame_kiri.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

# --- KELOMPOK M1 ---
lbl_m1 = tk.Label(
    frame_kiri,
    text='M1 - DATA PESANAN',
    font=('Arial', 8, 'bold'),
    fg='#555555',
    anchor='w',
)
lbl_m1.pack(fill=tk.X, padx=8, pady=(8, 2))

tk.Button(
    frame_kiri,
    text='ARRAY - LIHAT (INDEKS)',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('ARR_LIHAT_INDEKS'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='ARRAY - LIHAT (OID)',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('ARR_LIHAT_OID'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='ARRAY - TAMBAH PESANAN REGULER',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('ARR_TAMBAH_REGULER'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='ARRAY - TAMBAH PESANAN PRIORITAS',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('ARR_TAMBAH_PRIORITAS'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='ARRAY - TAMBAH PESANAN VIP',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('ARR_TAMBAH_VIP'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='ARRAY - HAPUS PESANAN',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('ARR_HAPUS'),
).pack(fill=tk.X, padx=8, pady=1)

tk.Button(
    frame_kiri,
    text='LINKEDLIST - LIHAT (INDEKS)',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('LL_LIHAT_INDEKS'),
).pack(fill=tk.X, padx=8, pady=(6, 1))
tk.Button(
    frame_kiri,
    text='LINKEDLIST - LIHAT (OID)',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('LL_LIHAT_OID'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='LINKEDLIST - TAMBAH REGULER',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('LL_TAMBAH_REGULER'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='LINKEDLIST - TAMBAH PRIORITAS',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('LL_TAMBAH_PRIORITAS'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='LINKEDLIST - TAMBAH VIP',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('LL_TAMBAH_VIP'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='LINKEDLIST - HAPUS PESANAN',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('LL_HAPUS'),
).pack(fill=tk.X, padx=8, pady=1)

# --- KELOMPOK M2: STACK ---
lbl_m2 = tk.Label(frame_kiri, text="M2 - STACK DAN QUEUE", font=("Arial", 8, "bold"), fg="#555555", anchor="w")
lbl_m2.pack(fill=tk.X, padx=8, pady=(12, 2))

tk.Button(
    frame_kiri,
    text="STACK - POSTFIX (MESIN KASIR)",
    anchor="w",
    font=("Arial", 9),
    bg="#f8f9fa",
    bd=1,
    command=lambda: pilih_fitur("M2_POSTFIX")
).pack(fill=tk.X, padx=8, pady=1)

# Frame Kanan
frame_kanan = tk.Frame(frame_utama)
frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

lbl_judul_fitur = tk.Label(
    frame_kanan,
    text='Array: lihat pesanan ke-i',
    font=('Arial', 11, 'bold'),
    anchor='w',
)
lbl_judul_fitur.pack(fill=tk.X, pady=(5, 0))

lbl_sub_fitur = tk.Label(
    frame_kanan,
    text='get: mengambil data pesanan pada indeks tertentu',
    font=('Arial', 9, 'italic'),
    fg='gray',
    anchor='w',
)
lbl_sub_fitur.pack(fill=tk.X, pady=(0, 5))

frame_form = tk.Frame(frame_kanan, bd=1, relief=tk.SOLID)
frame_form.pack(fill=tk.X, pady=5)

lbl_nama = tk.Label(frame_form, text='Nama pelanggan:')
entry_nama = tk.Entry(frame_form, width=30)
entry_nama.insert(0, 'Pelanggan Baru')

lbl_index = tk.Label(frame_form, text='Indeks ke-i:')
entry_index = tk.Entry(frame_form, width=15)
entry_index.insert(0, '0')

btn_eksekusi = tk.Button(
    frame_form,
    text='LIHAT',
    font=('Arial', 9, 'bold'),
    width=12,
    command=eksekusi_fitur,
)
btn_eksekusi.grid(row=0, column=2, padx=15, pady=5)

# --- FRAME KANAN (HASIL & TABEL) ---
frame_kanan = tk.Frame(frame_utama)
frame_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

lbl_judul_fitur = tk.Label(frame_kanan, text="Stack: hitung struk lewat postfix", font=("Arial", 11, "bold"), anchor="w")
lbl_judul_fitur.pack(fill=tk.X, pady=(5, 0))

lbl_sub_fitur = tk.Label(frame_kanan, text="Struk ditulis infix, lalu dihitung dua tahap dengan stack", font=("Arial", 9, "italic"), fg="gray", anchor="w")
lbl_sub_fitur.pack(fill=tk.X, pady=(0, 5))

# Form Input
frame_form = tk.Frame(frame_kanan, bd=1, relief=tk.SOLID)
frame_form.pack(fill=tk.X, pady=5)

lbl_nama = tk.Label(frame_form, text="Struk belanja (infix):")
entry_nama = tk.Entry(frame_form, width=35)
entry_nama.insert(0, "( 3 * 12000 ) + ( 2 * 8500 ) - 5000")

lbl_index = tk.Label(frame_form, text="Indeks ke-i:")
entry_index = tk.Entry(frame_form, width=15)
entry_index.insert(0, "0")

btn_eksekusi = tk.Button(frame_form, text="HITUNG", font=("Arial", 9, "bold"), width=12, command=lambda: eksekusi_fitur())
btn_eksekusi.grid(row=0, column=2, padx=15, pady=5)

# --- AREA RINGKASAN TEKS ---
lbl_ringkasan = tk.Label(frame_kanan, text="", font=("Arial", 10), justify="left", anchor="w")
lbl_ringkasan.pack(fill=tk.X, pady=5)

# --- AREA TABEL BERKOLOM (TREEVIEW) ---
frame_tabel = tk.Frame(frame_kanan)
frame_tabel.pack(fill=tk.BOTH, expand=True, pady=5)

tree_hasil = ttk.Treeview(frame_tabel, show="headings")
scroll_y = ttk.Scrollbar(frame_tabel, orient="vertical", command=tree_hasil.yview)
scroll_x = ttk.Scrollbar(frame_tabel, orient="horizontal", command=tree_hasil.xview)
tree_hasil.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
tree_hasil.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Widget Text Alternatif (Tetap disimpan bila butuh output teks biasa)
text_hasil = tk.Text(frame_kanan, height=8)

frame_log = tk.LabelFrame(frame_kanan, text='COMMAND LOG & WAKTU')
frame_log.pack(fill=tk.X, side=tk.BOTTOM)

text_log = tk.Text(frame_log, height=5, bg='black', fg='lime', font=('Consolas', 9))
text_log.pack(fill=tk.BOTH, expand=True)

pilih_fitur('ARR_LIHAT_INDEKS')
root.mainloop()