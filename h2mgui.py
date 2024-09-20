import h2mfunctions as h2m
import json
from tkinter import *
from tkinter import ttk
import customtkinter as ctk
import pyperclip  
import random
import pkg_resources

class gui(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --------------------------------- Window -------------------------------
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")

        self.title("H2M-Tool")
        self.iconbitmap(pkg_resources.resource_filename(__name__, 'icon.ico'))
        self.minsize(900, 560)

        # Initialize filter variables
        self.filter_category = 'Show All'
        self.filter_regions = set()
        self.search_query = ""

        # -------------------------------- Functions -----------------------------

        def notify(notification):
            self.notifier.configure(text=notification)
            self.update_idletasks()
            self.after(2000, lambda: self.notifier.configure(text=""))

        def read_server_data():
            try:
                with open(h2m.output_file, 'r') as file:
                    return json.load(file)
            except FileNotFoundError:
                notify("Servers.json not found, try refreshing")
                return []  

        def update_treeview(server_data):
            tv.delete(*tv.get_children())
            for server in server_data:
                tv.insert("", "end", values=(
                    server.get('region', ''), 
                    server.get('name', ''), 
                    server.get('gamemode', ''), 
                    server.get('map', ''), 
                    server.get('category', ''), 
                    f"{server.get('players', '')}/{server.get('maxplayers', '')}"
                ), tags=(server.get('ip', ''),))
            for col in tv.cget('columns'):
                tv.heading(col, command=lambda _col=col: sort_treeview(tv, _col, False))
                
        def update_with_filters():
            server_data = read_server_data()
            filtered_data = apply_filters(server_data)
            update_treeview(filtered_data)

        def apply_filters(server_data):
            if self.filter_category == 'Favorites':
                try:
                    with open(h2m.favorites_file, 'r') as f:
                        favorites = json.load(f)
                    favorite_ips = set(favorites)
                except (FileNotFoundError, json.JSONDecodeError):
                    favorite_ips = set()
                filtered_data = [
                    server for server in server_data
                    if server.get('ip') in favorite_ips
                ]
            else:
                filtered_data = [
                    server for server in server_data
                    if (self.filter_category == 'Show All' or server.get('category') == self.filter_category) and
                       (not self.filter_regions or server.get('region') in self.filter_regions) and
                       (not self.search_query or self.search_query in server.get('name', '').lower())
                ]
            return filtered_data

        def refresh():
            h2m.fetch_servers()
            update_with_filters
            notify('Servers refreshed')

        def filter_category(category_name=None):
            self.filter_category = category_name
            update_with_filters()

        def filter_region():
            self.filter_regions = set()
            region_vars = {
                "NA": region_na.get(),
                "EU": region_eu.get(),
                "OCE": region_oce.get(),
                "LATAM": region_latam.get(),
                "SEA": region_sea.get(),
                "": region_unknown.get()
            }
            self.filter_regions.update(region for region, value in region_vars.items() if value == 1)
            update_with_filters()

        def search_servers(event=None):
            self.search_query = search_name.get().lower()
            update_with_filters()

        def sort_treeview(tv, col, reverse):
            if col == "Players":
                l = [(int(tv.set(k, col).split('/')[0]), k) for k in tv.get_children('')]
            else:
                l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(key=lambda t: t[0], reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda _col=col: sort_treeview(tv, _col, not reverse))

        def on_item_leftclick(event):
            item = tv.selection()
            if item:
                ip = tv.item(item[0], 'tags')
                if ip:
                    selected_ip = ip[0]
                    pyperclip.copy(f"/connect {selected_ip}")
                    notify(f'"/connect {selected_ip}" copied to clipboard')
                    
        def add_to_favorites(ip):
            try:
                with open(h2m.favorites_file, 'r') as f:
                    favorites = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                favorites = []
            
            if ip not in favorites:
                favorites.append(ip)
                with open(h2m.favorites_file, 'w') as f:
                    json.dump(favorites, f)
                notify(f'{ip} added to favorites')
            else:
                notify(f'{ip} is already in favorites')

        def remove_from_favorites(ip):
            try:
                with open(h2m.favorites_file, 'r') as f:
                    favorites = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                favorites = []
                
            if ip in favorites:
                favorites.remove(ip)
                with open(h2m.favorites_file, 'w') as f:
                    json.dump(favorites, f)
                update_with_filters()
                notify(f'{ip} removed from favorites')
            else:
                notify(f'{ip} is not in favorites')

        def create_context_menu(ip):
            context_menu = Menu(self, tearoff=0, background="#2e2e2e", foreground="#ffffff", activebackground="#01B366", activeforeground="#ffffff")
            try:
                with open(h2m.favorites_file, 'r') as f:
                    favorites = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                favorites = []

            if ip in favorites:
                context_menu.add_command(label="Remove from Favorites", command=lambda: remove_from_favorites(ip))
            else:
                context_menu.add_command(label="Add to Favorites", command=lambda: add_to_favorites(ip))
            
            return context_menu

        def show_context_menu(event):
            item = tv.identify_row(event.y)
            tv.selection_set(item)
            ip = tv.item(item, 'tags')
            if ip:
                selected_ip = ip[0]
                context_menu = create_context_menu(selected_ip)
                context_menu.post(event.x_root, event.y_root)

        def matchmaking():
            items = tv.get_children()
            available_servers = [
                tv.item(item, 'tags')[0] for item in items
                if int(tv.item(item, 'values')[5].split('/')[0]) < int(tv.item(item, 'values')[5].split('/')[1])
            ]
            if available_servers:
                selected_ip = random.choice(available_servers)
                pyperclip.copy(f"/connect {selected_ip}")
                notify(f'"/connect {selected_ip}" copied to clipboard')
            else:
                notify("No servers available for matchmaking")

        # -------------------------------- Elements ------------------------------
        # Tabviewer (tabs)
        self.tabview = ctk.CTkTabview(self, anchor='w')
        self.tabview.pack(fill='both', expand=True)

        # Server Browser Tab
        self.tab_main = self.tabview.add("Server Browser")

        # First Row Frame
        frame_row1 = ctk.CTkFrame(self.tab_main)
        frame_row1.pack(fill='x')

        # Checkboxes Frame
        frame_region = ctk.CTkFrame(frame_row1)
        frame_region.pack(side='left', padx=5, pady=5)

        # Region Filter
        region_na = IntVar()
        region_eu = IntVar()
        region_oce = IntVar()
        region_latam = IntVar()
        region_sea = IntVar()
        region_unknown = IntVar()
        
        check_NA = ctk.CTkCheckBox(frame_region, text="NA  ",
            variable=region_na, onvalue=1, offvalue=0, width=5, checkbox_height=22, checkbox_width=22,
            command=filter_region
        )
        check_NA.pack(side='left', padx=3, pady=2)

        check_EU = ctk.CTkCheckBox(frame_region, text="EU  ",
            variable=region_eu, onvalue=1, offvalue=0, width=5, checkbox_height=22, checkbox_width=22,
            command=filter_region
        )
        check_EU.pack(side='left', padx=3, pady=2)

        check_OCE = ctk.CTkCheckBox(frame_region, text="OCE",
            variable=region_oce, onvalue=1, offvalue=0, width=5, checkbox_height=20, checkbox_width=20,
            command=filter_region
        )
        check_OCE.pack(side='left', padx=3, pady=2)

        check_LATAM = ctk.CTkCheckBox(frame_region, text="LAT",
            variable=region_latam, onvalue=1, offvalue=0, width=5, checkbox_height=20, checkbox_width=20,
            command=filter_region
        )
        check_LATAM.pack(side='left', padx=3, pady=2)

        check_SEA = ctk.CTkCheckBox(frame_region, text="SEA",
            variable=region_sea, onvalue=1, offvalue=0, width=6, checkbox_height=20, checkbox_width=20,
            command=filter_region
        )
        check_SEA.pack(side='left', padx=3, pady=2)
        
        check_unknown = ctk.CTkCheckBox(frame_region, text="___ ",
            variable=region_unknown, onvalue=1, offvalue=0, width=6, checkbox_height=20, checkbox_width=20,
            command=filter_region
        )
        check_unknown.pack(side='left', padx=3, pady=2)
        
        # Row1 Buffer
        frame_buffer1 = ctk.CTkFrame(frame_row1, height=1, width=1)
        frame_buffer1.pack(side='left', padx=1, pady=1, expand=True)

        # Refresh Button 
        frame_refresh = ctk.CTkFrame(frame_row1)
        frame_refresh.pack(side='right', padx=5, pady=2)

        button_refresh = ctk.CTkButton(frame_refresh, text="Refresh", command=refresh)
        button_refresh.pack()

        # Second Row Frame
        frame_row2 = ctk.CTkFrame(self.tab_main)
        frame_row2.pack(fill='x')
        
        # Matchmaking Button
        button_matchmaking = ctk.CTkButton(frame_row2, text="Matchmaking", command=matchmaking)
        button_matchmaking.pack(side='right', padx=5, pady=2)
        
        # Category Selector Frame
        frame_category = ctk.CTkFrame(frame_row2)
        frame_category.pack(side='left', padx=5, pady=5)

        button_category = ctk.CTkSegmentedButton(
            frame_category,
            values=['Show All', 'Favorites', 'Regular', 'Trickshotting', 'Sniping', 'Double XP', 'Custom'],
            command=filter_category
        )
        button_category.pack()
        
        # Search Bar 
        frame_search_bar = ctk.CTkFrame(self.tab_main)
        frame_search_bar.pack(fill='x', pady=(0, 3))
        search_name = ctk.CTkEntry(frame_search_bar, placeholder_text="Search by name")
        search_name.pack(side='left', padx=5, pady=5, fill='x', expand=True)
        search_name.bind("<KeyRelease>", search_servers)

        # Server Browser Frame
        frame_browser = ctk.CTkFrame(self.tab_main)
        frame_browser.pack(fill='both', expand=True, padx=5, pady=5)
        
        global tv
        tv = ttk.Treeview(frame_browser, columns=(
            "Region", 
            "Server Name", 
            "Game Mode", 
            "Map",  
            "Category",
            "Players"
            ), show='headings')

        tv.heading("Region", text=" ", anchor='w')
        tv.heading("Server Name", text="Server Name", anchor='w')
        tv.heading("Game Mode", text="Game Mode", anchor='w')
        tv.heading("Map", text="Map", anchor='w')
        tv.heading("Category", text="Category", anchor='w')
        tv.heading("Players", text="Players", anchor='w')

        tv.column("Region", anchor='w', width=40, stretch=False)
        tv.column("Server Name", anchor='w', stretch=True)
        tv.column("Game Mode", anchor='w', width=100, stretch=False)
        tv.column("Map", anchor='w', width=100, stretch=False)
        tv.column("Category", anchor='w', width=100, stretch=False)
        tv.column("Players", anchor='w', width=50, stretch=False)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2e2e2e",
                        foreground="#ffffff",
                        fieldbackground="#2e2e2e",
                        borderwidth=0)

        style.configure("Treeview.Heading",
                        background="#444444",
                        foreground="#ffffff",
                        relief="flat",
                        borderwidth=0)

        style.map("Treeview",
                  background=[('selected', '#01B366')],
                  foreground=[('selected', '#ffffff')])

        scrollbar_y = ctk.CTkScrollbar(frame_browser, orientation='vertical', command=tv.yview)
        tv.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side='right', fill='y')
        tv.pack(side='left', fill='both', expand=True)

        tv.bind("<ButtonRelease-1>", on_item_leftclick)
        tv.bind("<Button-3>", show_context_menu)

        # Initial Load
        update_treeview(read_server_data())

        # Plugins Tab
        self.tab_plugins = self.tabview.add("Plugins")
        label_plugins = ctk.CTkLabel(self.tab_plugins, text="Plugin loader coming soon(ish)")
        label_plugins.pack(padx=10, pady=10)

        # About Tab
        self.tab_about = self.tabview.add("About")
        label_about_heading = ctk.CTkLabel(self.tab_about, font=('systemui', 18, UNDERLINE), text="What Everything Does")
        label_about_heading.pack(padx=10, pady=10, fill='x')
        
        frame_about = ctk.CTkFrame(self.tab_about)
        frame_about.pack(fill='both')
        label_about = ctk.CTkLabel(
            frame_about, 
            justify='left',
            font=('systemui', 18),
            text= "Clicking on a server copies its IP to your clipboard\n> Click server you want\n> Open your game's console (~)\n> Press Ctrl-V\n> Press ENTER\n> You are now in a server\n\n"
            + "Right Click a server to save it to your favorites\n> Right Click it again to remove it from your favorites\n\n"
            + "Refresh: re-feteches the server list\n> Do this to update player counts\n> Spam this at your own risk of getting rate limited\n\n"
            + "Matchmaking: selects a random server based on your applied filters that has an open player slot \n> Ctrl-V into your console, same as normal\n"
            )
        label_about.pack(padx=10, pady=5)
        
        frame_about2 = ctk.CTkFrame(self.tab_about)
        frame_about2.pack(fill='x')
        label_about2 = ctk.CTkLabel(
            frame_about2, 
            font=('systemui', 11),
            text= "if something bugs out yell at me on twitter @zomm\n(unless it's a virustotal screenshot)")
        label_about2.pack(anchor='s')

        # Notifier
        frame_bottom = ctk.CTkFrame(self)
        frame_bottom.pack(fill='x')
        self.notifier = ctk.CTkLabel(frame_bottom, text=f"", text_color="white")
        self.notifier.pack(side='left', fill='x', padx=14)
        
        self.version = ctk.CTkLabel(frame_bottom, text=f"{h2m.version_tag}", text_color="white")
        self.version.pack(side='right', fill='x', padx=14)

if __name__ == "__main__":
    server_browser = gui()
    server_browser.mainloop()
