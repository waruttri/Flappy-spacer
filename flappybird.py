import pygame,random
from PIL import Image
import requests
import cv2
import numpy as np
import sys
import pathlib
import os

class Bird(pygame.sprite.Sprite):
   def __init__(self,game):
      super().__init__()
      self.image=pimg[0] #Initial Start Picture
      self.image=pygame.transform.scale(self.image,(150,85)) #Re-scale picture ==> 100x85
      self.rect=self.image.get_rect()
      self.vel=vec(0,0)
      self.rect.center=(dw/2,dh/2) #Start at the centor of display
      self.acc=vec(0,0)
      self.pos=vec(self.rect.center)
      self.fc=0
   def update(self):
      self.acc=vec(0,1.5)
      self.vel=vec(0,0)
      keys=pygame.key.get_pressed()
      if keys[pygame.K_SPACE]: #Press Space Bar ==> Up
         self.acc.y=-1.5
         if self.fc+1<28: #Update location of the player
            self.fc+=1
            self.image=pimg[self.fc//7]
            self.image=pygame.transform.scale(self.image,(150,85))
         else:
            self.fc=0
      else:
         self.image=pimg[0]
         self.image=pygame.transform.scale(self.image,(150,85))
      self.vel+=self.acc
      self.pos+=self.vel+0.5*self.acc
      if self.pos.y<=0+self.rect.width/2:
         self.pos.y=0+self.rect.width/2
      if self.pos.y>=dh-self.rect.width/2:
         self.pos.y=dh-self.rect.width/2
      self.rect.center=self.pos
      self.mask=pygame.mask.from_surface(self.image)
class TBlock(pygame.sprite.Sprite): #Generate Top Pipe
   def __init__(self,x,h1):
      super().__init__()
      self.image=pygame.image.load('tp.png') #Load tp.png as Top Pipe
      self.image=pygame.transform.scale(self.image,(80,h1)) #Re-scale of the pipe 
      self.rect=self.image.get_rect()
      self.rect.x,self.rect.y=x,0
   def update(self):
      self.rect.x-=2
      self.mask1=pygame.mask.from_surface(self.image)
class BBlock(pygame.sprite.Sprite): #Genertate Bottom Pipe
   def __init__(self,x,h2):
      super().__init__()
      self.image=pygame.image.load('bp.png')
      self.image=pygame.transform.scale(self.image,(80,h2))
      self.rect=self.image.get_rect()
      self.rect.x,self.rect.y=x,dh-self.rect.height
   def update(self):
      self.rect.x-=2
      self.mask2=pygame.mask.from_surface(self.image)
class Game: # The Game
   def __init__(self):
      self.bgx=0
      self.x=650
      self.h1=180
      self.h2=180
      self.score=0
      self.gover=0
      self.last=pygame.time.get_ticks()
   def blockgen(self):
      x=random.randint(620,650)
      h=random.choice(blist) #Random Height of the Pipe during Game Play
      h1=h[0]
      h2=h[1]
      self.tblock=TBlock(x,h1)
      self.tblocks=pygame.sprite.Group()
      self.tblocks.add(self.tblock)
      self.all_sprites.add(self.tblock)
      self.bblock=BBlock(x,h2)
      self.bblocks=pygame.sprite.Group()
      self.bblocks.add(self.bblock)
      self.all_sprites.add(self.bblock)
   def new(self): #Setting Up - New Game
      self.bird=Bird(self)
      self.all_sprites=pygame.sprite.Group()
      self.all_sprites.add(self.bird)
      self.tblock=TBlock(self.x,self.h1)
      self.tblocks=pygame.sprite.Group()
      self.tblocks.add(self.tblock)
      self.all_sprites.add(self.tblock)
      self.bblock=BBlock(self.x,self.h2)
      self.bblocks=pygame.sprite.Group()
      self.bblocks.add(self.bblock)
      self.all_sprites.add(self.bblock)
      self.score=0
      self.gover=0
   def msg(self,text,x,y,color,size): #Message in Game
      self.font=pygame.font.SysFont('Kristen ITC',size,bold=1)
      msgtxt=self.font.render(text,1,color)
      msgrect=msgtxt.get_rect()
      msgrect.center=x/2,y/2
      screen.blit(msgtxt,(msgrect.center))
   def pause(self): # Pause Game
      wait=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT: #Press ESC or Close Icon
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN: #Press Enter
                  wait=0
         self.msg("Paused",dw-100,dh-100,blue,40)
         pygame.display.flip()
   def over(self): #Game Over
      global highest_score
      wait=1
      self.gover=1
      while wait:
         for event in pygame.event.get():
            if event.type==pygame.QUIT:
               pygame.quit()
               quit()
            if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  wait=0
         self.msg("Game Over",dw-250,dh-100,red,40)
         if(self.score>int(highest_score)):
                highest_score = self.score
                record_score()
         self.msg("Press Enter to Play Again",dw-450,dh+200,white,30)
         pygame.display.flip()
      self.new()# Setting Up New Game
   def scores(self):
         self.msg("Your Score: "+str(self.score),0,dh-450,green,30)
         self.msg("High Score: {}".format(highest_score),dw+120,dh-450,white,28)
      
   def update(self):#During Game Play
     self.all_sprites.update()
     now=pygame.time.get_ticks()
     hits1=pygame.sprite.spritecollide(self.bird,self.bblocks,False,pygame.sprite.collide_mask)
     hits2=pygame.sprite.spritecollide(self.bird,self.tblocks,False,pygame.sprite.collide_mask)
     if hits1 or hits2:
        self.over()       
     relx=self.bgx%bw+5
     screen.blit(bg,(relx-bw+3,0))
     if relx<dw:
        screen.blit(bg,(relx,0))
     self.bgx-=2
     if self.bblock.rect.x<dw/2 and self.tblock.rect.x<dw/2:
        self.blockgen()
        self.score+=1
     if now-self.last>1500:
         self.last=now
         self.score+=1
     else:
        self.score+=0
         
   def draw(self):
      self.all_sprites.draw(screen)
      self.scores()
   def event(self):
      for event in pygame.event.get():
         clock.tick(60)
         if event.type==pygame.QUIT:
            pygame.quit()
            quit()
         if event.type==pygame.KEYDOWN:
               if event.key==pygame.K_RETURN:
                  self.pause()
   def run(self):
      while 1:
         self.event()
         self.update()
         self.draw()
         pygame.display.flip()

def text_objects(text, font):
    textSurface = font.render(text, True, violet)
    return textSurface, textSurface.get_rect()

def text_objects2(text, font):
    textSurface2 = font.render(text, True, lightblue)
    return textSurface2, textSurface2.get_rect()

def game_opening():
    pass

def game_intro():
    intro = True
    img = pygame.image.load("intro.png")
    gameDisplay = pygame.display.set_mode((dw,dh))
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    intro = False
        gameDisplay.blit(img,(0,0))
        largeText = pygame.font.SysFont('Kristen ITC',48)
        TextSurf, TextRect = text_objects("Flappy Spacer", largeText)
        TextRect.center = ((dw/2),(dh*7/8))
        TextSurf2, TextRect2 = text_objects2('Press "Space" Button', largeText)
        TextRect2.center = ((dw/2),(dh/4))
        gameDisplay.blit(TextSurf, TextRect)
        gameDisplay.blit(TextSurf2, TextRect2)
        pygame.display.update()
        clock.tick(15)

def take_picture_cv():
    current_path = pathlib.Path().absolute()
    cascPath = "{}\{}".format(current_path,"haarcascade_frontalface_default.xml")
    faceCascade = cv2.CascadeClassifier(cascPath)
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("Press SPACE to take a photo")
    camera_on = True
    while camera_on: 
        # Capture frame-by-frame
        ret, frame = cam.read()  
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.1,minNeighbors=5,minSize=(30, 30))
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow("Let 's take a photo", frame)
        if not ret:
            break
        k = cv2.waitKey(1)
        if k%256 == 27: #ESC pressed
            break
        elif k%256 == 32: #SPACE pressed
            img_name = "opencv_frame_0.png"
            cv2.imwrite(img_name, frame)
            image = cv2.imread("opencv_frame_0.png")
            clone = image.copy()
            image = clone.copy()
            crop_img = image[y+2:y+h-1, x+2:x+w-1]
            cv2.imshow("crop_img", crop_img)
            cv2.imwrite("{}\{}".format(current_path,"face_img.png"), crop_img)
            #cv2.waitKey(0)
            camera_on = False
    cam.release()
    cv2.destroyAllWindows()
    removebg("{}\{}".format(current_path,"face_img.png"))
    paste()

