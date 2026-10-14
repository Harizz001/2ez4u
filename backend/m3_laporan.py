# backend/m3_laporan.py


def get_kunci_val(pesanan, kunci):
  if kunci in ['harga', 'prioritas']:
    return int(getattr(pesanan, kunci, 0))

  val = str(getattr(pesanan, kunci, ''))
  return val.lower()


# --- ALGORITMA SORTING ---
def insertion_sort(arr_input, kunci='harga'):
  arr = [arr_input[i] for i in range(len(arr_input))]
  perbandingan = 0
  pemindahan = 0

  n = len(arr)
  for i in range(1, n):
    key_item = arr[i]
    key_val = get_kunci_val(key_item, kunci)
    j = i - 1

    while j >= 0:
      perbandingan += 1
      if get_kunci_val(arr[j], kunci) > key_val:
        arr[j + 1] = arr[j]
        pemindahan += 1
        j -= 1
      else:
        break

    arr[j + 1] = key_item
    pemindahan += 1

  return arr, perbandingan, pemindahan


def merge_sort(arr_input, kunci='harga'):
  arr = [arr_input[i] for i in range(len(arr_input))]
  perbandingan = 0
  pemindahan = 0

  def _merge_sort_rec(sub_arr):
    nonlocal perbandingan, pemindahan
    if len(sub_arr) <= 1:
      return sub_arr

    mid = len(sub_arr) // 2
    left = _merge_sort_rec(sub_arr[:mid])
    right = _merge_sort_rec(sub_arr[mid:])

    i = j = 0
    merged = []

    while i < len(left) and j < len(right):
      perbandingan += 1
      val_left = get_kunci_val(left[i], kunci)
      val_right = get_kunci_val(right[j], kunci)

      if val_left <= val_right:
        merged.append(left[i])
        i += 1
      else:
        merged.append(right[j])
        j += 1
      pemindahan += 1

    while i < len(left):
      merged.append(left[i])
      i += 1
      pemindahan += 1

    while j < len(right):
      merged.append(right[j])
      j += 1
      pemindahan += 1

    return merged

  hasil = _merge_sort_rec(arr)
  return hasil, perbandingan, pemindahan


# --- ALGORITMA SEARCHING ---
def linear_search(arr_input, kunci, target):
  target_str = str(target).strip().lower()
  hasil = []
  perbandingan = 0

  for i in range(len(arr_input)):
    perbandingan += 1
    val = str(get_kunci_val(arr_input[i], kunci))

    if target_str in val:
      hasil.append(arr_input[i])

  return hasil, perbandingan


def binary_search(arr_input, kunci, target):
  # Binary Search mewajibkan data terurut, lakukan merge sort terlebih dahulu
  arr_sorted, _, _ = merge_sort(arr_input, kunci)

  target_str = str(target).strip().lower()
  n = len(arr_sorted)
  perbandingan = 0

  low = 0
  high = n - 1
  found_idx = -1

  # Pencarian biner mencari salah satu posisi pencocokan
  while low <= high:
    perbandingan += 1
    mid = (low + high) // 2
    val_mid = str(get_kunci_val(arr_sorted[mid], kunci))

    if val_mid == target_str or target_str in val_mid:
      found_idx = mid
      break
    elif val_mid < target_str:
      low = mid + 1
    else:
      high = mid - 1

  hasil = []
  if found_idx != -1:
    # Kumpulkan seluruh data yang cocok di sebelah kiri
    curr = found_idx
    while curr >= 0 and target_str in str(
        get_kunci_val(arr_sorted[curr], kunci)
    ):
      hasil.append(arr_sorted[curr])
      curr -= 1
      perbandingan += 1
    hasil.reverse()

    # Kumpulkan seluruh data yang cocok di sebelah kanan
    curr = found_idx + 1
    while curr < n and target_str in str(
        get_kunci_val(arr_sorted[curr], kunci)
    ):
      hasil.append(arr_sorted[curr])
      curr += 1
      perbandingan += 1

  return hasil, perbandingan, arr_sorted