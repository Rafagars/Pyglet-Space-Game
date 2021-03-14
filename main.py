import pyglet
from pyglet.window import key
import math
import random

window = pyglet.window.Window(800, 600)

# Background
background = pyglet.resource.image('Background/space.png')

# Sound
music = pyglet.resource.media('audio/background.wav')
music.play()

# Score
score = 0
score_label = pyglet.text.Label('Score: ' + str(score), font_name='Free Sans', font_size=16, x = 10, y = 560)

# Game Over
game_over = False
game_over_label = pyglet.text.Label('GAME OVER', font_name='Free Sans', font_size=36, 
                                   x = window.width//2, y = window.height//2, 
                                   anchor_x='center', anchor_y='center')

# Player Class
class Player(pyglet.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.image('sprites/P-blue-b.png'), 320, 10)
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.beam = pyglet.sprite.Sprite(pyglet.resource.image('sprites/Bullet1.png'))
        self.beam.visible = False
        self.beam.sound = pyglet.media.load('audio/laser.wav', streaming=False)
        self.key_handler = key.KeyStateHandler()
    
    def fire_bullet(self):
        self.beam.visible = True
        self.beam.y +=  10

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        if self.key_handler[key.LEFT]:
            self.velocity_x -= 5
        elif self.key_handler[key.RIGHT]:
            self.velocity_x += 5
        else:
            self.velocity_x = 0
        if self.key_handler[key.SPACE]:
            if not self.beam.visible:
                self.beam.sound.play()
                # Get the current x coordinate of the spaceship
                self.beam.x = self.x + 56
                self.beam.y = self.y + 70
                self.fire_bullet() 
            
player = Player()

window.push_handlers(player)
window.push_handlers(player.key_handler)

# Enemy Class and batch
enemies = pyglet.graphics.Batch()
class Enemy(pyglet.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.image('sprites/Enemy1.png'), batch=enemies)
        self.x_change = 4
        self.y_change = 40

    

num_of_enemies = 6
enemy_sprites = []

for i in range(num_of_enemies):
    enemy_sprites.append(Enemy())
    enemy_sprites[i].update(x = random.randint(0, 736), y = random.randint(350, 500))


def isCollision(one, two):
    distance = math.sqrt(math.pow(one.x - two.x, 2) + (math.pow(one.y - two.y, 2)))
    if distance < 27:
        return True
    else:
        return False

def update(dt):
    #Player Movement
    player.update(dt)
    if player.x < 0:
        player.x = 0
    elif player.x >= 680:
        player.x = 680
    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemy_sprites[i].y < 30:
            for j in range(num_of_enemies):
                enemy_sprites[j].y = 2000
                global game_over
                game_over = True
            break

        enemy_sprites[i].x += enemy_sprites[i].x_change
        if enemy_sprites[i].x <= 0:
            enemy_sprites[i].x_change = 4
            enemy_sprites[i].y -= enemy_sprites[i].y_change
        elif enemy_sprites[i].x >= 736:
            enemy_sprites[i].x_change = -4
            enemy_sprites[i].y -= enemy_sprites[i].y_change

        # Collision
        collision = isCollision(enemy_sprites[i], player.beam)
        if collision:
            explosion = pyglet.media.load("audio/explosion.wav")
            explosion.play()
            player.beam.y = 0
            player.beam.visible = False
            global score
            score += 1
            score_label.text = 'Score: ' + str(score)
            enemy_sprites[i].x = random.randint(0, 736)
            enemy_sprites[i].y = random.randint(350, 500)

    if player.beam.y >= 580:
        player.beam.y = 0
        player.beam.visible = False
    
    if player.beam.visible:
        player.fire_bullet()

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    score_label.draw()
    player.draw()
    enemies.draw()
    player.beam.draw()
    if game_over:
        game_over_label.draw()

        
pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()