def removebg(image_path):
    current_path = pathlib.Path().absolute()
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(image_path, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'tKkHoWkUdgDPmw6FonGnaEPm'},
   )
    if response.status_code == requests.codes.ok:
        with open("{}\{}".format(current_path,'face_img_no_bg.png'), 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

def paste():
    current_path = pathlib.Path().absolute()
    spacer_path = "{}\{}".format(current_path,"template.png") #1120x558
    face_path = "{}\{}".format(current_path,"face_img_no_bg.png")
    image = Image.open(spacer_path)
    face = Image.open(face_path)
    resize_face = face.resize((225, 225))
    resize_face=resize_face.rotate(-25)
    for i in range(1,5):
        image_copy = image.copy()
        position = ((image_copy.width - resize_face.width - 250), (image_copy.height - resize_face.height - 250)) #position = ((645), (80))
        image_copy.paste(resize_face, position, resize_face)
        image_copy.paste(image, (0,0), image)
        image_copy.save("{}\{}".format(current_path,"{}.png".format(i)))

def spacer():
    current_path = pathlib.Path().absolute()
    spacer_path = "{}\{}".format(current_path,"1.png")
    gameDisplay = pygame.display.set_mode((dw,dh))
    image = pygame.image.load(spacer_path)  
    image = pygame.transform.scale(image,(dw,dh))
    gameDisplay.fill(white)
    largeText = pygame.font.SysFont('Kristen ITC',48)
    TextSurf, TextRect = text_objects("Hi Spacer", largeText)
    TextRect.center = ((dw-450),(dh-400))
    gameDisplay.blit(image, (0, 0))
    gameDisplay.blit(TextSurf, TextRect)
    #gameDisplay.blit(TextSurf2, TextRect2)
    pygame.display.update()
    clock.tick(15)
    pygame.time.delay(3000)
    gameDisplay.fill(white)
    TextSurf, TextRect = text_objects("Go!!!", largeText)
    TextRect.center = ((dw/2),(dh/2))
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()
    pygame.time.delay(1000)

def read_score():
        current_path = pathlib.Path().absolute()
        score_path = "{}\{}".format(current_path,"score.txt")
        if pathlib.Path(score_path).is_file():
            f = open(score_path, "r")
            score = (f.readline())
            f.close() 
        else:
            file = open("score.txt", "w") 
            file.write("0") 
            file.close() 
            score = 0  
        return score

def record_score():
    current_path = pathlib.Path().absolute()
    score_path = "{}\{}".format(current_path,"score.txt")
    if pathlib.Path(score_path).is_file():
        f = open(score_path, "w")
        f.write(str(highest_score))
        f.close()

pygame.init()
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(0,255,0)
blue=(0,0,255)
lightblue=(0,168,243)
violet=(144,61,186)
dw=600 #Width of Screen
dh=476 #Height of Screen
screen=pygame.display.set_mode([dw,dh]) #Pygame Display
pygame.display.set_caption('Flappy Spacer')
#pimg=[pygame.image.load(str(i)+'.png') for i in range(1,5)]
clock=pygame.time.Clock()
vec=pygame.math.Vector2
bg=pygame.image.load('bg.png') #Load Background Pigture
bw=bg.get_width()
blist=[[50,310],[60,300],[70,290],[80,280],[90,270],[100,260],[110,250],[120,240],[130,230],[140,220],[150,210],[160,200],[170,190],[180,180],
       [190,170],[200,160],[210,150],[220,140],[230,130],[240,120],[250,110],[260,100],[270,90],[280,80]
       ,[290,70],[300,60],[310,50]] #Height of Top and Bottom Pipe [Top,Bottom]
highest_score = read_score()


def main():
    g=Game()
    while g.run:
        g.new()
        g.run()

game_intro()
take_picture_cv()
pimg=[pygame.image.load(str(i)+'.png') for i in range(1,5)] #Load Picture
spacer()
main()
