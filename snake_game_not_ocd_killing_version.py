from ursina import *

import threading

app = Ursina()

camera.orthographic = True

board = Entity("board",model="quad",scale=37,color=color.black)

length = board.scale_x
width = board.scale_y

foods = []

mainThread = threading.current_thread()

score = 0

scoreboard = Text(text="", scale=1.5,position = (-0.85,0.45,0) , color = color.white)
keybind0 = Text(text="space to restart", scale=1.2,position = (-0.85,0.4,0) , color = color.white)
keybind1 = Text(text="esc to exit", scale=1.2,position = (-0.85,0.35,0) , color = color.white)
keybind2 = Text(text="wasd to move", scale=1.2,position = (-0.85,0.3,0) , color = color.white)

window.title = "snake"


class Food(Entity):
    

    def __init__(self,position):
        super().__init__(model="quad",scale=0.6,z=0,color=color.red,position=position,collider="box")

    def update(self):
        
        global score
        hitInfo = self.intersects()
        
        if hitInfo.hit:
            foods.pop()
            destroy(self)
            a.append_body()
            score += 1
            
def food_spawn():

    random_position = [int(random.uniform(-length/2,length/2)),int(random.uniform(-width/2,width/2))]

    food = Food(position=random_position)
    foods.append(food)

    return random_position


can_take_input = True


def input(key):
    global a

    if key == "escape":
        application.quit()

    if key == "space":
        application.hot_reloader.reload_code()

    if can_take_input:
        if key == "w" and not a.direction == "down" and abs(a.x) < board.scale/2:
            a.direction = "up"
        if key == "s" and not a.direction == "up" and abs(a.x) < board.scale/2:
            a.direction = "down"
        if key == "a" and not a.direction == "right" and abs(a.y) < board.scale/2:
            a.direction = "left"
        if key == "d" and not a.direction == "left" and abs(a.y) < board.scale/2:
            a.direction = "right"

class Body(Entity):

    def __init__(self,position,Zrotation):
        super().__init__(model="cube", scale=(0.7,0.7),
         color=color.green,
         x=position.x, y=position.y, z=0,collider="box",
         rotation_z=Zrotation)

        self._collided_onces = 0
class Snake(Entity):

    def __init__(self):
        super().__init__(model="cube", scale=(0.7,0.99), color=color.white, x=0, y=0, z=0,collider="box")

        self.direction = "up"
        self.speed = 1
        self.body = []

        self.track = []
        
        self.rotation_matrix = []

    def append_body(self):
        
        self.body.append(Body(self.position,self.rotation_z))

    def move(self):
        while mainThread.is_alive():
            next_pos = self.position
            
            

            cols = self.intersects()
            if cols.hit:
                if type(cols.entity) == Body:
                    
                    if cols.entity._collided_onces == 1 :
                        break
                    else:
                        cols.entity._collided_onces += 1

                        if cols.entity._collided_onces == 0:
                            self.append_body()

            if self.direction == "right":
                next_pos.x += self.speed
            if self.direction == "left":
                next_pos.x -= self.speed
            if self.direction == "up":
                next_pos.y += self.speed
            if self.direction == "down":
                next_pos.y -= self.speed

            if abs(next_pos.x) > board.scale/2:
                
                self.x = -(abs(next_pos.x)/next_pos.x)*((width/2)-0.5)
                
            
            elif abs(next_pos.y) > board.scale/2:
                
                self.y = -(abs(next_pos.y)/next_pos.y)*((length/2)-0.5)
            
            else:
                self.position = next_pos

            
            self.track.append(self.position)
            cur_index = -1

            try:
                for i in self.body:
                    i.position = self.track[cur_index-1]
                    cur_index -= 1

            except Exception as e:
                print(e)

            time.sleep(0.2)

    def update(self):
        scoreboard.text = f"Your Score : {score}"

        if not foods:
            food_spawn()

        if self.direction == "right":

            self.rotation_z = 90
        elif self.direction == "left":
          
            self.rotation_z = -90
        elif self.direction == "up":
            self.rotation_z = 180

        elif self.direction == "down":
            
            self.rotation_z = -180


a = Snake()

thread = threading.Thread(target=a.move)
thread.start()


app.run()