import tkinter
import requests
import threading
from time import sleep

name = None
balance = None
user_id = None
password = None
thread = None
base_url = 'https://km-blockchain.herokuapp.com/'
event = threading.Event()


def req(req_name, **kwargs):
    r = requests.get(base_url+req_name, params=kwargs)
    if r.status_code != 200:
        return None
    return r.json()


def register(name, password):
    return req('register', name=name, password=password)


def login(name, password):
    return req('login', name=name, password=password)


def user(user_id):
    return req('user', user_id=user_id)


def trans(trans_id):
    return req('trans', trans_id=trans_id)


def trans_from(user_id):
    return req('trans_from', user_id=user_id)


def trans_to(user_id):
    return req('trans_to', user_id=user_id)


def trans_add(from_id, to_id, amount, password):
    return req('trans_add', from_id=from_id, to_id=to_id, amount=amount, password=password)


def verify_block(user_id, password, block_id):
    return req('verify_block', user_id=user_id, password=password, block_id=block_id)


def block_get(block_id):
    return req('block_get', block_id=block_id)


def verify_get(user_id):
    return req('verify_get', user_id=user_id)


def loop(label, user_id, password):
    while True:
        sleep(1)
        if event.is_set():
            return
        r = user(user_id)
        if r:
            label['text'] = f"Your balance: {r['balance']}"
        r = verify_get(user_id)
        if r:
            verify_block(user_id, password, r['id'])


def start_thread(label, user_id, password):
    global thread, event
    event.clear()
    thread = threading.Thread(target=loop, args=(label, user_id, password))
    thread.start()


class Entry:
    def __init__(self, root):
        self.master = root
        self.master.title("Welcome!")
        self.master.geometry('400x200')
        self.b1 = tkinter.Button(text="Log in", width='35', height='2', command=self.log_in, font=('Arial', 9))
        self.b1.place(relx='.2', rely='.2')
        self.b1.configure(background='#00C89C', foreground="#000")
        self.b2 = tkinter.Button(text="Sign up", width='35', height='2', font=('Arial', 9), command=self.sign_up)
        self.b2.place(relx='.2', rely='.5')
        self.b2.configure(background='#FF353F', foreground="#FFF")
        root["bg"] = "#0B001E"
        self.reg = None
        self.login = None

    def log_in(self):
        self.login = Login(self.master)
        master.withdraw()

    def sign_up(self):
        master.withdraw()
        self.reg = Reg(self.master)


class Login:
    def __init__(self, root):
        self.root = root
        self.top = tkinter.Toplevel(root)
        self.main_ = None
        self.top.title("Log in")
        self.top.geometry('250x150')
        self.name = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.top.title1 = tkinter.Label(self.top, text="Log in", font=('Arial', 11), bg='#0B001E', fg="#FFF")
        self.top.title1.place(relx='.40', rely='.07')
        self.top.name_label = tkinter.Label(self.top, text="Login:", bg='#0B001E', fg="#FFF")
        self.top.name_label.place(relx='.1', rely='.30')
        self.top.surname_label = tkinter.Label(self.top, text="Password:", bg='#0B001E', fg="#FFF")
        self.top.surname_label.place(relx='.1', rely='.55')

        self.top.name_entry = tkinter.Entry(self.top, textvariable=self.name)
        self.top.name_entry.place(width='143', height='20', relx='.25', rely='.30')
        self.top.name_entry.config(background="#7E4B74", foreground="#FFF", borderwidth="0")
        self.top.password_entry = tkinter.Entry(self.top, textvariable=self.password)
        self.top.password_entry.place(width='123', height='20', relx='.33', rely='.55')
        self.top.password_entry.config(background="#7E4B74", foreground="#FFF", borderwidth="0")
        self.top.message_button = tkinter.Button(self.top, text="Log in", font=('Arial', 12), command=self.main)
        self.top.message_button.configure(background='#35CEC2')
        self.top.message_button.place(relx='.2', rely='.800', width='160', height='24')
        self.top.configure(background="#0B001E")
        self.top.protocol('WM_DELETE_WINDOW', self.exit)

    def main(self):
        global name, user_id, password, balance
        r = login(self.name.get(), self.password.get())
        if r:
            name = self.name.get()
            user_id = r['id']
            password = self.password.get()
            balance = r['balance']
            self.main_ = Main(self.root)
            start_thread(self.main_.top.txt2, user_id, password)
            self.top.destroy()
        else:
            self.top.name_entry.delete(0, 'end')
            self.top.password_entry.delete(0, 'end')
            self.top.title('Log in FAILED')
            self.top.title1['text'] = 'Log in FAILED'
            self.top.title1.place(relx='.30', rely='.07')

    def exit(self):
        master.deiconify()
        self.top.destroy()


