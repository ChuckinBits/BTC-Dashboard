from tkinter import *
from tkinter import messagebox
import requests
from PIL import ImageTk,Image
from urllib.request import urlopen
import config

global customtk
try:
	import customtkinter
	customtk = True
except:
	customtk = False

def settingsMenu():
	# slider values (min 1 second, max 24 hours)
	minval = 1
	maxval = 24

	def testConnection():
		#Tests custom node IP:Port to ensure proper connectivity
		try:
			e_url = ip_entry.get()
			urltest = requests.get(e_url)
			status = urltest.status_code
			urltest.close()
			print("Tried connecting to: " + e_url + " Status code: " + str(status))
			b_url = e_url + "api/blocks/tip/height"
			urltest = requests.get(b_url)
			status = urltest.status_code
			urltest.close()
			print("Tried connecting to: " + b_url + " Status code: " + str(status))
			d_url = e_url + 'api/v1/difficulty-adjustment'
			urltest = requests.get(b_url)
			status = urltest.status_code
			urltest.close()
			print("Tried connecting to: " + d_url + " Status code: " + str(status))
			f_url = e_url + 'api/v1/fees/recommended'
			urltest = requests.get(f_url)
			status = urltest.status_code
			urltest.close()
			print("Tried connecting to: " + f_url + " Status code: " + str(status))
			t_url = e_url + 'api/mempool'
			urltest = requests.get(t_url)
			status = urltest.status_code
			urltest.close()
			print("Tried connecting to: " + t_url + " Status code: " + str(status))
			print("Success on all node tests!")
			messagebox.showinfo("Success!", "Success on all node tests!", parent=settings)
		except:
			print("Tried connecting to: " + e_url)
			print("Error Connecting to Node!")
			messagebox.showerror("Error!", "Error Connecting to Node!\nCheck your URL and try again.", parent=settings)

	def nodeEnable():
		#Check if Custom Node is checked to enable Custom Node IP:Port text field
		choice = src.get()
		if customtk == True:
			if choice == 0:
				ip_entry.configure(state=DISABLED, text_color=["gray52", "gray62"])
				test_button.configure(state=DISABLED)
			else:
				ip_entry.configure(state=NORMAL, text_color=["gray20", "gray90"])
				test_button.configure(state=NORMAL)
		else:
			if choice == 0:
				ip_entry.configure(state=DISABLED)
				test_button.configure(state=DISABLED)
			else:
				ip_entry.configure(state=NORMAL)
				test_button.configure(state=NORMAL)

	def connectToNode():
		#Update refresh time and mempool node source with and display updated values in a messagebox
		global articles
		global node_connected
		global new_refreshtime
		global refresh_seconds

		suffix_msg = ""
		try:
			articles
		except NameError:
			articles = int(config.articlecount)
		try:
			refresh_seconds
		except NameError:
			refresh_seconds = int(config.refreshtime / 1000)
		
		config.new_refreshtime = int(refresh_seconds) * 1000
		if int(refresh_seconds) == int(config.refreshtime / 1000):
			refresh_msg = ""
		else:
			refresh_msg = "\nRefresh time set to " + time_text
			suffix_msg = ".\nNew settings will apply after the next refresh"
		
		if art_var.get() == config.articlecount:
			articles_msg = ""
		else:
			articles_msg = "\nSet to display the latest " + str(art_var.get()) + " articles"
			suffix_msg = ".\nNew settings will apply after the next refresh"
			config.articlecount = art_var.get()

		if src.get() == 0:
			try:
				urltest = requests.get('https://mempool.space/')
				status = urltest.status_code
				urltest.close()
				config.node_connected = 0
				messagebox.showinfo("Success!", "Successfully connected to Mempool.Space!" + refresh_msg + articles_msg + suffix_msg, parent=settings)
				settings.destroy()
			except:
				messagebox.showerror("Error!", "Error Connecting to Mempool.Space!\nTry again later." + refresh_msg + articles_msg + suffix_msg, parent=settings)
		else:
			try:
				node_url = ip_entry.get()
				urltest = requests.get(node_url)
				status = urltest.status_code
				urltest.close()
				print("Tried connecting to: " + node_url + " Status code: " + str(status))
				print("Successfully connected to custom node!")
				config.node_connected = 1
				config.ip_url = node_url
				messagebox.showinfo("Success!", "Successfully connected to custom node!" + refresh_msg + articles_msg + suffix_msg, parent=settings)
				settings.destroy()
			except:
				print("Tried connecting to: " + node_url)
				print("Error Connecting to Node!")
				messagebox.showerror("Error!", "Error Connecting to Node!\nCheck your URL and try again." + refresh_msg + articles_msg + suffix_msg, parent=settings)
	
	def add_news():
		#art = articles.get()
		#art += 1
		#articles.set(art)
		art_var.set(art_var.get()+1)
		articles_label.configure(text=str(art_var.get()))
		articles_slider.set(art_var.get())
		articles_buttons_state()

	def sub_news():
		art = art_var.get()
		art -= 1
		art_var.set(art)
		articles_label.configure(text=str(art))
		articles_slider.set(art)
		articles_buttons_state()

	def articles_buttons_state():
		art = art_var.get()
		if art == 1:
			subtract_news_button.configure(state=DISABLED, fg_color='darkgray')
		elif art == 25:
			add_news_button.configure(state=DISABLED, fg_color='darkgray')
		else:
			add_news_button.configure(state=NORMAL, fg_color=["#72CF9F", "#11B384"])
			subtract_news_button.configure(state=NORMAL, fg_color=["#72CF9F", "#11B384"])

	def articles_change(self):
		global articles_slider_value
		articles_label.configure(text=str(art_var.get()))
		articles_slider_value = art_var.get()

	def slider_change(self):
		#Sets slider value to various refresh times
		global refresh_seconds
		global time_text
		global slider_value
		global var
		var = spin_var.get()
		x = var
		if var == 1:
			refresh_seconds = var
			time_text = "1 second"
		elif var > 1 and var <= 5:
			refresh_seconds = var
			time_text = str(var) + " seconds"
		elif var == 6:
			refresh_seconds = 10
			time_text= "10 seconds"
		elif var == 7:
			refresh_seconds = 15
			time_text= "15 seconds"
		elif var == 8:
			refresh_seconds = 30
			time_text= "30 seconds"
		elif var == 9:
			refresh_seconds = 60
			time_text = "1 minute"
		elif var > 9 and var < 14:
			x = var - 8
			refresh_seconds = x * 60
			time_text = str(x) + " minutes"
		elif var == 14:
			refresh_seconds = 10 * 60
			time_text = "10 minutes"
		elif var == 15:
			refresh_seconds = 15 * 60
			time_text = "15 minutes"
		elif var == 16:
			refresh_seconds = 30 * 60
			time_text = "30 minutes"
		elif var == 17:
			refresh_seconds = 60 * 60
			time_text = "1 hour"
		elif var > 17 and var < 21:
			x = var - 16
			refresh_seconds = x * 60 * 60
			time_text = str(x) + " hours"
		elif var == 21:
			refresh_seconds = 8 * 60 * 60
			time_text = "8 hours"
		elif var == 22:
			refresh_seconds = 12 * 60 * 60
			time_text = "12 hours"
		elif var == 23:
			refresh_seconds = 18 * 60 * 60
			time_text = "18 hours"
		elif var == 24:
			refresh_seconds = 24 * 60 * 60
			time_text = "24 hours"
		else:
			time_text = "Error"
		refresh_conv.configure(text=time_text)
		slider_value = var

	def checkCustomRefresh(check):
		global time_text
		if check < 60:
			secs = check
		elif check >= 60 and check < (60 * 60):
			mins = check // 60
			secs = check % 60
		elif check >= 60 * 60:
			hrs = check//3600
			mins = (check % 3600) // 60
			secs = (check % 3600) % 60
		if check == 1:
			time_text = str(secs) + " second"
			return 1
		elif check > 1 and check < 6:
			time_text = str(secs) + " seconds"
			return check
		elif check >= 6 and check <= 10:
			time_text = str(secs) + " seconds"
			return 6
		elif check > 10 and check <= 15:
			time_text = str(secs) + " seconds"
			return 7
		elif check > 15 and check <= 30:
			time_text = str(secs) + " seconds"
			return 8
		elif check > 30 and check < 60:
			time_text = str(secs) + " seconds"
			return 9
		elif check == 60:
			time_text = str(mins) + " minute"
			return 9
		elif check > 60 and check <= (60 * 5):
			time_text = str(mins) + " minutes " + str(secs) + " seconds"
			return 8 + (mins)
		elif check > (60 * 5) and check <= (60 * 10):
			time_text = str(mins) + " minutes " + str(secs) + " seconds"
			return 14
		elif check > (60 * 10) and check <= (60 * 15):
			time_text = str(mins) + " minutes " + str(secs) + " seconds"
			return 15
		elif check > (60 * 15) and check <= (60 * 30):
			time_text = str(mins) + " minutes " + str(secs) + " seconds"
			return 16
		elif check > (60 * 30) and check < (60 * 60):
			time_text = str(mins) + " minutes " + str(secs) + " seconds"
			return 17
		elif check == (60 * 60):
			time_text = str(hrs) + " hour"
			return 17
		elif check > (60 * 60) and check <= (60 * 60 * 4):
			time_text = str(hrs) + " hours " + str(mins) + " minutes " + str(secs) + " seconds"
			return 16 + hrs
		elif check > (4 * 60 * 60) and check <= (8 * 60 * 60):
			time_text = str(hrs) + " hours " + str(mins) + " minutes " + str(secs) + " seconds"
			return 21
		elif check > (8 * 60 * 60) and check <= (12 * 60 * 60):
			time_text = str(hrs) + " hours " + str(mins) + " minutes " + str(secs) + " seconds"
			return 22
		elif check > (12 * 60 * 60) and check <= (18 * 60 * 60):
			time_text = str(hrs) + " hours " + str(mins) + " minutes " + str(secs) + " seconds"
			return 23
		elif check > (18 * 60 * 60) and check < (24 * 60 * 60):
			time_text = str(hrs) + " hours " + str(mins) + " minutes " + str(secs) + " seconds"
			return 24
		else:
			time_text = str(hrs) + " hours"
			return 24

	def on_closing():
		#Set the slider value to the refresh time when closing the settings window
		global slider_value
		global articles_slider_value
		slider_value = checkCustomRefresh(config.new_refreshtime // 1000)
		articles_slider_value = config.articlecount
		settings.destroy()

	global ip_entry
	global settings
	global slider_value
	global src

	try:
		slider_value
	except NameError:
		slider_value = checkCustomRefresh(config.default_refresh)
	try:
		articles_slider_value
	except NameError:
		articles_slider_value = config.articlecount
	try:
		articles_text
	except NameError:
		articles_text = str(config.articlecount)


	art_var = IntVar()
	art_var.set(articles_slider_value)
	spin_var = IntVar()
	spin_var.set(slider_value)

	if customtk == True:
		settings_width = 550
		settings_height = 480
		customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
		customtkinter.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green
		settings = customtkinter.CTkToplevel()
		frame_all = customtkinter.CTkFrame(master=settings)
		frame_all.grid(pady=20, padx=30)
		### Declare Images ###
		ip_text = StringVar()
		ip_text.set(config.ip_url)
		try:
			add_news_image = ImageTk.PhotoImage(Image.open("images\add-news.png").resize((35,35), Image.ANTIALIAS))
			subtract_news_image = ImageTk.PhotoImage(Image.open("images\subtract-news.png").resize((35,35), Image.ANTIALIAS))
		except:
			add_news_image = ImageTk.PhotoImage(Image.open("images/add-news.png").resize((35,35), Image.ANTIALIAS))
			subtract_news_image = ImageTk.PhotoImage(Image.open("images/subtract-news.png").resize((35,35), Image.ANTIALIAS))
		### Refresh Interval ###
		refresh_label = customtkinter.CTkLabel(frame_all, text="Refresh Interval", text_font=('Helvetica',20, 'bold'), text_color='#f2a900')
		refresh_label.grid(row=0, column=1, columnspan=3, ipady=20)
		refresh_conv = customtkinter.CTkLabel(frame_all, text=time_text, text_font=('Helvetica', 16))
		slider = customtkinter.CTkSlider(frame_all, from_=minval, to=maxval, variable=spin_var, command=slider_change)
		###  News Article Slider ###
		news_title = customtkinter.CTkLabel(frame_all, text="Latest News Articles", text_font=('Helvetica',20, 'bold'), text_color='#f2a900')
		news_title.grid(row=3, column=1, columnspan=3, ipady=20)
		subtract_news_button = customtkinter.CTkButton(frame_all, image=subtract_news_image, text="", width=40, height=40, compound="right", command=sub_news)
		subtract_news_button.grid(row=4, column=1, columnspan=2)
		articles_label = customtkinter.CTkLabel(frame_all, text=articles_text, text_font=('Helvetica', 16), width=40)
		add_news_button = customtkinter.CTkButton(frame_all, image=add_news_image, text="", width=40, height=40, compound="left", command=add_news)
		add_news_button.grid(row=4, column=2, columnspan=2, pady=(0,0))
		articles_slider = customtkinter.CTkSlider(frame_all, from_=1, to=25, variable=art_var, command=articles_change)
		### Mempool Source ###
		top_label = customtkinter.CTkLabel(frame_all, text="Mempool Source", text_font=('Helvetica',20, 'bold'), text_color='#f2a900')
		#r_memp = customtkinter.CTkRadioButton(settings, text="Default", variable=src, value=0, command=nodeEnable, text_font=('Helvetica',14))
		#r_custom = customtkinter.CTkRadioButton(settings, text="Custom Node", variable=src, value=1, command=nodeEnable, text_font=('Helvetica',14))
		mempool_label = customtkinter.CTkLabel(frame_all, text="mempool.space", text_font=('Helvetica',14))
		mempool_label.grid(row=7, column=1, columnspan=2, padx=(0,70))
		src = customtkinter.CTkSwitch(frame_all, text="Custom Node", command=nodeEnable, text_font=('Helvetica',14), onvalue=1, offvalue=0)
		src.grid(row=7, column=2, columnspan=3, padx=(0,0), pady=(10,10))
		url_label = customtkinter.CTkLabel(frame_all, text="Node URL", text_font=('Helvetica',14))
		url_label.grid(row=8, column=1, padx=(10,0))
		ip_entry = customtkinter.CTkEntry(frame_all, text_font=('Helvetica',14), textvariable=ip_text, width=250)
		ip_entry.grid(row=8, column=2, padx=(0,0))
		test_button = customtkinter.CTkButton(frame_all, text="Test", text_font=('Helvetica', 14), command=testConnection, width=60)
		test_button.grid(row=8, column=3, padx=(0,30))
		connect_button = customtkinter.CTkButton(frame_all, text="Apply", text_font=('Helvetica',14, 'bold'), bg='#f2a900', width=300, command=connectToNode)
		connect_button.grid(row=9, column=0, columnspan=4, pady=30)
		if config.node_connected == 1:
			src.select()
		else:
			src.deselect()
	else:
		settings_width = 480
		settings_height = 400
		### Classic Tkinter ###
		settings = Toplevel()
		src = IntVar()
		src.set(config.node_connected)
		### Refresh Interval ###
		refresh_label = Label(settings, text="Refresh Interval", font=('Helvetica',18, 'bold'))
		refresh_label.grid(row=0, column=1, columnspan=3, ipady=5)
		refresh_conv = Label(settings, text=time_text, font=('Helvetica', 16))
		slider = Scale(settings, from_=minval, to=maxval, orient='horizontal', showvalue=0, variable=spin_var, command=slider_change)
		### News Articles Slider ###
		news_title = Label(settings, text="Latest News Articles", font=('Helvetica',18, 'bold'))
		news_title.grid(row=3, column=1, columnspan=3, ipady=5)
		articles_label = Label(settings, text=articles_text, font=('Helvetica', 16))
		articles_slider = Scale(settings, from_=1, to=25, orient='horizontal', showvalue=0, variable=art_var, command=articles_change)
		### Mempool Source ###
		top_label = Label(settings, text="Mempool Source", font=('Helvetica',18, 'bold'))
		r_memp = Radiobutton(settings, text="Default", variable=src, value=0, command=nodeEnable, font=('Helvetica',14))
		r_memp.grid(row=7, column=1, columnspan=2, padx=(0,120), pady=(5,10))
		r_custom = Radiobutton(settings, text="Custom Node", variable=src, value=1, command=nodeEnable, font=('Helvetica',14))
		r_custom.grid(row=7, column=2, columnspan=2, padx=(0,0), pady=(5,10))
		url_label = Label(settings, text="Node URL", font=('Helvetica',14))
		url_label.grid(row=8, column=1, padx=(30,0))
		ip_entry = Entry(settings, font=('Helvetica',14), width=25)
		ip_entry.grid(row=8, column=2)
		ip_entry.insert(0, config.ip_url)
		test_button = Button(settings, text="Test", font=('Helvetica', 14), command=testConnection)
		test_button.grid(row=8, column=3)
		connect_button = Button(settings, text="Apply", font=('Helvetica',14, 'bold'), bg='#f2a900', width=30, command=connectToNode)
		connect_button.grid(row=9, column=0, columnspan=4, pady=10)
	config.width_value=config.root.winfo_screenwidth()
	config.height_value=config.root.winfo_screenheight()
	settings_x = int((config.width_value / 2) - (settings_width / 2))
	settings_y = int((config.height_value / 2) - (settings_height / 2))
	settings.geometry(f'{settings_width}x{settings_height}+{settings_x}+{settings_y}')
	settings.title('Settings')
	try:
		img = PhotoImage(file=r'images\btcicon.png')
	except:
		img = PhotoImage(file=r'images/btcicon.png')
	settings.tk.call('wm', 'iconphoto', settings._w, img)
	refresh_conv.grid(row=1, column=1, columnspan=3)
	slider.grid(row=2, column=1, columnspan=3)
	slider.set(slider_value)
	articles_label.grid(row=4, column=1, columnspan=3)
	articles_slider.grid(row=5, column=1, columnspan=3)
	articles_slider.set(articles_slider_value)
	top_label.grid(row=6, column=1, columnspan=3)
	nodeEnable()
	settings.update()
	settings.protocol("WM_DELETE_WINDOW", on_closing)
	config.root.wait_window(settings)