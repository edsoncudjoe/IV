from Tkinter import *
import requests
import json
from CatDVlib import Cdvlib


class App:

	def __init__(self, master):

		self.user = Cdvlib()

		frame = Frame(master)
		frame.grid()

		login = Frame(frame)
		login.config(background="yellow")
		login.grid(sticky=W)

		usr_search = Frame(frame)
		usr_search.config(background="blue")
		usr_search.grid(sticky=W)

		res_list = Frame(frame)
		res_list.config(background="yellow")
		res_list.grid(sticky=W)

		######## USER LOGIN #######
		self.usr = Label(login, text="username: ")
		self.usr.grid(row=0, column=0)

		self.usernm = StringVar()
		self.usr_ent = Entry(login, textvariable=self.usernm)
		self.usr_ent.grid(row=0, column=1)

		self.pwd = Label(login, text="password: ")
		self.pwd.grid(row=0, column=2)

		self.passwrd = StringVar()
		self.pwd_ent = Entry(login, textvariable=self.passwrd)
		self.pwd_ent.grid(row=0, column=3)

		self.login_btn = Button(login, text="LOGIN", command=self.catdv_login)
		self.login_btn.grid(row=0, column=4)

		#self.logout_btn = Button(login, text="LOG OUT", command=self.deleteSession)
		#self.login_btn.grid(row=1, column=5)

		######## USER SEARCH ENTRY ######
		self.term = StringVar()
		self.clip = Entry(usr_search, width="70", textvariable=self.term)
		self.clip.grid(row=0, column=0, sticky=E)

		self.search_btn = Button(usr_search, text="SEARCH", command=self.print_search)
		self.search_btn.grid(row=0, column=1, sticky=E)

		######## RESULTS ###########
		self.result = Listbox(res_list, bg='grey', width=100)
		self.result.grid(row=0, column=0)

		self.clr_btn = Button(frame, text="Clear", command=self.clear_text)
		self.clr_btn.grid(sticky=E)

		self.button = Button(frame, text="QUIT", fg="red", command=frame.quit)
		self.button.grid(sticky=E)



	def print_login(self):
		u = self.usernm.get()
		p = self.passwrd.get()
		self.result.insert(END, "username: " + str(u) + ".  password: " + str(p))
			
	def print_search(self):
		s = self.term.get()
		self.result.insert(END, "searched: " + str(s))

	def clear_text(self):
		self.result.delete(0, END)

##################### CatDVLogin####################

		
	
#user.getAuth()

	def catdv_login(self):
		"""Enter CatDV server login details to get access to the API"""
		try:
			u = self.usernm.get()
			p = self.passwrd.get()
			self.auth = self.user.url + "/session?usr=" + str(u) + "&pwd=" + str(p)
			self.response = requests.get(self.auth)
			self.data = json.loads(self.response.text)
			self.key = self.data['data']['jsessionid']
			self.result.insert(END, "Logged in to CatDV successfully.\n")
			return self.key 
		except requests.exceptions.ConnectionError as e:
			print('\nCan\'t access the API.'
				' Please check you have the right domain address')
		except TypeError:
			print('\nYou provided incorrect login details.'
				' Please check and try again.')
		

	def clipSearch(self):
		self.item = self.term.get()
		res = requests.get(
			self.url + '/clips;jsessionid=' + self.key + '?filter=and((clip.name)'
				'has({}))&include=userFields'.format(str(self.item)))
		self.data = json.loads(res.text)
		for i in self.data['data']['items']:
			if i['userFields']['U7']:        
				self.result.insert(END, i['userFields']['U7'] + ' ' + i['name'])
			else:
				self.result.insert(END, i['name'])

	def deleteSession(self):
		"""HTTP delete call to the API"""
		return requests.delete(self.url + '/session')


root = Tk()
app = App(root)

root.geometry()
#root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.title('api-search')
root.mainloop()
#root.destroy()