class Main:
    def __init__(self, root):
        self.root = root
        self.top = tkinter.Toplevel(root)
        self.login = None
        self.trans = None
        self.top.title("Main")
        self.top.geometry("500x200")
        self.top.configure(background="#0B001E")
        self.top.txt1 = tkinter.Label(self.top, fg="#FFF", bg="#0B001E", text=f"Welcome, {name} (id {user_id})!",
                                      font=('Arial', 15))
        self.top.txt1.place(rely='.0', width="500", height="40")
        self.top.b1 = tkinter.Button(self.top, text="Fulfill the transaction", font=('Arial', 15), command=self.tran)
        self.top.b1.place(width="450", rely=".2", relx=".05", height="45")
        self.top.b1.configure(background='#35CEC2', foreground='#000')
        self.top.txt2 = tkinter.Label(self.top, fg="#FFF", bg="#4B2243", text=f"Your balance: {balance}",
                                      font=('Arial', 15), borderwidth=2, relief="solid", highlightbackground="white")
        self.top.txt2.place(rely='.45', relx='.05', width="450", height="40")
        self.top.b2 = tkinter.Button(self.top, text="Exit", font=('Arial', 15), command=self.exit)
        self.top.b2.place(width="300", rely=".67", relx=".18", height="30")
        self.top.b2.configure(background='#FF353F', foreground="#FFF")
        self.top.protocol('WM_DELETE_WINDOW', self.exit)

    def exit(self):
        event.set()
        self.root.deiconify()
        self.top.destroy()

    def tran(self):
        self.top.withdraw()
        self.trans = Trans(self.top)


class Reg:
    def __init__(self, root):
        self.root = root
        self.top = tkinter.Toplevel(root)
        self.main_ = None
        self.top.title("Registration")
        self.top.geometry('300x150+500+200')
        self.top.button = tkinter.Button(self.top, text='Registration', command=self.main)
        self.top.button.pack(side=tkinter.BOTTOM)
        self.top.button.configure(background="#35CEC2")
        self.login = tkinter.StringVar()
        self.password = tkinter.StringVar()
        self.repeat = tkinter.StringVar()
        self.top.txt = tkinter.Entry(self.top, textvariable=self.login)
        self.top.txt.place(relx=.3, rely=.1, height="20")
        self.top.txt2 = tkinter.Entry(self.top, textvariable=self.password)
        self.top.txt2.place(relx=.3, rely=.3, height="20")
        self.top.txt3 = tkinter.Entry(self.top, textvariable=self.repeat)
        self.top.txt3.place(relx=.5, rely=.5, height="20")
        self.top.lbl = tkinter.Label(self.top, text="Login:", bg='#0B001E', fg="#FFF")
        self.top.lbl2 = tkinter.Label(self.top, text="Password:", bg='#0B001E', fg="#FFF")
        self.top.lbl3 = tkinter.Label(self.top, text="Repeat password:", bg='#0B001E', fg="#FFF")
        self.top.lbl.place(relx=.1, rely=.1)
        self.top.lbl2.place(relx=.1, rely=.3)
        self.top.lbl3.place(relx=.1, rely=.5)
        self.top.configure(background="#0B001E")
        self.top.protocol('WM_DELETE_WINDOW', self.exit)

    def restart(self):
        self.top.txt.delete(0, 'end')
        self.top.txt2.delete(0, 'end')
        self.top.txt3.delete(0, 'end')
        self.top.title("Registration FAILED")

    def main(self):
        global name, user_id, password, balance, thread
        if self.password.get() != self.repeat.get():
            return self.restart()
        r = register(self.login.get(), self.password.get())
        if r is None:
            return self.restart()
        name = self.login.get()
        user_id = r['id']
        password = self.password.get()
        balance = r['balance']
        self.main_ = Main(self.root)
        thread = start_thread(self.main_.top.txt2, user_id, password)
        self.top.destroy()

    def exit(self):
        master.deiconify()
        self.top.destroy()


class Trans:
    def __init__(self, root):
        self.root = root
        self.top = tkinter.Toplevel(root)
        self.main_ = None
        self.top.title("Transaction")
        self.top.geometry('250x150')

        self.user_id = tkinter.StringVar()
        self.amount = tkinter.StringVar()
        self.top.title1 = tkinter.Label(self.top, text="Transfer", font=('Arial', 15), bg='#0B001E', fg="#FFF")
        self.top.title1.place(relx='.35', rely='.07')
        self.top.name_label = tkinter.Label(self.top, text="Recipiet Cash ID:", bg='#0B001E', fg="#FFF")
        self.top.name_label.place(relx='.1', rely='.30')
        self.top.surname_label = tkinter.Label(self.top, text="Currency:", bg='#0B001E', fg="#FFF")
        self.top.surname_label.place(relx='.1', rely='.55')

        self.top.name_entry = tkinter.Entry(self.top, textvariable=self.user_id)
        self.top.name_entry.place(width='100', height='20', relx='.47', rely='.30')
        self.top.name_entry.config(background="#7E4B74", foreground="#FFF", borderwidth="0")
        self.top.surname_entry = tkinter.Entry(self.top, textvariable=self.amount)
        self.top.surname_entry.place(width='137', height='20', relx='.32', rely='.55')
        self.top.surname_entry.config(background="#7E4B74", foreground="#FFF", borderwidth="0")

        self.top.message_button = tkinter.Button(self.top, text="Send", font=('Arial', 10), command=self.main)

        self.top.message_button.configure(background='#00C89C')
        self.top.message_button.place(relx='.2', rely='.800', width='160', height='20')

        self.top.configure(background="#0B001E")
        self.top.protocol('WM_DELETE_WINDOW', self.exit)

    def restart(self):
        self.top.name_entry.delete(0, 'end')
        self.top.surname_entry.delete(0, 'end')
        self.top.title("Transaction FAILED")
        self.top.title1['text'] = "Transfer FAILED"

    def main(self):
        r = trans_add(user_id, self.user_id.get(), self.amount.get(), password)
        if r is None:
            return self.restart()
        self.exit()

    def exit(self):
        self.root.deiconify()
        self.top.destroy()


if __name__ == '__main__':
    master = tkinter.Tk()
    Entry(master)
    master.mainloop()
