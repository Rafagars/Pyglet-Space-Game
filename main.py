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
game_over_label = pyglet.text.Label('GAME OVER', font_name='Free Sans', font_size=36, 
                                   x = window.width//2, y = window.height//2, 
                                   anchor_x='center', anchor_y='center')

# Player Class
class Player(pyglet.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.image('sprites/P-blue-b.png'), 320, 10)
        self.velocity_x, self.velocity_y = 0.0, 0.0
        self.key_handler = key.KeyStateHandler()

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        if self.key_handler[key.LEFT]:
            self.velocity_x -= 2
        elif self.key_handler[key.RIGHT]:
            self.velocity_x += 2
        else:
            self.velocity_x = 0
"""     if self.key_handler[key.SPACE]:
            if bullet.state == "ready":
                bullet.sound.play()
                # Get the current x coordinate of the spaceship
                bullet.x = self.x + 56
                bullet.y = self.y + 70
                bullet.fire_bullet()  """
            
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

# Bullet
class Bullet(pyglet.sprite.Sprite):
    def __init__(self):
        super().__init__(pyglet.resource.image('sprites/Bullet1.png'))
        self.visible = False
        self.state = "ready"
        self.sound = pyglet.media.load('audio/laser.wav', streaming=False)

    def fire_bullet(self):
        self.state = "fire"
        self.visible = True
        self.y +=  10

bullet = Bullet()

def isCollision(one, two):
    return (one.x >= two.x and one.x <= two.x + two.width) and (one.y >= two.y and one.y <= two.y + two.height) or (two.x >= one.x and two.x <= one.x + one.width) and (two.y >= one.y and two.y <= one.y + one.height)


"""@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.SPACE:
        if bullet.state == "ready":
            bullet.sound.play()
            # Get the current x coordinate of the spaceship
            bullet.x = player.x + 56
            bullet.y = player.y + 70
            bullet.fire_bullet() """
 
def update(dt):
    player.update(dt)
    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemy_sprites[i].y < 20:
            for j in range(num_of_enemies):
                enemy_sprites[j].y = 2000
            game_over_label.draw()
            break

        enemy_sprites[i].x += enemy_sprites[i].x_change
        if enemy_sprites[i].x <= 0:
            enemy_sprites[i].x_change = 4
            enemy_sprites[i].y -= enemy_sprites[i].y_change
        elif enemy_sprites[i].x >= 736:
            enemy_sprites[i].x_change = -4
            enemy_sprites[i].y -= enemy_sprites[i].y_change

        # Collision
        collision = isCollision(enemy_sprites[i], bullet)
        if collision:
            explosion = pyglet.media.load("audio/explosion.wav")
            explosion.play()
            bullet.y = 0
            bullet.state = "ready"
            bullet.visible = False
            global score
            score += 1
            enemy_sprites[i].x = random.randint(0, 736)
            enemy_sprites[i].y = random.randint(350, 150)

    if bullet.y >= 580:
        bullet.y = 0
        bullet.state = "ready"
        bullet.visible = False
    
    if bullet.state == "fire":
        bullet.fire_bullet()

@window.event
def on_draw():
    window.clear()
    background.blit(0, 0)
    score_label.draw()
    player.draw()
    enemies.draw()
    bullet.draw()

        
pyglet.clock.schedule_interval(update, 1/120.0)
pyglet.app.run()