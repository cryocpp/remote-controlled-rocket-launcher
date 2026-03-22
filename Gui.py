import pygame, time 
import requests as req


iffired = False
movementqueue = []

def fire():
    print("> SENT Firing event to #arduino")
    try:
        firerequest = req.get("http://192.168.2.129/firerocket/")
        if firerequest.status_code == 200:
            print("Firing event sent OK")
    except Exception as error:
        print(f"Error > {error}")
        quit()

try:
    icon = pygame.image.load("logo.png")
    pygame.display.set_icon(icon)
    UIpic = pygame.image.load("uiv2.png")
    UIpic = pygame.transform.scale(UIpic, (540, 540))
    pygame.init()
    gui = pygame. display.set_mode((540, 540))
    pygame.display.set_caption("Remote Turret Control")
    gui.fill(color=(255,255,255))
    gui.blit(source=UIpic,dest=(0,0))
except Exception as error:
    print (f"Error: \n {error}")
    quit()


while True:
    for events in pygame.event.get(eventtype=[pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]): 
        gui.fill(color=(255,255,255))
        gui.blit(source=UIpic,dest=(0,0))
        mousex, mousey = pygame.mouse.get_pos()
        pygame.draw.circle(center=[mousex, mousey], surface=gui, color=(0, 255, 0),radius=3)
        if events.type == pygame.MOUSEBUTTONDOWN:
            if iffired == False:
                pygame.draw.circle(center=[mousex, mousey], surface=gui, color=(255, 0, 0), radius=23)
                fire()
                iffired=True
        if iffired:
            myfont = pygame.font.SysFont("Arial", 20, bold=True)
            infotext = myfont.render("Out of ammo", False, (0,0,255))
            gui.blit(source=infotext, dest=(28,40))
        pygame.display.update()
        mousex=mousex/3  
        mousey=mousey/3 
        print(mousex,mousey)

        aimcords = f"{round(mousey)},{round(mousex)}\n"  
        movementqueue.append(aimcords)
 
    if len(movementqueue) >= 3:
        try:
            movementreq = req.post("http://192.168.2.129/movpos/",data=movementqueue[2])
            if movementreq.status_code == 200:
                print("DEBUG > Movement response 200 ")
        except Exception as e:
            print(f"DEBUG > {e}")
            quit()
        movementqueue.clear()

