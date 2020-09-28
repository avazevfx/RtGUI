from tkinter import *
import tkinter.font as TkFont
import json
from tkinter import messagebox as mb
from tkinter import filedialog
from PIL import Image, ImageTk

# Window Properties
app = Tk()
app.title("Scene Editor")
try:
    app.iconbitmap("se_logo.ico")
except:
    mb.showerror("Startup Error", "Could not load Icon File")
    quit()
app.minsize(475, 0)
w, h = 900, 720
app.geometry("{0}x{1}+{2}+{3}".format(w, h, app.winfo_screenwidth()//2 - w//2, app.winfo_screenheight()//2 - h//2))

# Variables
FONT = TkFont.Font(family="Cascadia Code", size=10)
FONT_B = TkFont.Font(family="Cascadia Code", size=10, weight="bold")
FONT_L = TkFont.Font(family="Cascadia Code", size=12)
FONT_XL = TkFont.Font(family="Cascadia Code", size=14, weight="bold")

global objects
objects = {}
DEFAULTOBJ = {"posx": 0, "posy": 0, "posz": 0, "rad": 1, "mat": "default"}

global materials
materials = {}
DEFAULTMAT = {"difr": 100, "difg": 100, "difb": 100, "spcr": 255, "spcg": 255, "spcb": 255, "refl": 1, "rough": 1, "emsr": 0, "emsg": 0, "emsb": 0}

global last_obj
last_obj = None

global last_mat
last_mat = None

global objwidgets
objwidgets = {}

global matwidgets
matwidgets = {}

global pressedwidget

global filename
filename = False


class ObjWidget(Frame):
    def __init__(self, master, name, **kw):
        Frame.__init__(self, master=master, **kw)
        self.name = name
        self.bg = self["bg"]
        self.focuscol = self["highlightcolor"]
        self.delbtn = HButton(self, text=" X ", font=FONT_B, command=self.delete, border=0, bg="#dd3322", fg="#000000", activebackground="#8e1e14")
        self.delbtn.pack(side="right", fill=BOTH)
        self.lbl = Label(self, text=name, bg=self.bg, fg="#aaaaaa", font=FONT_L)
        self.lbl.pack(fill=BOTH)
        self.lbl.bind("<Button-1>", self.oncl)
        global objwidgets
        objwidgets[name] = self

    def oncl(self, event):
        onclick(self.name)

    def focus(self):
        print("Focusing " + str(self.name), self.bg, self.focuscol)
        self["bg"] = self.focuscol
        self.lbl["bg"] = self.focuscol

    def unfocus(self):
        self["bg"] = self.bg
        self.lbl["bg"] = self.bg

    def delete(self):
        global objects
        del objects[self.name]
        self.lbl.pack_forget()
        self.delbtn.pack_forget()
        self.pack_forget()
        update_widgets()


class HButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self["background"] = self["activebackground"]

    def on_leave(self, e):
        self["background"] = self.defaultBackground


def open_sc():
    global filename
    newfile = filedialog.askopenfilename(initialdir="C:/Users/%username%/Documents", title="Open Scene", filetypes=[
        ("Scene Files", "*.sc")])
    if newfile:
        path_lbl["text"] = newfile
        filename = newfile
        # TODO: Load json File and set parameters


def save_sc():
    global filename
    if not filename:
        savefile = filedialog.asksaveasfile(initialdir="C:/Users/%username%/Documents", title="Save Scene", filetypes=[
        ("Scene Files", "*.sc")])
        if savefile:
            path_lbl["text"] = savefile.name
            filename = savefile.name
    if filename:
        # TODO: Write json to file
        print("Writing File")
        pass


def clear_sc():
    global objects
    global materials
    res = mb.askyesno("Clear Scene?", "All unsaved Progress will be lost.", icon=mb.WARNING)
    if res == "yes":
        objects = {}
        materials = {}
        sname.delete(0, END)
        sname.insert(0, "--none--")


def cam_settings():
    cm = Toplevel()
    cm.title("Camera Settings")
    cm.iconbitmap("se_logo.ico")
    cm.configure(bg="#202020")
    Label(cm, text="width").pack()


def add_obj():
    global objects
    global last_obj
    store_obj()

    for i in range(0, 20):
        global last_obj
        new_name = "sphere" + str(i)
        if new_name in objects:
            pass
        else:
            objects[new_name] = DEFAULTOBJ
            last_obj = new_name
            load_obj(new_name)
            update_widgets()
            break
    print(objects)
    print("last_obj: " + last_obj)


def load_obj(objname):
    obj = objects[objname]
    sname.delete(0, END)
    posx.delete(0, END)
    posy.delete(0, END)
    posz.delete(0, END)
    rad.delete(0, END)
    mat.delete(0, END)
    sname.insert(0, objname)
    posx.insert(0, obj["posx"])
    posy.insert(0, obj["posy"])
    posz.insert(0, obj["posz"])
    rad.insert(0, obj["rad"])
    mat.insert(0, obj["mat"])


def store_obj():
    global objects
    global last_obj
    if sname.get() == "--none--":
        return

    objects[sname.get()] = {
        "posx": posx.get(),
        "posy": posy.get(),
        "posz": posz.get(),
        "rad": rad.get(),
        "mat": mat.get()
    }


    if last_obj is not None and last_obj != sname.get():
        del objects[last_obj]
        print("deleted")
        update_widgets()


def update_widgets():
    print("updatewidgets")
    global objects
    global objwidgets
    for wg in objwidgets:
        objwidgets[wg].lbl.pack_forget()
        objwidgets[wg].delbtn.pack_forget()
        objwidgets[wg].pack_forget()

    objwidgets = {}

    for obj in objects:
        objwidgets[obj] = ObjWidget(omc, obj, bg="#202020", width=50, height=20, highlightcolor="#00ff00")
        objwidgets[obj].pack(pady=3, padx=5, fill=BOTH)

    if len(objects) == 0:
        sname.delete(0, END)
        sname.insert(0, "--none--")


def add_mat():
    global materials
    global last_mat
    store_mat()

    for i in range(0, 20):
        global last_mat
        new_name = "mat" + str(i)
        if new_name in materials:
            pass
        else:
            materials[new_name] = DEFAULTMAT
            last_mat = new_name
            load_mat(new_name)
            break
    print(materials)
    print(last_mat)


def load_mat(matname):
    mat = materials[matname]
    mname.delete(0, END)
    difr.delete(0, END)
    difg.delete(0, END)
    difb.delete(0, END)
    spcr.delete(0, END)
    spcg.delete(0, END)
    spcb.delete(0, END)
    emsr.delete(0, END)
    emsg.delete(0, END)
    emsb.delete(0, END)
    rough.delete(0, END)
    refl.delete(0, END)
    mname.insert(0, matname)
    difr.insert(0, mat["difr"])
    difg.insert(0, mat["difg"])
    difb.insert(0, mat["difb"])
    spcr.insert(0, mat["spcr"])
    spcg.insert(0, mat["spcg"])
    spcb.insert(0, mat["spcb"])
    emsr.insert(0, mat["emsr"])
    emsg.insert(0, mat["emsg"])
    emsb.insert(0, mat["emsb"])
    rough.insert(0, mat["rough"])
    refl.insert(0, mat["refl"])


def store_mat():
    global materials
    global last_mat
    if mname.get() == "--none--":
        return
    try:
        materials[mname.get()] = {
            "difr": difr.get(),
            "difg": difg.get(),
            "difb": difb.get(),
            "spcr": spcr.get(),
            "spcg": spcg.get(),
            "spcb": spcb.get(),
            "emsr": emsr.get(),
            "emsg": emsg.get(),
            "emsb": emsb.get(),
            "rough": rough.get(),
            "refl": refl.get()
        }
        print(last_mat)
        if last_mat is not None and last_mat != mname.get():
            del materials[last_mat]
            print("deleted")
    except:
        mb.showerror("Error", "Could not store Material")


def onclick(name):
    # print("onclick")
    print("onclick " + name)
    global objwidgets
    global last_obj
    print("last: {0}, name: {1}".format(last_obj, name))

    for widgetname in objwidgets:
        print(widgetname, name)
        if widgetname == name:
            #print(name)
            #print(objwidgets[name])
            objwidgets[name].focus()
            print("Focusing " + name)
            store_obj()
            last_obj = name
            load_obj(name)
        else:
            print("Unfocusing " + name)
            objwidgets[name].unfocus()


def render():
    global objects
    print(objwidgets)
    print(sname.get())
    print(objects)
    print(app.winfo_width(), app.winfo_height())
    pass


# Options Bar Configuration
options = Frame(app, border=0, bg="#303030")
options.pack(expand=0, fill=X)

open_btn = HButton(options, border=0, font=FONT_B, text="Open", padx=5, pady=1, command=open_sc,
                   bg="#272727", fg="#dd3322", activebackground="#3c2020", activeforeground="#ff5544")
open_btn.pack(side=LEFT)

save_btn = HButton(options, border=0, font=FONT_B, text="Save", padx=5, pady=1, command=save_sc,
                   bg="#272727", fg="#dd3322", activebackground="#3c2020", activeforeground="#ff5544")
save_btn.pack(side=LEFT, padx=1)

clear_btn = HButton(options, border=0, font=FONT_B, text="Clear All", padx=5, pady=1, command=clear_sc,
                    bg="#272727", fg="#888888", activebackground="#3c2020", activeforeground="#dd3322")
clear_btn.pack(side=LEFT, padx=0)

render_btn = HButton(options, border=0, font=FONT_B, text="Render Scene", padx=10, pady=1, command=render,
                     bg="#272727", fg="#dd3322", activebackground="#3c2020", activeforeground="#ff5544")
render_btn.pack(side=RIGHT)

cam_btn = HButton(options, border=0, font=FONT_B, text="Camera", padx=10, pady=1, command=cam_settings,
                  bg="#272727", fg="#dd3322", activebackground="#3c2020", activeforeground="#ff5544")
cam_btn.pack(side=RIGHT, padx=1)

path_lbl = Label(options, text="New Scene", font=FONT, bg="#303030", fg="#aaaaaa")
path_lbl.pack()

# Main Window Configuration
window = Frame(app, bg="#202020")
window.pack(expand=1, fill=BOTH)

# Object Manager Configuration
om = Frame(window, bg="#252525")
om.pack(side=LEFT, expand=True, fill=BOTH)

om_lbl = Label(om, text="Objects", border=0, font=FONT_L, bg="#666666")
om_lbl.pack(side=TOP, fill=BOTH, padx=10, pady=10)

omc = Frame(om, bg="#303030")
omc.pack(fill=BOTH, expand=True, padx=10)
Frame(om, height=10, bg="#252525").pack()

Label(omc, text="Name", bg="#303030", fg="#dd3322", font=FONT_B, width=12).pack(padx=5, fill=BOTH)
sname = Entry(omc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0, justify=CENTER)
sname.pack(fill=BOTH, padx=5)

Label(omc, text="Position", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
pos = Frame(omc, bg="#303030")
pos.pack(fill=BOTH, padx=5)
posx = Entry(pos, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
posx.pack(fill=BOTH, side="left", expand=True)
posy = Entry(pos, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
posy.pack(fill=BOTH, side="left", padx=5, expand=True)
posz = Entry(pos, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
posz.pack(fill=BOTH, side="left", expand=True)

Label(omc, text="Radius", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
rad = Entry(omc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
rad.pack(fill=BOTH, padx=5)

Label(omc, text="Material", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
mat = Entry(omc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0, justify=CENTER)
mat.pack(fill=BOTH, padx=5)

add_obj_btn = HButton(omc, border=0, font=FONT_B, text=" + ", padx=5, height=0, pady=1, command=add_obj,
                  bg="#272727", fg="#dd3322", activebackground="#3c2020", activeforeground="#ff5544")
add_obj_btn.pack(pady=10)

sname.insert(0, "--none--")
posx.insert(0, "0")
posy.insert(0, "0")
posz.insert(0, "0")
rad.insert(0, "1")
mat.insert(0, "default")

# Material Manager Configuration
mm = Frame(window, bg="#252525")
mm.pack(side=RIGHT, expand=True, fill=BOTH)

mm_lbl = Label(mm, text="Materials", border=0, font=FONT_L, bg="#666666")
mm_lbl.pack(side=TOP, fill=BOTH, padx=10, pady=10)

mmc = Frame(mm, bg="#303030")
mmc.pack(fill=BOTH, expand=True, padx=10)
Frame(mm, height=10, bg="#252525").pack()

Label(mmc, text="Name", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
mname = Entry(mmc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0, justify=CENTER)
mname.pack(fill=BOTH, padx=5)

Label(mmc, text="Diffuse", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
dif = Frame(mmc, bg="#303030")
dif.pack(fill=BOTH, padx=5)
difr = Entry(dif, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
difr.pack(fill=BOTH, side="left", expand=True)
difg = Entry(dif, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
difg.pack(fill=BOTH, side="left", padx=5, expand=True)
difb = Entry(dif, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
difb.pack(fill=BOTH, side="left", expand=True)

Label(mmc, text="Specular", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
spc = Frame(mmc, bg="#303030")
spc.pack(fill=BOTH, padx=5)
spcr = Entry(spc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
spcr.pack(fill=BOTH, side="left", expand=True)
spcg = Entry(spc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
spcg.pack(fill=BOTH, side="left", padx=5, expand=True)
spcb = Entry(spc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
spcb.pack(fill=BOTH, side="left", expand=True)

Label(mmc, text="Reflectivity", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
refl = Entry(mmc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
refl.pack(fill=BOTH, padx=5)

Label(mmc, text="Roughness", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
rough = Entry(mmc, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
rough.pack(fill=BOTH, padx=5)

Label(mmc, text="Emissive", bg="#303030", fg="#dd3322", font=FONT_B, width=0).pack(padx=5, fill=BOTH)
ems = Frame(mmc, bg="#303030")
ems.pack(fill=BOTH, padx=5)
emsr = Entry(ems, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
emsr.pack(fill=BOTH, side="left", expand=True)
emsg = Entry(ems, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
emsg.pack(fill=BOTH, side="left", padx=5, expand=True)
emsb = Entry(ems, font=FONT_L, border=0, bg="#202020", fg="#aaaaaa", insertbackground="#dd3322", selectbackground="#dd3322", insertofftime=500, width=0)
emsb.pack(fill=BOTH, side="left", expand=True)

add_mat_btn = HButton(mmc, border=0, font=FONT_B, text=" + ", padx=5, height=0, pady=1, command=add_mat,
                  bg="#272727", fg="#dd3322", activebackground="#3c2020", activeforeground="#ff5544")
add_mat_btn.pack(pady=10)

mname.insert(0, "--none--")
difr.insert(0, "0")
difg.insert(0, "0")
difb.insert(0, "0")
spcr.insert(0, "0")
spcg.insert(0, "0")
spcb.insert(0, "0")
refl.insert(0, "1")
rough.insert(0, "1")
emsr.insert(0, "0")
emsg.insert(0, "0")
emsb.insert(0, "0")

app.mainloop()

# TODO: implement material creation methods (add, load, store)
# TODO: implement showobjwidgets & showmatwidgets function, clever way of wrapping elements
