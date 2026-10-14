# backend/m2_antrean.py


class Stack:

  def __init__(self, capacity=10):
    self.capacity = capacity
    self.data = [None] * capacity
    self.top = 0

  def is_empty(self):
    return self.top == 0

  def is_full(self):
    return self.top == self.capacity

  def _resize(self, new_capacity):
    new_data = [None] * new_capacity
    for i in range(self.top):
      new_data[i] = self.data[i]
    self.data = new_data
    self.capacity = new_capacity

  def push(self, x):
    if self.is_full():
      self._resize(self.capacity * 2)
    self.data[self.top] = x
    self.top += 1

  def pop(self):
    if self.is_empty():
      return None
    self.top -= 1
    val = self.data[self.top]
    self.data[self.top] = None
    return val

  def peek(self):
    if self.is_empty():
      return None
    return self.data[self.top - 1]

  def size(self):
    return self.top


# --- MODUL MESIN KASIR (INFIX KE POSTFIX & EVALUASI) ---
def tokenisasi(ekspresi):
  tokens = []
  i = 0
  n = len(ekspresi)
  while i < n:
    c = ekspresi[i]
    if c in ' \t':
      i += 1
      continue
    if c.isdigit():
      val = ''
      while i < n and ekspresi[i].isdigit():
        val += ekspresi[i]
        i += 1
      tokens.append(val)
    elif c in '+-*/()':
      tokens.append(c)
      i += 1
    else:
      i += 1
  return tokens


def ke_postfix(ekspresi):
  tokens = tokenisasi(ekspresi)
  output = []
  op_stack = Stack()
  langkah_log = []
  prioritas = {'+': 1, '-': 1, '*': 2, '/': 2}

  for t in tokens:
    if t.isdigit():
      output.append(t)
      tindakan = 'operand, langsung ke output'
    elif t == '(':
      op_stack.push(t)
      tindakan = 'push ( ke stack'
    elif t == ')':
      tindakan = 'pop sampai (, lalu buang ('
      top_val = op_stack.pop()
      while top_val is not None and top_val != '(':
        output.append(top_val)
        top_val = op_stack.pop()
    elif t in '+-*/':
      tindakan = 'push operator'
      p = prioritas[t]
      while not op_stack.is_empty() and op_stack.peek() != '(':
        top_p = prioritas.get(op_stack.peek(), 0)
        if top_p >= p:
          output.append(op_stack.pop())
        else:
          break
      op_stack.push(t)

    stk_str = (
        ' '.join([str(op_stack.data[i]) for i in range(op_stack.top)])
        if op_stack.top > 0
        else 'kosong'
    )
    out_str = ' '.join(output)
    langkah_log.append((t, tindakan, stk_str, out_str))

  while not op_stack.is_empty():
    output.append(op_stack.pop())
    stk_str = (
        ' '.join([str(op_stack.data[i]) for i in range(op_stack.top)])
        if op_stack.top > 0
        else 'kosong'
    )
    out_str = ' '.join(output)
    langkah_log.append(('akhir', 'pop sisa stack', stk_str, out_str))

  return output, langkah_log


def hitung_postfix(postfix_tokens):
  val_stack = Stack()
  langkah_log = []

  for t in postfix_tokens:
    if t.isdigit():
      val_stack.push(int(t))
      tindakan = f'operand, push {t}'
    elif t in '+-*/':
      b = val_stack.pop()
      a = val_stack.pop()
      if a is None or b is None:
        return 0, langkah_log

      if t == '+':
        res = a + b
      elif t == '-':
        res = a - b
      elif t == '*':
        res = a * b
      elif t == '/':
        res = a // b if b != 0 else 0

      val_stack.push(res)
      tindakan = f'pop dua teratas -> hitung ({a} {t} {b}) = {res}'

    stk_str = (
        ' '.join([str(val_stack.data[i]) for i in range(val_stack.top)])
        if val_stack.top > 0
        else 'kosong'
    )
    langkah_log.append((t, tindakan, stk_str))

  total = val_stack.pop() if not val_stack.is_empty() else 0
  return total, langkah_log


# --- STRUKTUR DATA ANTREAN NAIF DAN CIRCULAR ---
class AntreanNaif:

  def __init__(self, capacity=10):
    self.capacity = capacity
    self.data = [None] * capacity
    self.count = 0

  def is_full(self):
    return self.count == self.capacity

  def _resize(self, new_capacity):
    new_data = [None] * new_capacity
    for i in range(self.count):
      new_data[i] = self.data[i]
    self.data = new_data
    self.capacity = new_capacity

  def enqueue(self, x):
    if self.is_full():
      self._resize(self.capacity * 2)
    self.data[self.count] = x
    self.count += 1

  def un_enqueue(self):
    if self.count == 0:
      return None
    self.count -= 1
    val = self.data[self.count]
    self.data[self.count] = None
    return val

  def size(self):
    return self.count


class AntreanMelingkar:

  def __init__(self, capacity=10):
    self.capacity = capacity
    self.data = [None] * capacity
    self.front = 0
    self.rear = 0
    self.count = 0

  def is_full(self):
    return self.count == self.capacity

  def _resize(self, new_capacity):
    new_data = [None] * new_capacity
    for i in range(self.count):
      new_data[i] = self.data[(self.front + i) % self.capacity]
    self.data = new_data
    self.front = 0
    self.rear = self.count
    self.capacity = new_capacity

  def enqueue(self, x):
    if self.is_full():
      self._resize(self.capacity * 2)
    self.data[self.rear] = x
    self.rear = (self.rear + 1) % self.capacity
    self.count += 1

  def un_enqueue(self):
    if self.count == 0:
      return None
    self.rear = (self.rear - 1 + self.capacity) % self.capacity
    val = self.data[self.rear]
    self.data[self.rear] = None
    self.count -= 1
    return val

  def size(self):
    return self.count