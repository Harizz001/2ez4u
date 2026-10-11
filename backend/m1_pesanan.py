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

    def cari_by_oid(self, target_oid):
        """Mencari pesanan berdasarkan OID (contoh: 'O-000005')"""
        for i in range(self.size):
            if self.data[i].oid.upper() == target_oid.upper():
                return self.data[i], i
        return None, -1

class Node:

    def __init__(self, val):
        self.val = val
        self.next = None

class LinkList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, v):
        """Tambah pesanan REGULER di posisi paling belakang -> O(1) via tail pointer"""
        node_baru = Node(v)
        if self.head is None:
            self.head = node_baru
            self.tail = node_baru
        else:
            self.tail.next = node_baru
            self.tail = node_baru
        self.size += 1

    def insert(self, i, v):
        """Tambah VIP (i=0) -> O(1), atau PRIORITAS (i=tengah) -> O(n) traversal"""
        node_baru = Node(v)
        if i <= 0:
            # VIP: Sisip di depan (head)
            node_baru.next = self.head
            self.head = node_baru
            if self.tail is None:
                self.tail = node_baru
            self.size += 1
        elif i >= self.size:
            # REGULER: Sisip di belakang
            self.append(v)
        else:
            # PRIORITAS: Menelusuri node dari head sampai posisi i-1
            curr = self.head
            for k in range(i - 1):
                curr = curr.next
            node_baru.next = curr.next
            curr.next = node_baru
            self.size += 1

    def get(self, i):
        """Lihat pesanan ke-i -> O(n) Traversal"""
        if i < 0 or i >= self.size:
            return None
        curr = self.head
        for k in range(i):
            curr = curr.next
        return curr.val

    def delete(self, i):
        """Hapus pesanan ke-i -> O(n) Traversal"""
        if i < 0 or i >= self.size:
            return None

        if i == 0:
            hasil = self.head.val
            self.head = self.head.next
            self.size -= 1
            if self.size == 0:
                self.tail = None
            return hasil

        curr = self.head
        for k in range(i - 1):
            curr = curr.next

        hasil = curr.next.val
        curr.next = curr.next.next

        if curr.next is None:
            self.tail = curr

        self.size -= 1
        return hasil

    def cari_by_oid(self, target_oid):
        """Cari pesanan berdasarkan OID -> O(n) Traversal"""
        curr = self.head
        idx = 0
        while curr is not None:
            if curr.val.oid.upper() == target_oid.upper():
                return curr.val, idx
            curr = curr.next
            idx += 1
        return None, -1