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