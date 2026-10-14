import csv
import os
import sys
import time
import tkinter as tk
from tkinter import ttk

# Import Backend M1 & M2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.m1_pesanan import Array, LinkList, Pesanan
from backend.m2_antrean import (
    AntreanMelingkar,
    AntreanNaif,
    Stack,
    hitung_postfix,
    ke_postfix,
)
from backend.m3_laporan import insertion_sort

# Global Variable M1
data_array = Array()
data_ll = LinkList()

# Global Variable M2
q_naif = AntreanNaif()
q_circ = AntreanMelingkar()
undo_stack = Stack()
redo_stack = Stack()

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
  count_antre = 0
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

    if p.status == 'ANTRE':
      q_naif.enqueue(p)
      q_circ.enqueue(p)
      count_antre += 1

    count += 1

  f.close()
  t2 = time.perf_counter()
  ms = (t2 - t1) * 1000

  label_status.config(
      text=f'Status: {count} data dimuat | Antrean ANTRE: {count_antre}'
  )
  cetak_log(
      f'Load CSV Selesai ({count} data, {count_antre} ANTRE) -> Waktu:'
      f' {round(ms, 2)} ms'
  )


def buat_pesanan_baru(prioritas):
  global id_baru
  oid = 'O-' + str(id_baru)
  id_baru += 1
  nama = entry_nama.get().strip()
  if not nama:
    nama = 'Pelanggan Baru'
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


def reset_input_form():
  entry_nama.delete(0, tk.END)
  entry_nama.insert(0, 'Pelanggan Baru')
  entry_index.delete(0, tk.END)
  entry_index.insert(0, '1')


def tampilkan_tabel_pesanan(daftar_pesanan):
  text_hasil.pack_forget()
  lbl_ringkasan.pack_forget()
  frame_tabel.pack(fill=tk.BOTH, expand=True, pady=5)

  kolom = ('no', 'oid', 'pelanggan', 'resto', 'menu', 'harga', 'status')
  tree_hasil['columns'] = kolom
  for c in kolom:
    tree_hasil.heading(c, text=c, anchor='w')

  tree_hasil.column('no', width=40, minwidth=30)
  tree_hasil.column('oid', width=90, minwidth=70)
  tree_hasil.column('pelanggan', width=150, minwidth=100)
  tree_hasil.column('resto', width=120, minwidth=90)
  tree_hasil.column('menu', width=120, minwidth=90)
  tree_hasil.column('harga', width=80, minwidth=60)
  tree_hasil.column('status', width=80, minwidth=60)

  for item in tree_hasil.get_children():
    tree_hasil.delete(item)

  for idx, p in enumerate(daftar_pesanan, 1):
    tree_hasil.insert(
        '',
        tk.END,
        values=(idx, p.oid, p.pelanggan, p.resto, p.menu, p.harga, p.status),
    )


