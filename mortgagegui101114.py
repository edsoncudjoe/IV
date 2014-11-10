# -*- coding: utf-8 -*-
##############################################################################
# Program: mortgagegui.py
# Purpose:  a GUI for a mortgage calculator. It will calculate the monthly 
#           payments of a mortgage term.  
#    
# Author: E. Cudjoe
# Date: 07/10/2014
#
#-----------------------------------------------------------------------------
# Version 1.0
#     Initial build
# ----------------------------------------------------------------------------
#TODO - format calculation output - Complete 08/10/14
#TODO - Handle user input errors 10/11/14
#
##############################################################################


from Tkinter import *
import tkMessageBox

class Application(Frame):
	"""Mortgage calulator GUI"""

	def __init__(self, master):
		"""Initialize the frame"""
		Frame.__init__(self, master)
		self.grid()
		self.create_widgets()

	def create_widgets(self):
		"""Buttons, labels and text entry"""
		#Mortgage Amount
		self.property_price = Label(self, text="Enter the property value (£):", 
			pady=10)
		self.property_price.grid(row=0, column=0)

		self.property_entry = Entry(self)
		self.property_entry.grid(row=0, column=1)

		#Deposit amount
		self.deposit = Label(self, text="Enter your deposit amount (£):", 
			pady=10)
		self.deposit.grid(row=1, column=0)

		self.deposit_entry = Entry(self)
		self.deposit_entry.grid(row=1, column=1)

		#Interest amount
		self.interest = Label(self, text="Enter your bank's interest rate (%):", 
			pady=10)
		self.interest.grid(row=2, column=0)

		self.interest_entry = Entry(self)
		self.interest_entry.grid(row=2, column=1)

		#Length of term
		self.length_of_term = Label(self, 
			text="Enter the length of the mortgage term (years):")
		self.length_of_term.grid()

		self.term_entry = Entry(self)
		self.term_entry.grid(row=3, column=1)

		#Calculator button
		self.calc_button = Button(self, text="Calculate", 
			command=self.monthlyPay)
#		self.calc_button(self, = self.answers
		self.calc_button.grid(column=1)

		#calculation results
		self.result = Text(self, x=0, y=50, width=70, height=10, wrap=WORD)
		self.result.grid(columnspan=2)
			

	def monthlyPay(self):
		"""calculates monthly payment rate"""
		value = self.property_entry.get().replace(',', '')
		deposit = self.deposit_entry.get().replace(',', '')
		interest = self.interest_entry.get()
		term = self.term_entry.get()

		if value.isdigit():
			house_price = int(value)
		else:
			tkMessageBox.showerror("Error1", 
				"Please check that all fields entered are numbers.")
		if deposit.isdigit():
			user_deposit = int(deposit)
		else:
			tkMessageBox.showerror("Error1", 
				"Please check that all fields entered are numbers.")
		if interest.isdigit():
			user_interest = float(interest)
		else:
			tkMessageBox.showerror("Error1", 
				"Please check that all fields entered are numbers.")
		if term.isdigit():
			user_term = int(term)
		else:
			tkMessageBox.showerror("Error1", 
				"Please check that all fields entered are numbers.")

		loan = house_price - user_deposit
		interest_as_decimal = user_interest / 100
		interest_per_permonth = interest_as_decimal / 12
		total_months = 12 * user_term
		interest_over_term = (1 + interest_as_decimal / 12) ** total_months
		final = loan * ((interest_per_permonth * interest_over_term) / 
			(interest_over_term - 1))

		#Print results
		self.result.delete(0.0, END)
		self.result.insert(0.0, 
			"Your monthly payments will be approximately £%6.2f " % final)




def main():
	root = Tk()

	root.title('Mortgage Monthly Payment Calculator')
	root.geometry('525x350+100+100')

	app = Application(root)
	app.grid()

	root.mainloop()

if __name__ == '__main__':
	main()
