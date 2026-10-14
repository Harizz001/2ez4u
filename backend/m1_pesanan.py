class Pesanan:

  """Model data untuk merepresentasikan 1 entitas pesanan makanan."""

  def __init__(
      self,
      oid,
      pelanggan,
      resto,
      menu,
      harga,
      prioritas,
      masuk,
      selesai,
      status,
  ):
    self.oid = oid  # Order ID (misal: 'O-000001')
    self.pelanggan = pelanggan  # Nama pelanggan
    self.resto = resto  # Nama restoran/kantin
    self.menu = menu  # Menu pesanan
    self.harga = harga  # Harga pesanan
    self.prioritas = prioritas  # Tingkat prioritas (1: VIP, 2: Prioritas, 3: Reguler)
    self.masuk = masuk  # Waktu pesanan masuk
    self.selesai = selesai  # Waktu pesanan selesai
    self.status = status  # Status pesanan ('ANTRE', 'PROSES', 'SELESAI')


# ==========================================
# STRUKTUR DATA ARRAY (DYNAMIC ARRAY)
# ==========================================
class Array:

  """Struktur data Array dinamis manual dengan alokasi memori berkala."""

  def __init__(self, capacity=10):
    self.capacity = capacity
    self.data = [None] * capacity  # Alokasi memori internal awal
    self.size = 0  # Jumlah elemen terisi saat ini

  def _resize(self, new_capacity):
    """Meningkatkan/menyesuaikan kapasitas array ketika memori penuh."""
    new_data = [None] * new_capacity
    for i in range(self.size):
      new_data[i] = self.data[i]
    self.data = new_data
    self.capacity = new_capacity

  def append(self, pesanan):
    """Menambahkan pesanan di posisi paling belakang - O(1) amortized."""
    if self.size == self.capacity:
      self._resize(self.capacity * 2)  # Double capacity jika penuh
    self.data[self.size] = pesanan
    self.size += 1

  def insert(self, idx, pesanan):
    """Menyisipkan pesanan pada indeks tertentu - O(n) karena penggeseran elemen ke kanan."""
    if idx < 0 or idx > self.size:
      return False
    if self.size == self.capacity:
      self._resize(self.capacity * 2)

    # Geser elemen ke kanan dari indeks paling belakang hingga idx
    for i in range(self.size, idx, -1):
      self.data[i] = self.data[i - 1]

    self.data[idx] = pesanan
    self.size += 1
    return True

  def delete(self, idx):
    """Menghapus pesanan pada indeks tertentu - O(n) karena penggeseran elemen ke kiri."""
    if idx < 0 or idx >= self.size:
      return None
    val = self.data[idx]

    # Geser elemen ke kiri untuk mengisi kekosongan
    for i in range(idx, self.size - 1):
      self.data[i] = self.data[i + 1]

    self.data[self.size - 1] = None
    self.size -= 1
    return val

  def get(self, idx):
    """Mengambil pesanan berdasarkan indeks - O(1) Random Access."""
    if 0 <= idx < self.size:
      return self.data[idx]
    return None

  def cari_by_oid(self, target_oid):
    """Pencarian linier pesanan berdasarkan OID - O(n)."""
    for i in range(self.size):
      if self.data[i].oid == target_oid:
        return self.data[i], i
    return None, -1


# ==========================================
# STRUKTUR DATA LINKED LIST
# ==========================================
class Node:

  """Elemen/Simpul tunggal pada Linked List."""

  def __init__(self, data):
    self.data = data
    self.next = None  # Penunjuk ke node berikutnya


class LinkList:

  """Singly Linked List dengan penunjuk Head dan Tail."""

  def __init__(self):
    self.head = None  # Penunjuk node pertama
    self.tail = None  # Penunjuk node terakhir
    self.size = 0  # Jumlah node terpasang

  def append(self, pesanan):
    """Menambahkan node di posisi akhir via Tail pointer - O(1)."""
    new_node = Node(pesanan)
    if self.head is None:
      self.head = new_node
      self.tail = new_node
    else:
      self.tail.next = new_node
      self.tail = new_node
    self.size += 1

  def insert(self, idx, pesanan):
    """Menyisipkan node pada indeks tertentu - O(n) penelusuran pointer."""
    if idx < 0 or idx > self.size:
      return False
    if idx == 0:
      # Sisip di awal (VIP) - O(1)
      new_node = Node(pesanan)
      new_node.next = self.head
      self.head = new_node
      if self.size == 0:
        self.tail = new_node
      self.size += 1
      return True
    elif idx == self.size:
      # Sisip di akhir (Reguler) - O(1)
      self.append(pesanan)
      return True

    # Sisip di tengah (Prioritas) - O(n)
    new_node = Node(pesanan)
    curr = self.head
    for _ in range(idx - 1):
      curr = curr.next

    new_node.next = curr.next
    curr.next = new_node
    self.size += 1
    return True

  def delete(self, idx):
    """Menghapus node pada indeks tertentu - O(n) penelusuran pointer."""
    if idx < 0 or idx >= self.size or self.head is None:
      return None

    if idx == 0:
      val = self.head.data
      self.head = self.head.next
      if self.head is None:
        self.tail = None
      self.size -= 1
      return val

    curr = self.head
    for _ in range(idx - 1):
      curr = curr.next

    val = curr.next.data
    curr.next = curr.next.next
    if curr.next is None:
      self.tail = curr
    self.size -= 1
    return val

  def get(self, idx):
    """Mengambil data pada indeks tertentu via penelusuran dari Head - O(n)."""
    if idx < 0 or idx >= self.size:
      return None
    curr = self.head
    for _ in range(idx):
      curr = curr.next
    return curr.data

  def cari_by_oid(self, target_oid):
    """Menelusuri rantai node untuk mencari OID yang cocok - O(n)."""
    curr = self.head
    idx = 0
    while curr:
      if curr.data.oid == target_oid:
        return curr.data, idx
      curr = curr.next
      idx += 1
    return None, -1