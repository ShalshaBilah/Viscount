# Comments
# Comments dalam python bisa menggunakan tanda # dan """

# Variables
# Variable adalah wadah untuk menyimpan suatu nilai data
# Nama variable harus dimulai dengan huruf atau karakter garis bawah
# Contoh : 
# a = 5
# b = "Salsa"
# print(a)
# print (b) Jika dijalankan maka akan otomatis mencetak nilai 5 dan text Salsa
# a = 10
# b = 5
# c = a+b
# print(c)           
#hasilnya adalah 15

# Data Types
# Number
# Ada 3 tipe data yaitu int, float, complex
# int yaitu bilangan bulat, positif atau negatif TANPA desimal
# float yaitu bilangan bulat, positif atau negatif yang terdapat desimal
# complex yaitu bilangan yang diperoleh dari akar bilangan rasional negatif.

# String
# Huruf yang diapit oleh tanda kutip tinggal atau tanda kutip ganda

# Boolean
# Tipe data yang hanya memiliki 2 nilai yaitu true and false

# Lists
# Tipe data yang digunakan untuk menyimpan banyak item dalam satu variable
# Ditulis menggunakan tanda []

# Tuples
# Tipe data kolektif yang bersifat immutable dan ordered. Dalam artian ia sama dengan list, hanya saja tuple tidak bisa diedit-edit.
# Ditulis menggunakan tanda ()

# Sets
# Ditulis menggunakan tanda {}
# tipe data kolektif yang bersifat unique, semua nilainya harus unik
# unordered, ia tidak bisa diakses via indeks (karena tidak berurut)
# unchangeable, dia tidak bisa diedit-edit (akan tetapi bisa ditambah dan dihapus).

# Dictionaries
# Tipe data pada python yang berfungsi untuk menyimpan kumpulan data/nilai dengan pendekatan “key-value”.
# Unordered - tidak berurutan
# Changeable - bisa diubah
# Unique - alias tidak bisa menerima dua keys yang sama

# Casting (Konversi tipe data)
# Konversi string ke numerik 
# panjang = int(input('Masukkan panjang: '))
# lebar = float(input('Masukkan lebar: '))
# print('Luas =', panjang * lebar)

# Konversi numerik ke string
# nama = 'Wudi'
# tahun_lahir = 2000
# print(nama + ' lahir di tahun ' + str(tahun_lahir))

# Konversi ke boolean
# Data yang bernilai “putih” atau kosong akan dianggap dan dikonversi sebagai False, sebaliknya data yang bernilai “hitam” atau tidak kosong akan dianggap dan dikonversi menjadi True.
print(type(None), '->', bool(None))
print(type(0), '->', bool(0))
print(type(0.0), '->', bool(0.0))
print(type(""), '->', bool(""))
print(type([]), '->', bool([]))
print(type(()), '->', bool(()))
print(type({}), '->', bool({}))

print("-" * 20)

print(type(5), '->', bool(5))
print(type(-14.5), '->', bool(-14.5))
print(type("Aku"), '->', bool("Aku"))
print(type([1, 2, 3]), '->', bool([1, 2, 3]))
print(type(("a", "b", False)), '->', bool(("a", "b", False)))
print(type({ 'nama': 'Lendis Fabri' }), '->', bool({ 'nama': 'Lendis Fabri' }))

# Konversi Dari dan Ke List, Set dan Tuple
# list ke tuple dan ke set
listHuruf = ['a', 'b', 'c', 'c']

print(listHuruf)
print(tuple(listHuruf))
print(set(listHuruf))
# tuple ke list dan ke set
tplBuah = ('Mangga', 'Jambu')

print(tplBuah)
print(list(tplBuah))
print(set(tplBuah))
# set ke list dan ke tuple
setAngka = {1, 3, 5, 5}

print(setAngka)
print(list(setAngka))
print(tuple(setAngka))

# Operators

# If-Else

# Loops
# While loops
# Perulangan uncountable atau perulangan yang jumlah proses pengulangannya tidak ditentukan. 
# Ia akan menjalankan baris kode di dalam blok kodenya secara terus menerus selama masih memenuhi ekspresi yang 
# sudah ditentukan sebelumnya, yang berarti ia akan terus mengulang selama kondisi bernilai TRUE.
# For loops