# logger.py

log_box = None
root = None


def init_logger(tkinter_root, text_widget):
    global root, log_box
    root = tkinter_root
    log_box = text_widget


def log(msg):
    if root:
        root.after(0, _log, msg)
    else:
        print(msg)  


def _log(msg):
    if log_box:
        log_box.configure(state="normal")
        log_box.insert("end", msg + "\n")
        log_box.see("end")
        log_box.configure(state="disabled")