def pilih_fitur(kode_fitur):
  global fitur_aktif
  fitur_aktif = kode_fitur

  # Sembunyikan elemen form
  lbl_nama.grid_forget()
  entry_nama.grid_forget()
  lbl_index.grid_forget()
  entry_index.grid_forget()
  combo_kunci.grid_forget()

  # Reset posisi tombol ke kolom 2 (default untuk fitur lainnya)
  entry_nama.config(width=35)
  entry_index.config(width=15)
  btn_eksekusi.grid(row=0, column=2, padx=15, pady=5)

  # Reset Tampilan Output ke mode Teks biasa
  lbl_ringkasan.config(text='')
  lbl_ringkasan.pack_forget()
  frame_tabel.pack_forget()
  text_hasil.pack(fill=tk.BOTH, expand=True, pady=5)

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
    lbl_nama.config(text='Nama pelanggan:')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    reset_input_form()
    btn_eksekusi.config(text='TAMBAH', bg='#0056b3', fg='white')

  elif kode_fitur == 'ARR_TAMBAH_PRIORITAS':
    lbl_judul_fitur.config(
        text='Array: pesanan PRIORITAS, menyerobot ke tengah'
    )
    lbl_sub_fitur.config(text='insert: disisipkan tepat di pertengahan barisan')
    lbl_nama.config(text='Nama pelanggan:')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    reset_input_form()
    btn_eksekusi.config(text='TAMBAH', bg='#0056b3', fg='white')

  elif kode_fitur == 'ARR_TAMBAH_VIP':
    lbl_judul_fitur.config(
        text='Array: pesanan VIP, langsung ke urutan pertama'
    )
    lbl_sub_fitur.config(text='insert: disisipkan paling depan (indeks 0)')
    lbl_nama.config(text='Nama pelanggan:')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    reset_input_form()
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
    lbl_nama.config(text='Nama pelanggan:')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    reset_input_form()
    btn_eksekusi.config(text='TAMBAH', bg='#27ae60', fg='white')

  elif kode_fitur == 'LL_TAMBAH_PRIORITAS':
    lbl_judul_fitur.config(
        text='LinkedList: pesanan PRIORITAS, menyerobot ke tengah'
    )
    lbl_sub_fitur.config(
        text='insert: menelusuri hingga pertengahan lalu menyambung pointer'
    )
    lbl_nama.config(text='Nama pelanggan:')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    reset_input_form()
    btn_eksekusi.config(text='TAMBAH', bg='#27ae60', fg='white')

  elif kode_fitur == 'LL_TAMBAH_VIP':
    lbl_judul_fitur.config(
        text='LinkedList: pesanan VIP, langsung ke urutan pertama'
    )
    lbl_sub_fitur.config(text='insert: langsung mengubah penunjuk head')
    lbl_nama.config(text='Nama pelanggan:')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    reset_input_form()
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
  elif kode_fitur == 'M2_POSTFIX':
    lbl_judul_fitur.config(text='Stack: hitung struk lewat postfix')
    lbl_sub_fitur.config(
        text=(
            'Struk ditulis infix, lalu dihitung dua tahap dengan stack: tahap'
            ' 1 infix ke postfix, tahap 2 evaluasi.'
        )
    )
    lbl_nama.config(text='Struk belanja (infix):')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    entry_nama.delete(0, tk.END)
    entry_nama.insert(0, '( 3 * 12000 ) + ( 2 * 8500 ) - 5000')
    btn_eksekusi.config(text='HITUNG', bg='#0056b3', fg='white')

  elif kode_fitur == 'M2_UNDO':
    lbl_judul_fitur.config(text='Stack: batalkan aksi perubahan terakhir')
    lbl_sub_fitur.config(
        text='Mengambil catatan teratas tumpukan undo, lalu membatalkannya.'
    )
    btn_eksekusi.config(text='UNDO', bg='#e67e22', fg='white')

  elif kode_fitur == 'M2_REDO':
    lbl_judul_fitur.config(text='Stack: kerjakan lagi aksi yang dibatalkan')
    lbl_sub_fitur.config(
        text='Mengambil catatan teratas tumpukan redo, lalu mengerjakan ulang.'
    )
    btn_eksekusi.config(text='REDO', bg='#2980b9', fg='white')

  elif kode_fitur == 'M2_ENQUEUE':
    lbl_judul_fitur.config(text='Queue: pesanan baru masuk ke belakang')
    lbl_sub_fitur.config(
        text='Menambah pesanan di ujung belakang kedua antrean sekaligus.'
    )
    lbl_nama.config(text='Nama pelanggan:')
    lbl_nama.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nama.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    reset_input_form()
    btn_eksekusi.config(text='ENQUEUE', bg='#0056b3', fg='white')

  elif kode_fitur == 'M2_DEQUEUE_NAIF':
    lbl_judul_fitur.config(
        text='Queue naif: ambil dari depan dengan menggeser isi'
    )
    lbl_sub_fitur.config(
        text='Mengambil indeks 0 lalu menggeser seluruh sisa 1 petak ke kiri.'
    )
    lbl_index.config(text='Berapa kali dequeue:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    entry_index.delete(0, tk.END)
    entry_index.insert(0, '1')
    btn_eksekusi.config(text='DEQUEUE', bg='#0056b3', fg='white')

  elif kode_fitur == 'M2_DEQUEUE_CIRCULAR':
    lbl_judul_fitur.config(
        text='Queue circular: ambil dari depan dengan memajukan penunjuk'
    )
    lbl_sub_fitur.config(
        text=(
            'Hanya penunjuk front yang maju. Isi larik tidak digeser sama'
            ' sekali.'
        )
    )
    lbl_index.config(text='Berapa kali dequeue:')
    lbl_index.grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_index.grid(row=0, column=1, padx=5, pady=5, sticky='w')
    entry_index.delete(0, tk.END)
    entry_index.insert(0, '1')
    btn_eksekusi.config(text='DEQUEUE', bg='#0056b3', fg='white')

  # --- M3 FITUR ---
  elif kode_fitur == 'SORT_INSERTION':
      lbl_judul_fitur.config(text='Sort: insertion sort, O(n²)')
      lbl_sub_fitur.config(
          text=(
              'Setiap elemen digeser mundur sampai menemukan tempatnya.'
              ' Sederhana, tetapi kerjanya tumbuh kuadratik.'
          )
      )

      # Perkecil lebar entry jumlah baris
      entry_index.config(width=8)

      # Input 1: Jumlah Baris (Kolom 0 & 1)
      lbl_index.config(text='Jumlah baris:')
      lbl_index.grid(row=0, column=0, padx=(5, 2), pady=5, sticky='w')
      entry_index.grid(row=0, column=1, padx=(0, 10), pady=5, sticky='w')
      entry_index.delete(0, tk.END)
      entry_index.insert(0, '10')

      # Input 2: Kunci Urut pakai Dropdown/Combobox (Kolom 2 & 3)
      lbl_nama.config(text='Urutkan menurut:')
      lbl_nama.grid(row=0, column=2, padx=(5, 2), pady=5, sticky='w')
      combo_kunci.grid(row=0, column=3, padx=(0, 10), pady=5, sticky='w')

      # Tombol URUTKAN (Kolom 4)
      btn_eksekusi.grid(row=0, column=4, padx=5, pady=5)
      btn_eksekusi.config(text='URUTKAN', bg='#0056b3', fg='white')

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
    undo_stack.push(('ARR_TAMBAH', p, data_array.size - 1))
    redo_stack = Stack()
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
    undo_stack.push(('ARR_TAMBAH', p, pos))
    redo_stack = Stack()
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
    undo_stack.push(('ARR_TAMBAH', p, 0))
    redo_stack = Stack()
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
    if p != None:
      undo_stack.push(('ARR_HAPUS', p, idx))
      redo_stack = Stack()
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
    undo_stack.push(('LL_TAMBAH', p, data_ll.size - 1))
    redo_stack = Stack()
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
    undo_stack.push(('LL_TAMBAH', p, pos))
    redo_stack = Stack()
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
    undo_stack.push(('LL_TAMBAH', p, 0))
    redo_stack = Stack()
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
    if p != None:
      undo_stack.push(('LL_HAPUS', p, idx))
      redo_stack = Stack()
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

  # --- M2: STACK POSTFIX ---
  elif fitur_aktif == 'M2_POSTFIX':
    expr = entry_nama.get().strip()
    t1 = time.perf_counter()
    postfix_tokens, log_1 = ke_postfix(expr)
    total, log_2 = hitung_postfix(postfix_tokens)
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    text_hasil.pack_forget()
    lbl_ringkasan.pack(fill=tk.X, pady=5)
    frame_tabel.pack(fill=tk.BOTH, expand=True, pady=5)

    text_ringkasan = (
        f'Struk : {expr}\nPostfix: {" ".join(postfix_tokens)}\nTOTAL : Rp'
        f' {total:,}'
    )
    lbl_ringkasan.config(text=text_ringkasan)

    kolom = ('langkah', 'token', 'tindakan', 'stack', 'output')
    tree_hasil['columns'] = kolom
    for c in kolom:
      tree_hasil.heading(c, text=c, anchor='w')

    tree_hasil.column('langkah', width=70, minwidth=60)
    tree_hasil.column('token', width=60, minwidth=50)
    tree_hasil.column('tindakan', width=280, minwidth=200)
    tree_hasil.column('stack', width=120, minwidth=100)
    tree_hasil.column('output', width=200, minwidth=150)

    for item in tree_hasil.get_children():
      tree_hasil.delete(item)

    idx = 1
    for tkn, tin, stk, out in log_1:
      lbl_step = f'1.{idx}' if idx != len(log_1) else '1.akhir'
      tree_hasil.insert('', tk.END, values=(lbl_step, tkn, tin, stk, out))
      idx += 1

    idx_eval = 1
    for tkn, tin, stk in log_2:
      tree_hasil.insert(
          '', tk.END, values=(f'2.{idx_eval}', tkn, tin, stk, stk)
      )
      idx_eval += 1

    cetak_log(f'M2 - Stack Postfix (Mesin Kasir) -> Waktu: {round(ms, 4)} ms')

  # --- M2: QUEUE ENQUEUE ---
  elif fitur_aktif == 'M2_ENQUEUE':
    p = buat_pesanan_baru(2)
    t1 = time.perf_counter()
    q_naif.enqueue(p)
    q_circ.enqueue(p)
    undo_stack.push(('QUEUE_ENQUEUE', p, None))
    redo_stack = Stack()
    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    lbl_ringkasan.pack(fill=tk.X, pady=5)
    text_ringkasan = (
        f'{p.oid} masuk ke barisan paling belakang pada KEDUA antrean.\nPanjang'
        f' sekarang: naif {q_naif.size():,}, circular {q_circ.size():,}.'
    )
    lbl_ringkasan.config(text=text_ringkasan)

    tampilkan_tabel_pesanan([p])
    cetak_log(f'M2 - Queue Enqueue ({p.oid}) -> Waktu: {round(ms, 4)} ms')

  # --- M2: QUEUE DEQUEUE NAIF ---
  elif fitur_aktif == 'M2_DEQUEUE_NAIF':
    try:
      k = int(entry_index.get())
    except:
      k = 1
    t1 = time.perf_counter()
    dilayani_naif, geseran = q_naif.dequeue_n(k)
    dilayani_circ, _ = q_circ.dequeue_n(k)

    if dilayani_naif:
      undo_stack.push(('QUEUE_DEQUEUE', dilayani_naif, None))
      redo_stack = Stack()

    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    lbl_ringkasan.pack(fill=tk.X, pady=5)
    rata_geser = (
        round(geseran / len(dilayani_naif), 2) if dilayani_naif else 0
    )
    text_ringkasan = (
        f'{len(dilayani_naif)} pesanan keluar dari depan antrean naif.\nTotal'
        f' {geseran:,} elemen digeser, rata-rata {rata_geser:,} geseran per'
        f' dequeue.\nSisa antrean naif {q_naif.size():,}.'
    )
    lbl_ringkasan.config(text=text_ringkasan)

    tampilkan_tabel_pesanan(dilayani_naif)
    cetak_log(
        f'M2 - Queue Dequeue Naif ({len(dilayani_naif)} data) -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  # --- M2: QUEUE DEQUEUE CIRCULAR ---
  elif fitur_aktif == 'M2_DEQUEUE_CIRCULAR':
    try:
      k = int(entry_index.get())
    except:
      k = 1
    t1 = time.perf_counter()
    dilayani_naif, _ = q_naif.dequeue_n(k)
    dilayani_circ, _ = q_circ.dequeue_n(k)

    if dilayani_circ:
      undo_stack.push(('QUEUE_DEQUEUE', dilayani_circ, None))
      redo_stack = Stack()

    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    lbl_ringkasan.pack(fill=tk.X, pady=5)
    text_ringkasan = (
        f'{len(dilayani_circ)} pesanan keluar dari depan antrean'
        ' circular.\nTidak ada elemen yang digeser. front sekarang'
        f' {q_circ.front}, rear {q_circ.rear}, kapasitas'
        f' {q_circ.capacity}.\nSisa antrean circular {q_circ.size():,}.'
    )
    lbl_ringkasan.config(text=text_ringkasan)

    tampilkan_tabel_pesanan(dilayani_circ)
    cetak_log(
        f'M2 - Queue Dequeue Circular ({len(dilayani_circ)} data) -> Waktu:'
        f' {round(ms, 4)} ms'
    )

  # --- M2: STACK UNDO ---
  elif fitur_aktif == 'M2_UNDO':
    if undo_stack.is_empty():
      text_hasil.delete('1.0', tk.END)
      text_hasil.insert(
          tk.END, 'Tumpukan UNDO kosong, tidak ada aksi untuk dibatalkan!'
      )
      return

    t1 = time.perf_counter()
    aksi = undo_stack.pop()
    jenis, payload, pos = aksi[0], aksi[1], aksi[2]

    if jenis == 'ARR_TAMBAH':
      data_array.delete(pos)
      redo_stack.push(('ARR_TAMBAH', payload, pos))
      pesan = f'Membatalkan penambahan Array: {payload.oid} ({payload.pelanggan})'
    elif jenis == 'ARR_HAPUS':
      data_array.insert(pos, payload)
      redo_stack.push(('ARR_HAPUS', payload, pos))
      pesan = f'Membatalkan penghapusan Array: {payload.oid} ({payload.pelanggan})'
    elif jenis == 'LL_TAMBAH':
      data_ll.delete(pos)
      redo_stack.push(('LL_TAMBAH', payload, pos))
      pesan = (
          f'Membatalkan penambahan LinkedList: {payload.oid} ({payload.pelanggan})'
      )
    elif jenis == 'LL_HAPUS':
      data_ll.insert(pos, payload)
      redo_stack.push(('LL_HAPUS', payload, pos))
      pesan = (
          f'Membatalkan penghapusan LinkedList: {payload.oid}'
          f' ({payload.pelanggan})'
      )
    elif jenis == 'QUEUE_ENQUEUE':
      q_naif.un_enqueue()
      q_circ.un_enqueue()
      redo_stack.push(('QUEUE_ENQUEUE', payload, None))
      pesan = (
          f'Membatalkan enqueue: {payload.oid} dikeluarkan lagi dari belakang.'
          f' Panjang antrean sekarang: naif {q_naif.size():,}, circular'
          f' {q_circ.size():,}.'
      )
    elif jenis == 'QUEUE_DEQUEUE':
      q_naif.un_dequeue(payload)
      q_circ.un_dequeue(payload)
      redo_stack.push(('QUEUE_DEQUEUE', payload, None))
      pesan = (
          f'Membatalkan dequeue: {len(payload)} pesanan dikembalikan ke DEPAN'
          f' antrean. Panjang antrean sekarang: naif {q_naif.size():,},'
          f' circular {q_circ.size():,}.'
      )

    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        f'{pesan}\nTumpukan undo tersisa {undo_stack.size()} catatan, redo'
        f' {redo_stack.size()} catatan.',
    )
    cetak_log(f'M2 - Stack Undo -> Waktu: {round(ms, 4)} ms')

  # --- M2: STACK REDO ---
  elif fitur_aktif == 'M2_REDO':
    if redo_stack.is_empty():
      text_hasil.delete('1.0', tk.END)
      text_hasil.insert(
          tk.END,
          'Tumpukan REDO kosong, tidak ada aksi untuk dikerjakan ulang!',
      )
      return

    t1 = time.perf_counter()
    aksi = redo_stack.pop()
    jenis, payload, pos = aksi[0], aksi[1], aksi[2]

    if jenis == 'ARR_TAMBAH':
      data_array.insert(pos, payload)
      undo_stack.push(('ARR_TAMBAH', payload, pos))
      pesan = (
          f'Mengerjakan ulang penambahan Array: {payload.oid} ({payload.pelanggan})'
      )
    elif jenis == 'ARR_HAPUS':
      data_array.delete(pos)
      undo_stack.push(('ARR_HAPUS', payload, pos))
      pesan = (
          f'Mengerjakan ulang penghapusan Array: {payload.oid}'
          f' ({payload.pelanggan})'
      )
    elif jenis == 'LL_TAMBAH':
      data_ll.insert(pos, payload)
      undo_stack.push(('LL_TAMBAH', payload, pos))
      pesan = (
          'Mengerjakan ulang penambahan LinkedList:'
          f' {payload.oid} ({payload.pelanggan})'
      )
    elif jenis == 'LL_HAPUS':
      data_ll.delete(pos)
      undo_stack.push(('LL_HAPUS', payload, pos))
      pesan = (
          'Mengerjakan ulang penghapusan LinkedList:'
          f' {payload.oid} ({payload.pelanggan})'
      )
    elif jenis == 'QUEUE_ENQUEUE':
      q_naif.enqueue(payload)
      q_circ.enqueue(payload)
      undo_stack.push(('QUEUE_ENQUEUE', payload, None))
      pesan = (
          f'Enqueue dikerjakan lagi: {payload.oid} masuk kembali ke belakang.'
          f' Panjang antrean sekarang: naif {q_naif.size():,}, circular'
          f' {q_circ.size():,}.'
      )
    elif jenis == 'QUEUE_DEQUEUE':
      k = len(payload)
      q_naif.dequeue_n(k)
      q_circ.dequeue_n(k)
      undo_stack.push(('QUEUE_DEQUEUE', payload, None))
      pesan = (
          f'Dequeue dikerjakan lagi: {k} pesanan keluar kembali dari depan.'
          f' Panjang antrean sekarang: naif {q_naif.size():,}, circular'
          f' {q_circ.size():,}.'
      )

    t2 = time.perf_counter()
    ms = (t2 - t1) * 1000

    text_hasil.delete('1.0', tk.END)
    text_hasil.insert(
        tk.END,
        f'{pesan}\nTumpukan undo {undo_stack.size()} catatan, redo tersisa'
        f' {redo_stack.size()} catatan.',
    )
    cetak_log(f'M2 - Stack Redo -> Waktu: {round(ms, 4)} ms')

  elif fitur_aktif == 'SORT_INSERTION':
        try:
            limit = int(entry_index.get())
        except:
            limit = 10

        # Ambil nilai kunci langsung dari Combobox
        kunci = combo_kunci.get().strip().lower()
        opsi_valid = ['oid', 'pelanggan', 'resto', 'menu', 'harga', 'status']
        if kunci not in opsi_valid:
            kunci = 'harga'

        if limit > 20000:
            text_hasil.delete('1.0', tk.END)
            text_hasil.insert(
                tk.END,
                'DITOLAK: Batas maksimal Insertion Sort adalah 20.000 baris untuk'
                ' menghindari freeze!',
            )
            return

        n_data = min(limit, data_array.size)
        sampel_data = [data_array.get(i) for i in range(n_data)]

        t1 = time.perf_counter()
        hasil_sort, perbandingan, pemindahan = insertion_sort(
            sampel_data, kunci
        )
        t2 = time.perf_counter()
        ms = (t2 - t1) * 1000

        lbl_ringkasan.pack(fill=tk.X, pady=5)
        text_ringkasan = (
            f'{n_data} pesanan diurutkan menurut {kunci}.\n{perbandingan:,}'
            f' perbandingan, {pemindahan:,} pemindahan.'
        )
        lbl_ringkasan.config(text=text_ringkasan)

        tampilkan_tabel_pesanan(hasil_sort)
        cetak_log(
            f'M3 - Insertion Sort ({n_data} data, kunci: {kunci}) -> Waktu:'
            f' {round(ms, 4)} ms'
        )

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

# --- FRAME KIRI (SIDEBAR MENU WITH SCROLLBAR) ---
frame_kiri_outer = tk.Frame(frame_utama, width=280, bd=1, relief=tk.SOLID)
frame_kiri_outer.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 5))

