# Fox Jump Game

---
## Overview
This is the game I wrote, using the pygame library, it's a 2D endless game about a fox jumping into the skies on the randomly generated platforms.
Game has multiple screens, high score, and game over screen.

---
## Short Gameplay Video Demo


---
## Objective
My goal was to create a 2D game that would be similar to the game I played when I was in middle school and it's called "Doodle Jump"


---
## Purpose
* Create a game that has some sort of goal(such as beating the highscore), and is actually playable. 
* Learn the pygame library (reference: https://www.pygame.org/news).
* Practice using classes python.
* Learn how to animate a Player.
* Learn how to create basic collisions between sprites.

---
## Screenshots / Game Demonstration

---
### Start Screen
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
![walk_animation_demo](https://user-images.githubusercontent.com/59861277/163666730-8d7fe2d5-fbf6-4e60-b04c-21152e24ea24.gif)

---
### Jump Animation
![jump_animation_demo](https://user-images.githubusercontent.com/59861277/163666657-77a0f0ef-9f03-4fd8-9406-17fde0f06ec0.gif)



---
### Game Over Screen
<img width="478" alt="Screen Shot 2022-04-16 at 12 26 09 AM" src="https://user-images.githubusercontent.com/59861277/163666032-5a16a9d7-4d6d-482a-8323-a9aaa7ee3ad0.png">
