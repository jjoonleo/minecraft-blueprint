import tkinter as tk
import copy
import PIL
import os
from blueprint import *
from cursor import *
from block import *
from PIL import Image, ImageTk, ImageEnhance

photos = {}


def update(data):
    # Clear the listbox
    my_list.delete(0, tk.END)

    # Add toppings to listbox
    for item in data:
        my_list.insert(tk.END, item)

# Update entry box with listbox clicked


def fillout(e):
    # Delete whatever is in the entry box
    my_entry.delete(0, tk.END)

    # Add clicked list item to entry box
    my_entry.insert(0, my_list.get(tk.ANCHOR))

# Create function to check entry vs listbox


def check(e):
    # grab what was typed
    typed = my_entry.get()

    if typed == '':
        data = blockList
    else:
        data = []
        for item in blockList:
            if typed.lower() in item.lower():
                data.append(item)

    # update our listbox with selected items
    update(data)


def render(blueprint):
    for i in range(blueprintSize):
        for j in range(blueprintSize):

            if blueprint[cursor.layer][i][j].name:
                canvas.create_image(startCorX+size*i+size //
                                    2, startCorY+size*j+size//2, image=getPhoto(blueprint[cursor.layer][i][j].name, 1))
                # canvas.create_rectangle(startCorX+size*curRecX, startCorY+size*curRecY,startCorX+size*(curRecX+1), startCorY+size*(curRecY+1), fill="red") #color[blueprint.blueprint[cursor.layer][curRecX][curRecY].name]
                canvas.create_text(startCorX+size*i, startCorY +
                                   size*j, text=blueprint[cursor.layer][i][j].number, anchor="nw")
            else:
                canvas.create_rectangle(startCorX+size*i, startCorY+size*j,
                                        startCorX+size*(i+1), startCorY+size*(j+1), fill="bisque")  # color[blueprint[cursor.layer][i][j].name]
                if cursor.layer > 0 and blueprint[cursor.layer-1][i][j].name:
                    canvas.create_image(startCorX+size*i+size //
                                    2, startCorY+size*j+size//2, image=getPhoto(blueprint[cursor.layer-1][i][j].name, 0.5))


def onNumberButtonClicked():
    cursor.block.number = int(numberOfBlock.get())


def onNameButtonClicked():
    cursor.block.name = nameOfBlock.get()


def onlayerButtonClicked():
    cursor.layer = int(layer.get())
    render(blueprint.blueprint)

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    assert opacity >= 0 and opacity <= 1
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = PIL.ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im    


def getPhoto(name,opacity):
    photo = photos.get(name+str(opacity))
    if photo == None:
        image = PIL.Image.open("blocks/"+name+".png")
        image = image.resize((size, size), PIL.Image.Resampling.LANCZOS)
        image = reduce_opacity(image,opacity)
        photo = PIL.ImageTk.PhotoImage(image)
        photos[cursor.block.name+str(opacity)] = photo
    return photo


def stackBlock(x, y):
    curRecX = (x - startCorX)//size
    curRecY = (y - startCorY)//size
    if 0 <= curRecX < blueprintSize and 0 <= curRecY < blueprintSize:
        if cursor.clickState == 1:
            
            canvas.create_rectangle(startCorX+size*curRecX, startCorY+size*curRecY,
                                    startCorX+size*(curRecX+1), startCorY+size*(curRecY+1), fill="bisque")
            blueprint.blueprint[cursor.layer][curRecX][curRecY] = copy.deepcopy(cursor.block)
            canvas.create_image(startCorX+size*curRecX+size //2, startCorY+size*curRecY+size//2, image=getPhoto(cursor.block.name,1))
            # canvas.create_rectangle(startCorX+size*curRecX, startCorY+size*curRecY,startCorX+size*(curRecX+1), startCorY+size*(curRecY+1), fill="red") #color[blueprint.blueprint[cursor.layer][curRecX][curRecY].name]
            canvas.create_text(startCorX+size*curRecX, startCorY +
                               size*curRecY, text=cursor.block.number, anchor="nw")
        elif cursor.clickState == -1:
            blueprint.blueprint[cursor.layer][curRecX][curRecY] = Block("", 0)
            canvas.create_rectangle(startCorX+size*curRecX, startCorY+size*curRecY,
                                    startCorX+size*(curRecX+1), startCorY+size*(curRecY+1), fill="bisque")
            if cursor.layer > 0 and blueprint.blueprint[cursor.layer-1][curRecX][curRecY].name:
                canvas.create_image(startCorX+size*curRecX+size //2, startCorY+size*curRecY+size//2, image=getPhoto(blueprint.blueprint[cursor.layer-1][curRecX][curRecY].name,0.5))
            canvas.create_text(startCorX+size*curRecX, startCorY +
                               size*curRecY, text="", anchor="nw")


def onPress(event):
    cursor.clickState = True
    stackBlock(event.x, event.y)
    pass


def onRelease(event):
    cursor.clickState = 0
    pass


def onRightPress(event):
    cursor.clickState = -1
    stackBlock(event.x, event.y)
    pass


def onRightRelease(event):
    cursor.clickState = 0
    pass


def moved(event):
    stackBlock(event.x, event.y)


blockList = os.listdir("./blocks")
for i in range(len(blockList)):
    blockList[i] = blockList[i].replace(".png", "")


cursor = Cursor()
startCorX = 20
startCorY = 20
size = 50
blueprintSize = 17
address = input("함수 파일을 저장할 경로를 파일이름을 포함한 절대경로로 입력하세요.\n함수파일의 확장자는 .mcfunction이어야 합니다.\n입력값이 올바르지 않을 시 오류가 발생할 수 있습니다.\n")
blueprint = Blueprint(Block("", 0), blueprintSize,address)

root = tk.Tk()
root.geometry("1500x1000")

canvas = tk.Canvas(root, background="bisque", width=size *
                   blueprintSize+50, height=size*blueprintSize+50)
canvas.grid(column=0, row=0)


controlFrame = tk.Frame(root)
controlFrame.grid(column=1, row=0, padx=30)


blockNumberFrame = tk.Frame(controlFrame)
blockNumberFrame.pack()

numberOfBlock = tk.StringVar()
numberLabel = tk.Label(blockNumberFrame, text="number of blocks")
numberTextbox = tk.Entry(blockNumberFrame, width=20,
                         textvariable=numberOfBlock)
numberButton = tk.Button(blockNumberFrame, text="set",
                         command=onNumberButtonClicked)

numberLabel.grid(column=0, row=0, padx=5)
numberTextbox.grid(column=0, row=1, padx=5)
numberButton.grid(column=1, row=1, padx=5)


layerFrame = tk.Frame(controlFrame)
layerFrame.pack()

layerLabel = tk.Label(layerFrame, text="layer")
layer = tk.StringVar()
layerTextbox = tk.Entry(layerFrame, width=20, textvariable=layer)
layerButton = tk.Button(layerFrame, text="set", command=onlayerButtonClicked)

layerLabel.grid(column=0, row=0, padx=5)
layerTextbox.grid(column=0, row=1, padx=5)
layerButton.grid(column=1, row=1, padx=5)


blockNameFrame = tk.Frame(controlFrame)
blockNameFrame.pack()

nameOfBlock = tk.StringVar()
# Create a label
my_label = tk.Label(blockNameFrame, text="block name")
# Create an entry box
my_entry = tk.Entry(blockNameFrame, width=20, textvariable=nameOfBlock)
# Create a listbox
my_list = tk.Listbox(blockNameFrame, width=20)
nameButton = tk.Button(blockNameFrame, text="set", command=onNameButtonClicked)

# Add the toppings to our list
update(blockList)

my_label.grid(column=0, row=0, padx=5)
my_entry.grid(column=0, row=1, padx=5)
my_list.grid(column=0, row=2, padx=5)
nameButton.grid(column=1, row=1, padx=5)


buildButton = tk.Button(controlFrame, text="build", overrelief="solid",
                        width=15, command=lambda: blueprint.build())
buildButton.pack()

render(blueprint.blueprint)

canvas.bind("<Motion>", moved)
canvas.bind('<ButtonPress-1>', onPress)
canvas.bind('<ButtonRelease-1>', onRelease)
canvas.bind('<ButtonPress-3>', onRightPress)
canvas.bind('<ButtonRelease-3>', onRightRelease)


# Create a binding on the listbox onclick
my_list.bind("<<ListboxSelect>>", fillout)

# Create a binding on the entry box
my_entry.bind("<KeyRelease>", check)

root.mainloop()
