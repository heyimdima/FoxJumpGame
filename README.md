# Fox Jump Game

---
## Overview
This is the game I wrote, using the pygame library, it's a 2D endless game about a fox jumping into the skies on the randomly generated platforms.
Game has multiple screens, high score, and game over screen.

---
## Short Gameplay Demo
![game_demo](https://user-images.githubusercontent.com/59861277/163667985-0f3653be-da93-421a-ae81-cb6dada36434.gif)

---
## Objective
My goal was to create a 2D game that would be similar to the game I played when I was in middle school and it's called "Doodle Jump"


---
## Purpose
* Create a game that has some sort of goal(such as beating the highscore), and is actually playable. 
* Learn the pygame library (reference: https://www.pygame.org/news).
* Practice using classes python.
* Learn how to animate sprites.
* Learn how to create basic collisions between sprites.

---
## Screenshots / Game Demonstration

---
### Start Screen
```python
...some code
    def show_start_screen(self):
        # game splash/start screen
        pg.mixer.music.load(path.join(self.snd_dir, 'menu_music.ogg'))
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text("Fox Jump", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Arrows to move, SPACE to jump", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to start.", 26, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, 15)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
some code...
```
<img width="479" alt="Screen Shot 2022-04-16 at 12 25 47 AM" src="https://user-images.githubusercontent.com/59861277/163666018-b563e427-a703-42eb-b2dc-eaf59555a200.png">

---
### Idle Animation
* Consist of 4 frames

```python
...some code
        # idle frames
        self.idle_frames = [self.game.spritesheet.get_image(7, 24, 18, 22),
                            self.game.spritesheet.get_image(41, 25, 19, 21),
                            self.game.spritesheet.get_image(74, 26, 21, 20),
                            self.game.spritesheet.get_image(6, 59, 19, 21)]
        for frame in self.idle_frames:
            frame.set_colorkey(BLACK)
some code...
```
```python
...some code
   # show idle animation
        if not self.jumping and not self.walking:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.idle_frames)
                bottom = self.rect.bottom
                self.image = self.idle_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
some code...
```
![idle_animation_demo](https://user-images.githubusercontent.com/59861277/163666608-dd83b281-e3e8-47c6-8904-02410f796e62.gif)

---
### Walk Animation
* Consist of 6 frames
```python
...some code
            # walk frames
        self.walk_frames_r = [self.game.spritesheet.get_image(7, 92, 18, 22),
                              self.game.spritesheet.get_image(41, 91, 20, 22),
                              self.game.spritesheet.get_image(77, 92, 18, 22),
                              self.game.spritesheet.get_image(113, 11, 18, 22),
                              self.game.spritesheet.get_image(114, 44, 17, 22),
                              self.game.spritesheet.get_image(113, 79, 18, 22)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
some code...
```
* Frames to walk left are flipped using `pygame.transform.flip` in order to efficiently write the code.

```python
...some code
        # show walking animation
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
some code...
```
![walk_animation_demo](https://user-images.githubusercontent.com/59861277/163666730-8d7fe2d5-fbf6-4e60-b04c-21152e24ea24.gif)

---
### Jump Animation
* Consist of 2 frames
```python
...some code
        # jump frames
        self.jump_frames_r = [self.game.spritesheet.get_image(40, 57, 23, 21),
                              self.game.spritesheet.get_image(76, 55, 21, 22)]
        self.jump_frames_l = []
        for frame in self.jump_frames_r:
            frame.set_colorkey(BLACK)
            self.jump_frames_l.append(pg.transform.flip(frame, True, False))
some code...
```

```python
...some code
        # show jumping animation if we're jumping
        if self.jumping:
            if self.vel.y < 0 and self.vel.x > 0:
                self.image = self.jump_frames_r[0]
                self.walking = False
        if self.jumping:
            if self.vel.y > 0 and self.vel.x > 0:
                self.image = self.jump_frames_r[1]
                self.walking = False
        if self.jumping:
            if self.vel.y < 0 and self.vel.x < 0:
                self.image = self.jump_frames_l[0]
                self.walking = False
        if self.jumping:
            if self.vel.y > 0 and self.vel.x < 0:
                self.image = self.jump_frames_l[1]
                self.walking = False
some code...
```
![jump_animation_demo](https://user-images.githubusercontent.com/59861277/163666657-77a0f0ef-9f03-4fd8-9406-17fde0f06ec0.gif)




---
### Game Over Screen

```python
...some code
    def show_go_screen(self):
        # game over / continue
        if not self.running:
            return
        self.screen.fill(BGCOLOR)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score: " + str(self.score), 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to play again", 26, WHITE, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), "w") as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
some code...
```
<img width="478" alt="Screen Shot 2022-04-16 at 12 26 09 AM" src="https://user-images.githubusercontent.com/59861277/163666032-5a16a9d7-4d6d-482a-8323-a9aaa7ee3ad0.png">

---
## What I Learned
* Improved my undestanding of pygame library.
* Learned how to animate sprites using spritesheets.
* Improved my Python skills.
