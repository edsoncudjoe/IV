from Tkinter import *
import requests
import json
from CatDVlib import Cdvlib


class App(Frame):

	def __init__(self, master=None):

		self.user = Cdvlib()

		Frame.__init__(self, master)
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		main = Frame(self)
		main.config(background="PeachPuff4", bd=3, relief=GROOVE)
		main.grid()

		login = Frame(main)
		login.grid(sticky=W, padx=5, pady=5)

		usr_search = Frame(main)
		usr_search.grid(sticky=W, padx=5, pady=5)

		res_list = Frame(main)
		res_list.grid(sticky=W, padx=5, pady=5)

		util_btns = Frame(main)
		util_btns.grid(sticky=S+E, padx=2, pady=2)

		######## USER LOGIN #######
		self.usr = Label(login, text="username: ")
		self.usr.grid(row=0, column=0)

		self.usernm = StringVar()
		self.usr_ent = Entry(login, textvariable=self.usernm)
		self.usr_ent.grid(row=0, column=1)

		self.pwd = Label(login, text="password: ")
		self.pwd.grid(row=0, column=2)

		self.passwrd = StringVar()
		self.pwd_ent = Entry(login, textvariable=self.passwrd, show="*")
		self.pwd_ent.grid(row=0, column=3)

		self.login_btn = Button(login, text="LOGIN", command=self.catdv_login)
		self.login_btn.grid(row=0, column=4)

		self.logout_btn = Button(login, text="LOG OUT", command=self.deleteSession)
		self.login_btn.grid(row=0, column=5)

		######## USER SEARCH ENTRY ######
		self.term = StringVar()
		self.clip = Entry(usr_search, width="90", textvariable=self.term)
		self.clip.grid(row=0, column=0, sticky=E)

		self.search_btn = Button(usr_search, text="SEARCH", command=self.get_query)
		self.search_btn.grid(row=0, column=1, sticky=E)

		##### scrollbar
		self.scrollbar = Scrollbar(res_list)
		self.scrollbar.grid(column=1, sticky=N+S+W)

		######## RESULTS ###########
		self.result = Listbox(res_list, bg='grey', width=100)
		self.result.grid(row=0, column=0)

		self.scrollbar.config(command=self.result.yview)
		self.result.config(yscrollcommand=self.scrollbar.set)

		self.clr_btn = Button(util_btns, text="Clear", command=self.clear_text)
		self.clr_btn.grid(row=1, column=0, sticky=E)

		self.button = Button(util_btns, text="QUIT", fg="red", command=login.quit)
		self.button.grid(row=1, column=1, sticky=E)



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

	def catdv_login(self):
		"""Enter CatDV server login details to get access to the API"""
		try:
			u = self.usernm.get()
			p = self.passwrd.get()
			self.auth = self.user.url + "/session?usr=" + str(u) + "&pwd=" + str(p)
			
			response = requests.get(self.auth)
			#print response.text
			self.data = json.loads(response.text)
			self.key = self.data['data']['jsessionid']
<<<<<<< HEAD
			self.result.insert(END, "Logged in to CatDV successfully.\n")
=======
			self.result.insert(END, "Login successful.\n")
			#self.result.insert(END, self.key)
>>>>>>> march12
			return self.key 
		except requests.exceptions.ConnectionError as e:
			print('\nCan\'t access the API.'
				' Please check you have the right domain address')
		except TypeError:
<<<<<<< HEAD
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
=======
			self.result.insert(END, "You provided incorrect login details. Please try again")
			# Maybe log to a file instead?
			#print('\nYou provided incorrect login details.'
			#	' Please check and try again.')

	def get_query(self):
		self.entry = self.term.get()
		self.res = requests.get(
			self.user.url + '/clips;jsessionid=' + self.key + '?filter=and((clip.name)'
				'has({}))&include=userFields'.format(str(self.entry)))
		self.data = json.loads(self.res.text)
		for i in self.data['data']['items']:
			try:
				if i['userFields']['U7']:
					self.result.insert(END, i['userFields']['U7'] + '  ' + i['name'])        
				else:
					self.result.insert(END, i['name'])
			except KeyError:
				pass
>>>>>>> march12

	def deleteSession(self):
		"""HTTP delete call to the API"""
		return requests.delete(self.user.url + '/session')


root = Tk()
app = App(master=root)

root.geometry()
#root.update()
root.minsize(root.winfo_width(), root.winfo_height())
root.title('CatDV QuickSearch')
app.mainloop()
#root.destroy()