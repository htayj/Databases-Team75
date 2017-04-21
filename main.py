import Tkinter as tk
from Tkinter import *
import api
import tktable
# from Tkinter import ttk
LARGE_FONT=("Verdana", 12)

## TODO
# pending data points
# pending city officials
# fix datetime

class TKMain (tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)


        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # All frames (pages) must be included in this list
        for F in (LoginPage, RegisterPage, SciPortalPage, AddDPPage, AddPOIPage, OffPortalPage, AdminPortalPage, ViewPOIPage, POIReportPage, PDPPage, POPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky=N+E+S+W)
        self.show_frame(LoginPage)


    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()


class PageTemplate(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)

class LoginPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Login", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10, sticky=N+E+S+W)

        uname_label = tk.Label(self, text="Username").grid(row=1, column=0, pady = 20)
        pwd_label = tk.Label(self, text="Password").grid(row=2, column=0, pady = 20)

        uname_entry = tk.Entry(self)
        uname_entry.grid(row=1, column=1, pady = 20, padx= 20)
        pwd_entry = tk.Entry(self)
        pwd_entry.grid(row=2, column=1, pady = 20, padx= 20)


        reg_button = tk.Button(self, text="Register", command=lambda :self.register(controller))
        reg_button.grid(row=4, column=0, padx = 20, pady = 10)

        login_button = tk.Button(self, text="Login", command=lambda :self.login(controller, uname_entry.get(), pwd_entry.get()))
        login_button.grid(row=4, column=1, padx = 20, sticky="E")

        # table = tktable.Table(parent, 
        #     rows = 5,
        #     cols = 5
        # )
        # table.grid(row=5)



    def login(self, controller, uname, pwd):
        user_type  = api.login(uname, pwd)
        #check login creds
        #
        if user_type == "Invalid":
            return
        #   create popup window sayig its invalid
        #
        if user_type == "Admin":
            controller.show_frame(AdminPortalPage)

        #   go to admin portal
        #
        if user_type == "City Official":
            controller.show_frame(OffPortalPage)
        #   go to city official portal
        #
        if user_type == "City Scientist":
            controller.show_frame(SciPortalPage)
        #   go to city scientist portal


        # controller.show_frame(SciPortalPage)

        # controller.show_frame(OffPortalPage)
        # controller.show_frame(AdminPortalPage)


    def register(self, controller):
        controller.show_frame(RegisterPage)

class RegisterPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Register", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        uname_label = tk.Label(self, text="Username").grid(row=1, column=0, pady = 5)
        email_label = tk.Label(self, text="Email").grid(row=2, column=0, pady = 5)
        pwd_label = tk.Label(self, text="Password").grid(row=3, column=0, pady = 5)
        cpwd_label = tk.Label(self, text="Confirm Password").grid(row=4, column=0, pady = 5)
        type_label = tk.Label(self, text="User Type").grid(row=5, column=0, pady = 5)

        uname_entry = tk.Entry(self)
        uname_entry.grid(row=1, column=1, pady = 5, padx= 20)
        email_entry = tk.Entry(self)
        email_entry.grid(row=2, column=1, pady = 5, padx= 20)
        pwd_entry = tk.Entry(self)
        pwd_entry.grid(row=3, column=1, pady = 5, padx= 20)
        cpwd_entry = tk.Entry(self)
        cpwd_entry.grid(row=4, column=1, pady = 5, padx= 20)

        #variable in the dropdown
        type_var = StringVar(self)
        type_var.set("City Officials")
        #set trace on var
        # observer_name = trace_variable("w", callback)

        #dropdown box
        type_option = OptionMenu(self, type_var, "City Officials", "City Scientists").grid(row=5, column=1, padx = 20, pady = 10, sticky = "W")

        #TODO: add section that depends on user type


        officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        officials_frame.grid(row = 6, columnspan=2, padx = 20)

        officials_title = tk.Label(officials_frame, text="Fill out this form if you chose city official").grid(row=0, column=0, pady = 5, columnspan=2)
        city_label = tk.Label(officials_frame, text="City").grid(row=1, column=0, pady = 5)
        state_label = tk.Label(officials_frame, text="State").grid(row=2, column=0, pady = 5)
        title_label = tk.Label(officials_frame, text="Title").grid(row=3, column=0, pady = 5)

        ## city option menu
        city_options = self.get_city_options()
        city_var = StringVar(self)
        city_var.set(city_options[0])

        city_dropdown = apply(OptionMenu, (officials_frame, city_var) + tuple(city_options))
        city_dropdown.grid(row=1, column=1, padx = 20, pady = 5, sticky="W")

        ## state option menu
        state_options = self.get_state_options()
        state_var = StringVar(self)
        state_var.set(state_options[0])
        state_dropdown = apply(OptionMenu, (officials_frame, state_var) + tuple(state_options))
        state_dropdown.grid(row=2, column=1, padx = 20, pady = 5, sticky="W")


        title_entry = tk.Entry(officials_frame)
        title_entry.grid(row=3, column=1, pady = 5, padx=20)

        city_official_info = (city_var.get(), state_var.get(), title_entry.get())
        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller, uname_entry.get(),  email_entry.get(),  pwd_entry.get(), cpwd_entry.get(), type_var.get(), city_official_info))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def submit(self, controller, username, email, pwd, cpwd, user_type, type_args): #FIXME: probably need to pass an array with values to register with
        api.add_user(username, email, pwd, cpwd, user_type, type_args) #FIXME: error handling
        controller.show_frame(LoginPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(LoginPage)

    def get_state_options(self): 
        return api.get_states()

    def get_city_options(self): #FIXME: pass in state?
        return api.get_cities()

class SciPortalPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Choose Functionality", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        add_dp_button = tk.Button(self, text="Add Data Point", command=lambda :self.add_dp(controller)).grid(row=1, column=0, padx = 20, pady = 10)
        add_poi_button = tk.Button(self, text="Add POI", command=lambda :self.add_poi(controller)).grid(row=2, column=0, padx = 20, pady = 10)

        logout_button = tk.Button(self, text="Logout", command=lambda :self.logout(controller)).grid(row=3, column=0, padx = 20, pady = 10, sticky="W")


    def add_dp(self, controller):
        controller.show_frame(AddDPPage)

    def add_poi(self, controller):
        controller.show_frame(AddPOIPage)

    def logout(self, controller):
        api.logout()
        controller.show_frame(LoginPage)



class AddDPPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Add Data Point", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5)
        timedate_label = tk.Label(self, text="Time and Date of Data Reading").grid(row=2, column=0, pady = 5)
        datatype_label = tk.Label(self, text="Data Type").grid(row=3, column=0, pady = 5)
        dataval_label = tk.Label(self, text="Data Value").grid(row=4, column=0, pady = 5)

        timedate_entry = tk.Entry(self)
        timedate_entry.grid(row=2, column=1, pady = 5, padx= 20)
        dataval_entry = tk.Entry(self)
        dataval_entry.grid(row=4, column=1, pady = 5, padx= 20)


        ## location option menu
        #variable in the dropdown
        loc_options = self.get_loc_options()
        locname_var = StringVar(self)
        locname_var.set(loc_options[0])

        loc_dropdown = apply(OptionMenu, (self, locname_var) + tuple(loc_options))
        loc_dropdown.grid(row=1, column=1, padx = 20, pady = 10, sticky="W")

        ## datatype option menu
        datatype_options = self.get_datatype_options()
        datatype_var = StringVar(self)
        datatype_var.set(datatype_options[0])
        datatype_dropdown = apply(OptionMenu, (self, datatype_var) + tuple(datatype_options))
        datatype_dropdown.grid(row=3, column=1, padx = 20, pady = 10, sticky="W")

        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def submit(self, controller): #FIXME: probably need to pass an array with values to register with
        controller.show_frame(SciPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(SciPortalPage)

    def get_loc_options(self): #FIXME: get these from database
        return [ "Atl, GA","NYC, NY","San Fran, CA"]

    def get_datatype_options(self): #FIXME: get these from database
        return [ "Mold","Air Quality reading"]

class AddPOIPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Add a New Location", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5)
        city_label = tk.Label(self, text="City").grid(row=2, column=0, pady = 5)
        state_label = tk.Label(self, text="State").grid(row=3, column=0, pady = 5)
        zip_label = tk.Label(self, text="Zip Code").grid(row=4, column=0, pady = 5)

        locn_entry = tk.Entry(self)
        locn_entry.grid(row=1, column=1, pady = 5, padx= 20)
        dataval_entry = tk.Entry(self)
        dataval_entry.grid(row=4, column=1, pady = 5, padx= 20)

        ## city option menu
        city_options = self.get_city_options()
        city_var = StringVar(self)
        city_var.set(city_options[0])

        city_dropdown = apply(OptionMenu, (self, city_var) + tuple(city_options))
        city_dropdown.grid(row=3, column=1, padx = 20, pady = 10, sticky="W")

        ## state option menu
        state_options = self.get_state_options()
        state_var = StringVar(self)
        state_var.set(state_options[0])
        state_dropdown = apply(OptionMenu, (self, state_var) + tuple(state_options))
        state_dropdown.grid(row=2, column=1, padx = 20, pady = 10, sticky="W")

        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def submit(self, controller): #FIXME: probably need to pass an array with values to register with
        controller.show_frame(SciPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(SciPortalPage)

    def get_state_options(self): 
        return [ "atl","nyc","san fran"]

    def get_city_options(self): #FIXME: pass in state?
        return [ "GA","TN", "CA", "NY"]



class OffPortalPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Choose Functionality", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        fs_poi_button = tk.Button(self, text="Filter/Search POI", command=lambda :self.fs_poi(controller)).grid(row=1, column=0, padx = 20, pady = 10)
        poi_report_button = tk.Button(self, text="POI Report", command=lambda :self.poi_report(controller)).grid(row=2, column=0, padx = 20, pady = 10)

        logout_button = tk.Button(self, text="Logout", command=lambda :self.logout(controller)).grid(row=3, column=0, padx = 20, pady = 10, sticky="W")

    def fs_poi(self, controller):
        controller.show_frame(ViewPOIPage)

    def poi_report(self, controller):
        controller.show_frame(POIReportPage)

    def logout(self, controller):
        api.logout()
        controller.show_frame(LoginPage)

class POIReportPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="POI Report", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        # table goes here
                ##table stuff
        table_frame = tk.Frame(self)
        table_frame.grid(row=2,column=0, columnspan=2, padx=0,pady=5)
        numrows, numcols = 0, 11

        var = tktable.ArrayVar(table_frame)
        for y in range(numrows):
            for x in range(numcols):
                index = "%i,%i" % (y, x)
                var[index] = index

        table = tktable.Table(table_frame, 
            rows = numrows,
            cols = numcols,
            state='normal',
            titlerows=1,
            titlecols=0,
            colwidth=10,
            height=10,
            roworigin=-1,
            colorigin=-1,
            selectmode='extended',
            selecttype='row',
            rowstretch='all',
            colstretch='last',
            # browsecmd=browsecmd,
            flashmode='on',
            variable=var,
            usecommand=0
        )
        scroll = Scrollbar(table_frame, orient='vertical', command=table.yview_scroll)
        table.config(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        table.pack(expand=1, fill='y')
        
        # table.grid(row=0, column=0)
        # scroll.grid(row=0, column=1)
        titles = ("Location Name", "City", "State", "Zip Code", "Flagged", "Date Flagged")
        r = table.index('end').split(',')[0]
        print r
        index = r + ",-1"
        table.set("row", "-1,-1", "Results")

        filters = []
        apply_button = tk.Button(self, text="Show Report", command=lambda :self.apply_filter(controller, table, filters))
        apply_button.grid(row=1, column=0, padx = 20, pady = 10, sticky="E")

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def apply_filter(self, controller, table, filters): #FIXME: probably need to pass an array with values to filter with
        titles = ("POI Location", "City", "State", "Mold Min", "Mold Avg", "Mold Max", "AQ Min", "AQ Avg", "AQ Max", "# of Data points", "Flagged?")
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *titles)
        table.see(idx)
        filtered_poi = api.get_poi_report()
        for r in filtered_poi:
            self.add_new_data(r, table)

    def add_new_data(self, row, table):
        #table.config(state='normal')
        table.insert_rows('end', 1)
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *row)
        table.see(idx)
        #table.config(state='disabled')


    def back(self, controller):
        controller.show_frame(OffPortalPage)

class ViewPOIPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="View POI", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10, padx=20)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5, sticky = 'E')
        city_label = tk.Label(self, text="City").grid(row=2, column=0, pady = 5, sticky = 'E')
        state_label = tk.Label(self, text="State").grid(row=3, column=0, pady = 5, sticky = 'E')
        zip_label = tk.Label(self, text="Zip Code").grid(row=4, column=0, pady = 5, sticky = 'E')
        flag_label = tk.Label(self, text="Flagged").grid(row=5, column=0, pady = 5, sticky = 'E')

        ## date chooser stuff
        dateflag_label = tk.Label(self, text="Date Flagged").grid(row=6, column=0, pady = 5, sticky="E")
        date_frame = tk.Frame(self)
        date_frame.grid(row=6, column=1, pady = 5, sticky="W", padx = 20)

        #month
        month_options = self.get_month_options()
        month_var = StringVar(self)
        month_var.set(month_options[0])

        month_dropdown = apply(OptionMenu, (date_frame, month_var) + tuple(month_options))
        month_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(date_frame, text="/").grid(row=0, column=1, sticky = 'E')

        #day
        day_options = self.get_day_options()
        day_var = StringVar(self)
        day_var.set(day_options[0])

        day_dropdown = apply(OptionMenu, (date_frame, day_var) + tuple(day_options))
        day_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        slash_label2 = tk.Label(date_frame, text="/").grid(row=0, column=3,sticky = 'E')

        #year
        year_options = self.get_year_options()
        year_var = StringVar(self)
        year_var.set(year_options[0])

        year_dropdown = apply(OptionMenu, (date_frame, year_var) + tuple(year_options))
        year_dropdown.grid(row=0, column=4, padx = 1, sticky="W")

        dateto_label = tk.Label(self, text="to").grid(row=7, column=1, pady = 0)

        ##end date stuff
        end_date_frame = tk.Frame(self)
        end_date_frame.grid(row=8, column=1, pady = 5, sticky="W", padx = 20)
        #month
        month_options = self.get_month_options()
        end_month_var = StringVar(self)
        end_month_var.set(month_options[0])

        end_month_dropdown = apply(OptionMenu, (end_date_frame, end_month_var) + tuple(month_options))
        end_month_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(end_date_frame, text="/").grid(row=0, column=1, sticky = 'E')

        #day
        day_options = self.get_day_options()
        end_day_var = StringVar(self)
        end_day_var.set(day_options[0])

        end_day_dropdown = apply(OptionMenu, (end_date_frame, end_day_var) + tuple(day_options))
        end_day_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        slash_label2 = tk.Label(end_date_frame, text ="/").grid(row=0, column=3,sticky = 'E')

        #year
        year_options = self.get_year_options()
        end_year_var = StringVar(self)
        end_year_var.set(year_options[0])

        end_year_dropdown = apply(OptionMenu, (end_date_frame, end_year_var) + tuple(year_options))
        end_year_dropdown.grid(row=0, column=4, padx = 1, sticky="W")



        zip_entry = tk.Entry(self)
        zip_entry.grid(row=4, column=1, pady = 5, padx= 20, sticky="W")

        flag_var = IntVar()
        flag_check = Checkbutton(self, variable=flag_var)
        flag_check.grid(row=5, column=1, pady = 5, sticky="W", padx = 20)

        ## loc option menu
        loc_options = self.get_loc_options()
        loc_var = StringVar(self)
        loc_var.set(loc_options[0])

        loc_dropdown = apply(OptionMenu, (self, loc_var) + tuple(loc_options))
        loc_dropdown.grid(row=1, column=1, padx = 20, pady = 10, sticky="W")

        ## city option menu
        city_options = self.get_city_options()
        city_var = StringVar(self)
        city_var.set(city_options[0])

        city_dropdown = apply(OptionMenu, (self, city_var) + tuple(city_options))
        city_dropdown.grid(row=3, column=1, padx = 20, pady = 10, sticky="W")

        ## state option menu
        state_options = self.get_state_options()
        state_var = StringVar(self)
        state_var.set(state_options[0])
        state_dropdown = apply(OptionMenu, (self, state_var) + tuple(state_options))
        state_dropdown.grid(row=2, column=1, padx = 20, pady = 10, sticky="W")





        ##table stuff
        table_frame = tk.Frame(self)
        table_frame.grid(row=10,column=0, columnspan=2, padx=0,pady=5)
        numrows, numcols = 0, 6

        var = tktable.ArrayVar(table_frame)
        for y in range(numrows):
            for x in range(numcols):
                index = "%i,%i" % (y, x)
                var[index] = index

        table = tktable.Table(table_frame, 
            rows = numrows,
            cols = numcols,
            state='normal',
            titlerows=1,
            titlecols=0,
            colwidth=10,
            height=10,
            roworigin=-1,
            colorigin=-1,
            selectmode='extended',
            selecttype='row',
            rowstretch='all',
            colstretch='last',
            # browsecmd=browsecmd,
            flashmode='on',
            variable=var,
            usecommand=0
        )
        scroll = Scrollbar(table_frame, orient='vertical', command=table.yview_scroll)
        table.config(yscrollcommand=scroll.set)
        scroll.pack(side='right', fill='y')
        table.pack(expand=1, fill='y')
        
        # table.grid(row=0, column=0)
        # scroll.grid(row=0, column=1)
        titles = ("Location Name", "City", "State", "Zip Code", "Flagged", "Date Flagged")
        r = table.index('end').split(',')[0]
        print r
        index = r + ",-1"
        table.set("row", "-1,-1", "Results")

        filters = []
        apply_button = tk.Button(self, text="Apply Filter", command=lambda :self.apply_filter(controller, table, filters))
        apply_button.grid(row=9, column=1, padx = 20, pady = 10, sticky="E")

        reset_button = tk.Button(self, text="Reset Filter", command=lambda :self.reset_filter(controller))
        reset_button.grid(row=9, column=0, padx = 20, pady = 10, sticky="W")

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=11, column=0, padx = 20, pady = 10, sticky="W")

    def apply_filter(self, controller, table, filters): #FIXME: probably need to pass an array with values to filter with
        titles = ("Location Name", "City", "State", "Zip Code", "Flagged", "Date Flagged")
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *titles)
        table.see(idx)
        filtered_poi = api.get_poi(filters)
        for r in filtered_poi:
            self.add_new_data(r, table)

    def add_new_data(self, row, table):
        #table.config(state='normal')
        table.insert_rows('end', 1)
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *row)
        table.see(idx)
        #table.config(state='disabled')


    def reset_filter(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(OffPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(OffPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(OffPortalPage)

    def get_loc_options(self):
        return api.get_poi_names()

    def get_state_options(self): 
        return api.get_states()

    def get_city_options(self): #FIXME: pass in state?
        return api.get_cities()

    def get_year_options(self):
        return api.get_years()

    def get_month_options(self):
        return api.get_months()

    def get_day_options(self):
        return api.get_days("1")




class AdminPortalPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Choose Functionality", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        pdp_button = tk.Button(self, text="Pending Data Points", command=lambda :self.pdp(controller)).grid(row=1, column=0, padx = 20, pady = 10)
        poffacc_button = tk.Button(self, text="Pending City Official Accounts", command=lambda :self.poffacc(controller)).grid(row=2, column=0, padx = 20, pady = 10)

        logout_button = tk.Button(self, text="Logout", command=lambda :self.logout(controller)).grid(row=3, column=0, padx = 20, pady = 10, sticky="W")


    def pdp(self, controller):
        controller.show_frame(PDPPage)

    def poffacc(self, controller):
        controller.show_frame(POPage)

    def logout(self, controller):
        api.logout()
        controller.show_frame(LoginPage)

class PDPPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Pending Data Points", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        # table goes here
                ##table stuff
        table_frame = tk.Frame(self)
        table_frame.grid(row=2,column=0, columnspan=2, padx=5,pady=5)
        numrows, numcols = 0, 6

        titles = ["Select", "Location", "Datatype", "Data Value", "Time&Date of data reading"]
        cell_frames = []
        # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        pending_data_points = api.get_pending_dp()

        for i in range(0,len(pending_data_points)):
            cell_frames.append(self.add_row(table_frame, i+1, pending_data_points[i], "white"))


        filters = []
        # apply_button = tk.Button(self, text="Show Report", command=lambda :self.apply_filter(controller, table, filters))
        # apply_button.grid(row=1, column=0, padx = 20, pady = 10, sticky="E")

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def add_row(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        # r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0, sticky=N+S+E+W)
        flag_var = IntVar()
        flag_check = Checkbutton(flag_frame, bg = bg_color, variable=flag_var)
        flag_check.grid(row=0, column=0, pady = 5, padx = 5, sticky=N+S+E+W)

        locn_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        locn_frame.grid(row=r, column=1, sticky=N+S+E+W)
        locn_label = tk.Label(locn_frame, bg = bg_color, text=row[0])
        locn_label.pack(side="top", fill="both", expand = True)

        dtype_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dtype_frame.grid(row=r, column=2, sticky=N+S+E+W)
        dtype_label = tk.Label(dtype_frame, bg = bg_color, text=row[1])
        dtype_label.grid(row=0, column=0, pady = 5, padx = 5)

        dval_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dval_frame.grid(row=r, column=3, sticky=N+S+E+W)
        dval_label = tk.Label(dval_frame, bg = bg_color, text=row[2])
        dval_label.grid(row=0, column=0, pady = 5, padx = 5)

        td_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        td_frame.grid(row=r, column=4, sticky=N+S+E+W)
        td_label = tk.Label(td_frame, bg = bg_color, text=row[3])
        td_label.grid(row=0, column=0, pady = 5, padx = 5)

        return (flag_var, locn_label, dtype_label, dval_label, td_label)


        # return row_ref
    def add_titles(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0)
        flag_label = tk.Label(flag_frame, bg = bg_color, text=row[0])
        flag_label.grid(row=0, column=0, pady = 5, padx = 5)

        locn_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        locn_frame.grid(row=r, column=1)
        locn_label = tk.Label(locn_frame, bg = bg_color, text=row[1])
        locn_label.grid(row=0, column=0, pady = 5, padx = 5)

        dtype_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dtype_frame.grid(row=r, column=2)
        dtype_label = tk.Label(dtype_frame, bg = bg_color, text=row[2])
        dtype_label.grid(row=0, column=0, pady = 5, padx = 5)

        dval_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dval_frame.grid(row=r, column=3)
        dval_label = tk.Label(dval_frame, bg = bg_color, text=row[3])
        dval_label.grid(row=0, column=0, pady = 5, padx = 5)

        td_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        td_frame.grid(row=r, column=4)
        td_label = tk.Label(td_frame, bg = bg_color, text=row[4])
        td_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)


    def back(self, controller):
        controller.show_frame(AdminPortalPage)
class POPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Pending City Officials", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        # table goes here
                ##table stuff
        table_frame = tk.Frame(self)
        table_frame.grid(row=2,column=0, columnspan=2, padx=5,pady=5)
        numrows, numcols = 0, 6

        titles = ["Select", "Username", "Email", "City", "State", "Title"]
        cell_frames = []
        # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        pending_data_points = api.get_pending_off()

        for i in range(0,len(pending_data_points)):
            cell_frames.append(self.add_row(table_frame, i+1, pending_data_points[i], "white"))



        # apply_button = tk.Button(self, text="Show Report", command=lambda :self.apply_filter(controller, table, filters))
        # apply_button.grid(row=1, column=0, padx = 20, pady = 10, sticky="E")

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)
        reject_button = tk.Button(self, text="Reject", command=lambda :self.reject_selected(controller))
        reject_button.grid(row=9, column=2, padx = 20, pady = 10, columnspan = 2)
        accept_button = tk.Button(self, text="Acept", command=lambda :self.accept_selected(cell_frames))
        accept_button.grid(row=9, column=2, padx = 20, pady = 10, columnspan = 2)

    def accept_selected(self, cell_frames):
        for f in cell_frames:
            if f[0].get() ==1:
                api.accept_official(f[1])
            
        return

    def reject_selected(self, cell_frames):
        for f in cell_frames:
            if f[0].get() ==1:
                api.reject_official(f[1])
            
        return

    def add_row(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        # r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0, sticky=N+S+E+W)
        flag_var = IntVar()
        flag_check = Checkbutton(flag_frame, bg = bg_color, variable=flag_var)
        flag_check.grid(row=0, column=0, pady = 5, padx = 5, sticky=N+S+E+W)

        uname_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        uname_frame.grid(row=r, column=1, sticky=N+S+E+W)
        uname_label = tk.Label(uname_frame, bg = bg_color, text=row[0])
        uname_label.pack(side="top", fill="both", expand = True)

        email_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        email_frame.grid(row=r, column=2, sticky=N+S+E+W)
        email_label = tk.Label(email_frame, bg = bg_color, text=row[1])
        email_label.grid(row=0, column=0, pady = 5, padx = 5)

        city_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        city_frame.grid(row=r, column=3, sticky=N+S+E+W)
        city_label = tk.Label(city_frame, bg = bg_color, text=row[2])
        city_label.grid(row=0, column=0, pady = 5, padx = 5)

        state_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        state_frame.grid(row=r, column=4, sticky=N+S+E+W)
        state_label = tk.Label(state_frame, bg = bg_color, text=row[3])
        state_label.grid(row=0, column=0, pady = 5, padx = 5)

        title_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        title_frame.grid(row=r, column=5, sticky=N+S+E+W)
        title_label = tk.Label(title_frame, bg = bg_color, text=row[4])
        title_label.grid(row=0, column=0, pady = 5, padx = 5)

        return (flag_var, row[0])


        # return row_ref
    def add_titles(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0)
        flag_label = tk.Label(flag_frame, bg = bg_color, text=row[0])
        flag_label.grid(row=0, column=0, pady = 5, padx = 5)

        uname_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        uname_frame.grid(row=r, column=1, sticky=N+S+E+W)
        uname_label = tk.Label(uname_frame, bg = bg_color, text=row[1])
        uname_label.pack(side="top", fill="both", expand = True)

        email_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        email_frame.grid(row=r, column=2, sticky=N+S+E+W)
        email_label = tk.Label(email_frame, bg = bg_color, text=row[2])
        email_label.grid(row=0, column=0, pady = 5, padx = 5)

        city_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        city_frame.grid(row=r, column=3, sticky=N+S+E+W)
        city_label = tk.Label(city_frame, bg = bg_color, text=row[3])
        city_label.grid(row=0, column=0, pady = 5, padx = 5)

        state_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        state_frame.grid(row=r, column=4, sticky=N+S+E+W)
        state_label = tk.Label(state_frame, bg = bg_color, text=row[4])
        state_label.grid(row=0, column=0, pady = 5, padx = 5)

        title_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        title_frame.grid(row=r, column=5, sticky=N+S+E+W)
        title_label = tk.Label(title_frame, bg = bg_color, text=row[5])
        title_label.grid(row=0, column=0, pady = 5, padx = 5)


    def back(self, controller):
        controller.show_frame(AdminPortalPage)



def main():
    app = TKMain()
    app.mainloop()


if __name__ == '__main__':
    main()