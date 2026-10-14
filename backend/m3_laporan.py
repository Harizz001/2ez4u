def get_kunci_val(pesanan, kunci):
  """Fungsi pembantu untuk mengambil nilai dari objek Pesanan secara dinamis.

  Mengonversi tipe data ke integer untuk angka (harga/prioritas) atau string
  lowercase untuk teks.
  """
  if kunci in ['harga', 'prioritas']:
    return int(getattr(pesanan, kunci, 0))

  # Untuk atribut teks (oid, pelanggan, resto, menu, status), ubah ke string lowercase
  val = str(getattr(pesanan, kunci, ''))
  return val.lower()


# ==========================================
# ALGORITMA SORTING (PENGURUTAN)
# ==========================================


def insertion_sort(arr_input, kunci='harga'):
  """Insertion Sort - Kompleksitas O(n^2)

  Membandingkan dan menggeser elemen satu per satu ke posisi yang tepat.
  Bersifat STABIL (mempertahankan urutan elemen bernilai sama).
  """
  # Salin array agar tidak mengubah/merusak data asli di M1
  arr = [arr_input[i] for i in range(len(arr_input))]
  perbandingan = 0  # Counter total perbandingan kunci
  pemindahan = 0  # Counter total pergeseran/pemindahan posisi elemen

  n = len(arr)
  for i in range(1, n):
    key_item = arr[i]
    key_val = get_kunci_val(key_item, kunci)
    j = i - 1

    # Geser elemen yang lebih besar dari key_val ke kanan
    while j >= 0:
      perbandingan += 1
      if get_kunci_val(arr[j], kunci) > key_val:
        arr[j + 1] = arr[j]
        pemindahan += 1
        j -= 1
      else:
        break  # Berhenti jika menemukan posisi yang tepat

    # Sisipkan key_item di posisi yang sesuai
    arr[j + 1] = key_item
    pemindahan += 1

  return arr, perbandingan, pemindahan


def merge_sort(arr_input, kunci='harga'):
  """Merge Sort - Kompleksitas O(n log n)

  Menggunakan pendekatan Divide and Conquer: membagi array menjadi 2 sub-array,
  mengurutkannya secara rekursif, lalu menggabungkannya (merge). Bersifat STABIL.
  """
  arr = [arr_input[i] for i in range(len(arr_input))]
  perbandingan = 0
  pemindahan = 0

  def _merge_sort_rec(sub_arr):
    nonlocal perbandingan, pemindahan

    # Base case: jika elemen <= 1, sub-array sudah terurut
    if len(sub_arr) <= 1:
      return sub_arr

    # Divide: Bagi array menjadi 2 bagian (kiri dan kanan)
    mid = len(sub_arr) // 2
    left = _merge_sort_rec(sub_arr[:mid])
    right = _merge_sort_rec(sub_arr[mid:])

    # Combine: Gabungkan kembali sub-array kiri dan kanan
    i = j = 0
    merged = []

    while i < len(left) and j < len(right):
      perbandingan += 1
      val_left = get_kunci_val(left[i], kunci)
      val_right = get_kunci_val(right[j], kunci)

      # Penggunaan '<=' menjaga sifat STABIL pada pengurutan
      if val_left <= val_right:
        merged.append(left[i])
        i += 1
      else:
        merged.append(right[j])
        j += 1
      pemindahan += 1

    # Ambil sisa elemen di bagian kiri jika ada
    while i < len(left):
      merged.append(left[i])
      i += 1
      pemindahan += 1

    # Ambil sisa elemen di bagian kanan jika ada
    while j < len(right):
      merged.append(right[j])
      j += 1
      pemindahan += 1

    return merged

  hasil = _merge_sort_rec(arr)
  return hasil, perbandingan, pemindahan


# ==========================================
# ALGORITMA SEARCHING (PENCARIAN)
# ==========================================


def linear_search(arr_input, kunci, target):
  """Linear Search - Kompleksitas O(n)

  Mencari elemen dengan menelusuri data satu per satu dari awal hingga akhir.
  Dapat bekerja pada data yang BELUM TERURUT dan mendukung pencarian substring.
  """
  target_str = str(target).strip().lower()
  hasil = []
  perbandingan = 0

  for i in range(len(arr_input)):
    perbandingan += 1
    val = str(get_kunci_val(arr_input[i], kunci))

    # Cek apakah kata kunci target ada di dalam nilai kolom (substring matching)
    if target_str in val:
      hasil.append(arr_input[i])

  return hasil, perbandingan


def binary_search(arr_input, kunci, target):
  """Binary Search - Kompleksitas O(log n)

  Mencari elemen dengan membagi 2 ruang pencarian secara berulang.
  SYARAT UTAMA: Data WAJIB terurut terlebih dahulu (menggunakan Merge Sort).
  """
  # Step 1: Urutkan data menggunakan Merge Sort O(n log n)
  arr_sorted, _, _ = merge_sort(arr_input, kunci)

  target_str = str(target).strip().lower()
  n = len(arr_sorted)
  perbandingan = 0

  low = 0
  high = n - 1
  found_idx = -1

  # Step 2: Proses Binary Search untuk menemukan salah satu titik cocok
  while low <= high:
    perbandingan += 1
    mid = (low + high) // 2
    val_mid = str(get_kunci_val(arr_sorted[mid], kunci))

    if val_mid == target_str or target_str in val_mid:
      found_idx = mid
      break  # Titik awal kecocokan ditemukan
    elif val_mid < target_str:
      low = mid + 1  # Cari di setengah bagian kanan
    else:
      high = mid - 1  # Cari di setengah bagian kiri

  # Step 3: Ekspansi ke kiri dan kanan dari titik temuan untuk mengumpulkan data ganda
  hasil = []
  if found_idx != -1:
    # Telusuri ke arah kiri
    curr = found_idx
    while curr >= 0 and target_str in str(
        get_kunci_val(arr_sorted[curr], kunci)
    ):
      hasil.append(arr_sorted[curr])
      curr -= 1
      perbandingan += 1
    hasil.reverse()  # Balikkan agar urutannya tetap terjaga

    # Telusuri ke arah kanan
    curr = found_idx + 1
    while curr < n and target_str in str(
        get_kunci_val(arr_sorted[curr], kunci)
    ):
      hasil.append(arr_sorted[curr])
      curr += 1
      perbandingan += 1

  return hasil, perbandingan, arr_sorted