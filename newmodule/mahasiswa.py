from openerp import fields,models

class Mahasiswa(models.Model):
	_name = "mahasiswa.mahasiswa"

	nama = fields.Char(size=32,string="Nama")
	kelas = fields.Char(size=32,string="Kelas")
	alamat = fields.Char(size=32,string="Alamat")