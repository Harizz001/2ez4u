class Pesanan:
    def __init__(self, oid, pelanggan, resto, menu, harga, prioritas, t_masuk, t_selesai, status):
        self.oid = oid
        self.pelanggan = pelanggan
        self.resto = resto
        self.menu = menu
        self.harga = harga
        self.prioritas = prioritas
        self.t_masuk = t_masuk
        self.t_selesai = t_selesai
        self.status = status

class Array:
    def __init__(self):
        self.kapasitas = 10
        self.size = 0
        self.data = [None] * self.kapasitas

    def append(self, v):
        """"
        Tambah pesanan REGULER di barisan paling belakang
        """
        if self.size == self.kapasitas:
            self.kapasitas = self.kapasitas * 2
            data_baru = [None] * self.kapasitas
            for i in range(self.size):
                data_baru[i] = self.data[i]
            self.data = data_baru

        self.data[self.size] = v
        self.size += 1

    def insert(self, i, v):
        """
        Tambah pesanan VIP (i=0) atau PRIORITAS (i=tengah)
        """
        if i < 0:
            i = 0
        if i > self.size:
            i = self.size

        if self.size == self.kapasitas:
            self.kapasitas = self.kapasitas * 2
            data_baru = [None] * self.kapasitas
            for k in range(self.size):
                data_baru[k] = self.data[k]
            self.data = data_baru

        j = self.size
        while j > i:
            self.data[j] = self.data[j - 1]
            j -= 1

        self.data[i] = v
        self.size += 1

    def get(self, i):
        """
        Lihat pesanan berdasarkan indeks ke-i
        """
        if i >= 0 and i < self.size:
            return self.data[i]
        return None

    def delete(self, i):
        """
        Hapus pesanan berdasarkan indeks ke-i
        """
        if i >= 0 and i < self.size:
            hasil = self.data[i]
            for j in range(i, self.size - 1):
                self.data[j] = self.data[j + 1]
            self.data[self.size - 1] = None
            self.size -= 1
            return hasil
        return None