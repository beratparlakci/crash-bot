# gui.py

import customtkinter as ctk
from tkinter import messagebox
import config
from logger import init_logger
from symbol_loader import init_symbols
from bot_controller import start_bot, stop_bot


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


def create_gui():
    """Create GUI"""
    root = ctk.CTk()
    root.title("Crash Bot")
    root.geometry("700x850")
    
    
    main_frame = ctk.CTkFrame(root, corner_radius=0)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
   
    title_label = ctk.CTkLabel(main_frame, text="Crash Bot", 
                               font=ctk.CTkFont(size=24, weight="bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

   
    ctk.CTkLabel(main_frame, text="API Key", font=ctk.CTkFont(size=12)).grid(
        row=1, column=0, sticky='w', padx=10, pady=8)
    api_key_entry = ctk.CTkEntry(main_frame, width=300, show="*", 
                                  placeholder_text="Enter API Key",
                                  corner_radius=0)
    api_key_entry.grid(row=1, column=1, padx=10, pady=8)

    
    ctk.CTkLabel(main_frame, text="API Secret", font=ctk.CTkFont(size=12)).grid(
        row=2, column=0, sticky='w', padx=10, pady=8)
    api_secret_entry = ctk.CTkEntry(main_frame, width=300, show="*",
                                     placeholder_text="Enter API Secret",
                                     corner_radius=0)
    api_secret_entry.grid(row=2, column=1, padx=10, pady=8)

   
    ctk.CTkLabel(main_frame, text="Candle Count", font=ctk.CTkFont(size=12)).grid(
        row=3, column=0, sticky='w', padx=10, pady=8)
    candle_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="e.g.: 20",
                                corner_radius=0)
    candle_entry.insert(0, "20")
    candle_entry.grid(row=3, column=1, padx=10, pady=8)

    
    ctk.CTkLabel(main_frame, text="Interval", font=ctk.CTkFont(size=12)).grid(
        row=4, column=0, sticky='w', padx=10, pady=8)
    interval_var = ctk.StringVar(value="5m")
    interval_combo = ctk.CTkComboBox(main_frame, width=300, 
                                      values=list(config.BYBIT_INTERVALS.keys()),
                                      variable=interval_var, state="readonly",
                                      corner_radius=0,
                                      button_color="#747475",
                                      button_hover_color="#747475",
                                      dropdown_fg_color="#747475")
    interval_combo.grid(row=4, column=1, padx=10, pady=8)

  
    ctk.CTkLabel(main_frame, text="Trading pair", font=ctk.CTkFont(size=12)).grid(
        row=5, column=0, sticky='w', padx=10, pady=8)
    
    
    symbol_frame = ctk.CTkFrame(main_frame, fg_color="transparent", width=300)
    symbol_frame.grid(row=5, column=1, padx=10, pady=8)
    symbol_frame.grid_propagate(False) 
    
    symbol_var = ctk.StringVar()
    symbol_entry = ctk.CTkEntry(symbol_frame, width=300, 
                                 textvariable=symbol_var,
                                 placeholder_text="Search for pair (e.g.: BTC, ETH)",
                                 corner_radius=0)
    symbol_entry.pack(side="top")
    
    
    results_frame = ctk.CTkScrollableFrame(symbol_frame, width=280, height=150,
                                           corner_radius=0, 
                                           fg_color="#5a5a5a",
                                           scrollbar_button_color="#747475",
                                           scrollbar_button_hover_color="#747475")
    results_frame.pack_forget()
    
   
    result_buttons = []
    is_clicking_result = False 
    
    def update_symbol_results(event=None):
        """Update search results"""
        search_text = symbol_var.get().upper()
        
      
        for btn in result_buttons:
            btn.destroy()
        result_buttons.clear()
        
        if not search_text:
            results_frame.pack_forget()
            return
        
        
        matches = [s for s in config.ALL_SYMBOLS if search_text in s][:30]  
        
        if matches:
            results_frame.pack(side="top", pady=(2, 0))
            
            for symbol in matches:
                def select_symbol(s=symbol):
                    nonlocal is_clicking_result
                    is_clicking_result = True
                    symbol_var.set(s)
                    results_frame.pack_forget()
                    root.after(100, lambda: setattr(is_clicking_result, '__bool__', lambda: False))
                
                btn = ctk.CTkButton(results_frame, text=symbol, 
                                   command=select_symbol,
                                   width=270, height=30,
                                   corner_radius=0,
                                   fg_color="transparent",
                                   hover_color="#3b3b3b",
                                   anchor="w",
                                   font=ctk.CTkFont(size=11))
                btn.pack(pady=1, padx=2, fill="x")
                result_buttons.append(btn)
        else:
            results_frame.pack_forget()
    
    def on_entry_click(event):
        """Show results when the entry is clicked"""
        if symbol_var.get():
            update_symbol_results()
    
    def hide_results(event):
        """Hide when clicking outside the list"""
        root.after(150, lambda: results_frame.pack_forget())
    
    symbol_entry.bind("<KeyRelease>", update_symbol_results)
    symbol_entry.bind("<Button-1>", on_entry_click)
    symbol_entry.bind("<FocusOut>", hide_results)

    ctk.CTkLabel(main_frame, text="Category", font=ctk.CTkFont(size=12)).grid(
        row=6, column=0, sticky='w', padx=10, pady=8)
    category_var = ctk.StringVar(value="spot")
    category_combo = ctk.CTkComboBox(main_frame, width=300, 
                                      values=["spot"], variable=category_var,
                                      state="readonly",
                                      corner_radius=0,
                                      button_color="#747475",
                                      button_hover_color="#747475",
                                      dropdown_fg_color="#747475")
    category_combo.grid(row=6, column=1, padx=10, pady=8)

    
    ctk.CTkLabel(main_frame, text="Buy % (Drop)", font=ctk.CTkFont(size=12)).grid(
        row=7, column=0, sticky='w', padx=10, pady=8)
    buy_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="e.g.: 10",
                              corner_radius=0)
    buy_entry.insert(0, "10")
    buy_entry.grid(row=7, column=1, padx=10, pady=8)

   
    ctk.CTkLabel(main_frame, text="Sell % (Rise)", font=ctk.CTkFont(size=12)).grid(
        row=8, column=0, sticky='w', padx=10, pady=8)
    sell_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="e.g.: 10",
                               corner_radius=0)
    sell_entry.insert(0, "10")
    sell_entry.grid(row=8, column=1, padx=10, pady=8)

   
    ctk.CTkLabel(main_frame, text="Amount", font=ctk.CTkFont(size=12)).grid(
        row=9, column=0, sticky='w', padx=10, pady=8)
    qty_entry = ctk.CTkEntry(main_frame, width=300, placeholder_text="e.g.: 0.001",
                             corner_radius=0)
    qty_entry.insert(0, "0.001")
    qty_entry.grid(row=9, column=1, padx=10, pady=8)

   
    ctk.CTkLabel(main_frame, text="Amount Unit (Select quote to trade in USDT!)", font=ctk.CTkFont(size=12)).grid(
        row=10, column=0, sticky='w', padx=10, pady=8)
    marketUnit_var = ctk.StringVar(value="quoteCoin")
    marketUnit_combo = ctk.CTkComboBox(main_frame, width=300, 
                                      values=["baseCoin", "quoteCoin"],
                                      variable=marketUnit_var, state="readonly",
                                      corner_radius=0,
                                      button_color="#747475",
                                      button_hover_color="#747475",
                                      dropdown_fg_color="#747475")
    marketUnit_combo.grid(row=10, column=1, padx=10, pady=8)

   
    testnet_var = ctk.BooleanVar(value=True)
    testnet_check = ctk.CTkCheckBox(main_frame, text="Testnet Mode", 
                                     variable=testnet_var,
                                     font=ctk.CTkFont(size=13, weight="bold"),
                                     corner_radius=0)
    testnet_check.grid(row=11, column=0, columnspan=2, pady=15)

  
    start_btn = ctk.CTkButton(main_frame, text="Start Bot", 
                              command=lambda: start_bot(api_key_entry, api_secret_entry, testnet_var, 
                                                       symbol_var, interval_var, candle_entry, 
                                                       qty_entry, buy_entry, sell_entry, marketUnit_var),
                              width=300, height=40, 
                              font=ctk.CTkFont(size=14, weight="bold"),
                              fg_color="#4CAF50", hover_color="#45a049",
                              corner_radius=0)
    start_btn.grid(row=12, column=0, columnspan=2, pady=10)

  

    
    stop_btn = ctk.CTkButton(main_frame, text="Stop Bot", 
                             command=stop_bot,
                             width=200, height=40,
                             font=ctk.CTkFont(size=14, weight="bold"),
                             fg_color="#f44336", hover_color="#da190b",
                             corner_radius=0)
    stop_btn.grid(row=13, column=0, columnspan=2, pady=10)



      
    log_box = ctk.CTkTextbox(main_frame, width=600, height=100, 
                             fg_color="#1a1a1a", text_color="#00ff00",
                             font=ctk.CTkFont(family="Courier", size=11),
                             corner_radius=0)
    log_box.grid(row=14, column=0, columnspan=2, padx=10, pady=10)
    log_box.configure(state="disabled")

    
    init_logger(root, log_box)

    init_symbols(None)  

    return root