# Canvas dan Scrollbar untuk mendukung scroll
canvas_kiri = tk.Canvas(frame_kiri_outer, bd=0, highlightthickness=0, width=250)
scrollbar_kiri = ttk.Scrollbar(frame_kiri_outer, orient="vertical", command=canvas_kiri.yview)

# Inner frame tempat seluruh tombol diletakkan (variabel tetap 'frame_kiri')
frame_kiri = tk.Frame(canvas_kiri)

# Update area scroll secara otomatis saat ada elemen baru yang ditambahkan
frame_kiri.bind(
    "<Configure>",
    lambda e: canvas_kiri.configure(scrollregion=canvas_kiri.bbox("all"))
)

canvas_kiri.create_window((0, 0), window=frame_kiri, anchor="nw")
canvas_kiri.configure(yscrollcommand=scrollbar_kiri.set)

scrollbar_kiri.pack(side=tk.RIGHT, fill=tk.Y)
canvas_kiri.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Fitur Scroll menggunakan Wheel Mouse (Opsional)
def _on_mousewheel(event):
    canvas_kiri.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas_kiri.bind_all("<MouseWheel>", _on_mousewheel)

# KELOMPOK M1
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

# KELOMPOK M2
lbl_m2 = tk.Label(
    frame_kiri,
    text='M2 - STACK DAN QUEUE',
    font=('Arial', 8, 'bold'),
    fg='#555555',
    anchor='w',
)
lbl_m2.pack(fill=tk.X, padx=8, pady=(12, 2))

