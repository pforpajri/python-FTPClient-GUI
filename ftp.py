import tkinter as tk
import ftplib as f

class Main:
	def __init__(self):
		self.main = tk.Tk()

		self.main.title("FTP Client")
		self.main.geometry("400x400")

		self.login()

		self.main.mainloop()

	def login(self,host=False,username=False,password=False):
		self.la = tk.Label(self.main,text="FTP Client",font=("Consolas",16,"bold"))
		self.la.pack(pady=20)

		self.host_label = tk.Label(self.main,text="Hostname/IP :").pack()
		self.host_input = tk.Entry(self.main)
		self.host_input.pack()
		
		self.user_label = tk.Label(self.main,text="Username :").pack()
		self.user_input = tk.Entry(self.main)
		self.user_input.pack()

		self.pass_label = tk.Label(self.main,text="Username :").pack()
		self.pass_input = tk.Entry(self.main,show="*")
		self.pass_input.pack()

		self.submit = tk.Button(self.main,text="Login")
		self.submit.bind("<Button-1>",lambda e: self.success(e))
		self.submit.pack(pady=10)


	def success(self,event):

		self.hostname = self.host_input.get()
		self.username = self.user_input.get()
		password = self.pass_input.get()

		if self.hostname == "" or self.username == "" or password == "":
			self.err = tk.Label(text="Masukkan semua input",bg="red",fg="white",font=("Arial",8))
			self.err.pack()
		else:
			try:
				self.host = f.FTP(self.hostname)
				self.host.login(user=self.username,passwd=password)

				self.main.destroy()

				self.main = tk.Tk()
				self.main.title("User "+str(self.username)+"@"+str(self.hostname))
				self.main.geometry("400x500")

				self.dir_list()
			except Exception as e:
				print(e)
				self.err = tk.Label(text="Login gagal !",bg="red",fg="white",font=("Arial",8))
				self.err.pack()
				# print("Login Gagal")

	def dir_list(self,dir_location="/",dir_prev=""):
		
		self.dir = self.host.nlst(dir_location)

		if dir_prev == "":
			self.btn = tk.Label()

		elif dir_prev == ['']:
			dp = "/"
			self.btn = tk.Button(text='Back to "'+str(dp)+'"')
			self.btn.bind("<Button-1>",lambda e: self.toPrevious(dp))
		else:
			dp = '/'.join(dir_prev)
			self.btn = tk.Button(text='Back to "'+str(dp)+'"')
			self.btn.bind("<Button-1>",lambda e: self.toPrevious(dp))
		
		self.list = tk.Listbox(self.main,height=20,font=("Arial",12))

		for i  in range(len(self.dir)):
			self.list.insert(i,self.dir[i])
			self.list.bind("<Double-Button-1>",self.onDouble)

		self.list.pack(fill="x")

		self.btn.pack(side="left")



	def toPrevious(self,dp):

		if dp == "/":
			dprev = ""
		else:
			dprev = dp.split("/")
			dprev.pop(-1)

		print(dp)

		self.btn.pack_forget()
		self.list.pack_forget()

		self.dir_list(dp,dprev)


	def onDouble(self, event):
		widget = event.widget
		selection=widget.curselection()
		value=widget.get(selection[0])
		if value:
			try:
				self.host.cwd(value)

				dir_prev=value.split("/")
				dir_prev.pop(-1)

				self.btn.pack_forget()
				self.list.pack_forget()

				self.dir_list(value,dir_prev)
			except Exception as e:
				print(e)
				print("TEST")

Main()