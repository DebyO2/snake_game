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
spod = Text(text="Frame Speed",position=(0.55,0.08,0),scale=1.5)
eed = InputField(text="Speed : ",default_value="0.2", position=(0.65,0,0),scale=(0.3,0.05),limit_content_to = "0123456789.")
Speed = 0.2

scoreboard = Text(text="", scale=1.5,position = (-0.85,0.47,0) , color = color.white)
keybind0 = Text(text="control to restart", scale=1.2,position = (-0.85,0.4,0) , color = color.white)
keybind1 = Text(text="esc to exit", scale=1.2,position = (-0.85,0.35,0) , color = color.white)
keybind2 = Text(text="wasd to move", scale=1.2,position = (-0.85,0.3,0) , color = color.white)


window.title = "snake"

paused = False

wall_kills = False

def walling():
    global wall_kills
    wall_kills = not wall_kills

wall_option = Button(text="wall kills : no",position=(0.6,0.2,0),scale=(0.16,0.1))
wall_option.on_click = walling

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
    global paused

    if key == "escape":
        application.quit()

    if key == "space":
        # application.hot_reloader.reload_code()
        paused = not paused

    if key == "control":
        application.hot_reloader.reload_code()

    if can_take_input and not paused:
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
        global Speed
        while mainThread.is_alive():
            if not paused:
                next_pos = self.position
                content = eed.text
                try:
                    content = float(content)
                    Speed = content
                except Exception as e:
                    content = Speed
                    eed.text = str(Speed)
                    # print(e)

                # print(content,type(content))
                # print(Speed)
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
                    
                    if wall_kills:
                        break
                    else:
                        self.x = -(abs(next_pos.x)/next_pos.x)*((width/2)-0.5)
                    
                
                elif abs(next_pos.y) > board.scale/2:
                    
                    if wall_kills:
                        break
                    else:
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

                time.sleep(Speed)

    def update(self):
        global paused
        scoreboard.text = f"Your Score : {score}"

        if wall_kills:
            wall_option.text = "wall kills : yes"
        else:
            wall_option.text = "wall kills : no"

        if eed.active:
            paused = True
        else:
            paused = False

        if not foods:
            food_spawn()

        if mainThread.is_alive() and not paused:
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