tk.Button(
    frame_kiri,
    text='STACK - POSTFIX (MESIN KASIR)',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('M2_POSTFIX'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='STACK - UNDO',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('M2_UNDO'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='STACK - REDO',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('M2_REDO'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='QUEUE - ENQUEUE',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('M2_ENQUEUE'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='QUEUE - DEQUEUE NAIF',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('M2_DEQUEUE_NAIF'),
).pack(fill=tk.X, padx=8, pady=1)
tk.Button(
    frame_kiri,
    text='QUEUE - DEQUEUE CIRCULAR',
    anchor='w',
    font=('Arial', 9),
    bg='#f8f9fa',
    bd=1,
    command=lambda: pilih_fitur('M2_DEQUEUE_CIRCULAR'),
).pack(fill=tk.X, padx=8, pady=1)

# KELOMPOK M3 (SORT - INSERTION SORT)
lbl_m3 = tk.Label(frame_kiri, text="M3 - SORT DAN SEARCH", font=("Arial", 8, "bold"), fg="#555555", anchor="w")
lbl_m3.pack(fill=tk.X, padx=8, pady=(12, 2))

tk.Button(
    frame_kiri, 
    text="SORT - INSERTION SORT", 
    anchor="w", 
    font=("Arial", 9), 
    bg="#f8f9fa", 
    bd=1,
    command=lambda: pilih_fitur('SORT_INSERTION')
).pack(fill=tk.X, padx=8, pady=1)

# --- FRAME KANAN ---
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

# Form Input
frame_form = tk.Frame(frame_kanan, bd=1, relief=tk.SOLID)
frame_form.pack(fill=tk.X, pady=5)

lbl_nama = tk.Label(frame_form, text='Nama pelanggan:')
entry_nama = tk.Entry(frame_form, width=35)
entry_nama.insert(0, 'Pelanggan Baru')

lbl_index = tk.Label(frame_form, text='Indeks ke-i:')
entry_index = tk.Entry(frame_form, width=15)
entry_index.insert(0, '0')

combo_kunci = ttk.Combobox(
    frame_form,
    values=['oid', 'pelanggan', 'resto', 'menu', 'harga', 'status'],
    state='readonly',
    width=12,
)
combo_kunci.set('harga')

btn_eksekusi = tk.Button(
    frame_form,
    text='LIHAT',
    font=('Arial', 9, 'bold'),
    width=12,
    command=eksekusi_fitur,
)
btn_eksekusi.grid(row=0, column=2, padx=15, pady=5)

# Area Ringkasan Teks
lbl_ringkasan = tk.Label(
    frame_kanan, text='', font=('Arial', 10), justify='left', anchor='w'
)

# Area Tabel Treeview
frame_tabel = tk.Frame(frame_kanan)
tree_hasil = ttk.Treeview(frame_tabel, show='headings')
scroll_y = ttk.Scrollbar(
    frame_tabel, orient='vertical', command=tree_hasil.yview
)
scroll_x = ttk.Scrollbar(
    frame_tabel, orient='horizontal', command=tree_hasil.xview
)
tree_hasil.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
tree_hasil.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Area Text Biasa
text_hasil = tk.Text(frame_kanan, height=8)
text_hasil.pack(fill=tk.BOTH, expand=True, pady=5)

# Area Command Log
frame_log = tk.LabelFrame(frame_kanan, text='COMMAND LOG & WAKTU')
frame_log.pack(fill=tk.X, side=tk.BOTTOM)

text_log = tk.Text(
    frame_log, height=5, bg='black', fg='lime', font=('Consolas', 9)
)
text_log.pack(fill=tk.BOTH, expand=True)

pilih_fitur('ARR_LIHAT_INDEKS')
root.mainloop()