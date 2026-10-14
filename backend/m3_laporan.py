def get_kunci_val(pesanan, kunci):
    if kunci in ['harga', 'prioritas']:
        return int(getattr(pesanan, kunci, 0))
    
    # Untuk kolom berbasis teks (oid, pelanggan, resto, menu, status)
    val = str(getattr(pesanan, kunci, ''))
    return val.lower()

def insertion_sort(arr_input, kunci='harga'):
    # Buat salinan data agar data asli di Array/LinkedList M1 tidak rusak
    arr = [arr_input[i] for i in range(len(arr_input))]
    
    perbandingan = 0
    pemindahan = 0
    
    n = len(arr)
    for i in range(1, n):
        key_item = arr[i]
        key_val = get_kunci_val(key_item, kunci)
        j = i - 1
        
        # Penggunaan '>' memastikan algoritma bersifat STABIL
        while j >= 0:
            perbandingan += 1
            if get_kunci_val(arr[j], kunci) > key_val:
                arr[j + 1] = arr[j]
                pemindahan += 1
                j -= 1
            else:
                break
                
        arr[j + 1] = key_item
        pemindahan += 1 # Pemindahan elemen ke posisi akhirnya
        
    return arr, perbandingan, pemindahan

def merge_sort(arr_input, kunci='harga'):
  # Salin array agar data asli di M1 tidak terubah
  arr = [arr_input[i] for i in range(len(arr_input))]

  perbandingan = 0
  pemindahan = 0  # Pencatatan pemindahan / penulisan elemen ke sub-array baru

  def _merge_sort_rec(sub_arr):
    nonlocal perbandingan, pemindahan
    if len(sub_arr) <= 1:
      return sub_arr

    mid = len(sub_arr) // 2
    left = _merge_sort_rec(sub_arr[:mid])
    right = _merge_sort_rec(sub_arr[mid:])

    i = j = 0
    merged = []

    # Proses penggabungan (Combine)
    while i < len(left) and j < len(right):
      perbandingan += 1
      val_left = get_kunci_val(left[i], kunci)
      val_right = get_kunci_val(right[j], kunci)

      # Tanda '<=' menjaga sifat STABIL pada algoritma
      if val_left <= val_right:
        merged.append(left[i])
        i += 1
      else:
        merged.append(right[j])
        j += 1
      pemindahan += 1

    # Memindahkan sisa elemen kiri (jika ada)
    while i < len(left):
      merged.append(left[i])
      i += 1
      pemindahan += 1

    # Memindahkan sisa elemen kanan (jika ada)
    while j < len(right):
      merged.append(right[j])
      j += 1
      pemindahan += 1

    return merged

  hasil = _merge_sort_rec(arr)
  return hasil, perbandingan, pemindahan