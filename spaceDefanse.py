import cv2
import mediapipe as mp
import math
import random

# --- 1. SETTINGS AND VARIABLES ---
width, height = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# MediaPipe Setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Game Variables
player_x, player_y = width // 2, height - 50
bullets = []      # Bullet coordinates [x, y]
enemies = []      # Enemy coordinates [x, y]
score = 0
lives = 3
game_over = False
fire_cooldown = 0 # Counter to prevent rapid firing

# Colors (B, G, R)
COLOR_BULLET = (0, 255, 255)   # Yellow
COLOR_ENEMY = (0, 0, 255)      # Red
COLOR_PLAYER = (255, 0, 0)     # Blue
COLOR_TEXT = (255, 255, 255)   # White

print("GAME STARTED! Press 'q' to Quit, 'r' to Restart.")

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip the frame horizontally (Mirror effect)
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # --- IF GAME IS NOT OVER ---
    if not game_over:
        
        # 1. Player Movement (Hand Tracking)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Index Finger Tip (Point 8)
                x8 = int(hand_landmarks.landmark[8].x * width)
                y8 = int(hand_landmarks.landmark[8].y * height)
                
                # Thumb Tip (Point 4)
                x4 = int(hand_landmarks.landmark[4].x * width)
                y4 = int(hand_landmarks.landmark[4].y * height)

                # Sync player ship with index finger position
                player_x = x8
                player_y = y8

                # 2. Shooting Control (Pinch Gesture)
                distance = math.hypot(x4 - x8, y4 - y8)
                
                # Fire if fingers are close (pinched) AND cooldown is 0
                if distance < 30 and fire_cooldown == 0:
                    bullets.append([player_x, player_y])
                    fire_cooldown = 8 # Wait 8 frames before next shot

        # Decrease cooldown
        if fire_cooldown > 0:
            fire_cooldown -= 1

        # 3. Spawn Enemies (Random)
        if random.randint(0, 100) < 3: # 3% chance to spawn an enemy per frame
            enemy_x = random.randint(20, width - 20)
            enemies.append([enemy_x, 0]) # Start from top (y=0)

        # 4. Movements and Collisions
        
        # Move Bullets (Upwards)
        for bullet in bullets[:]: # Iterate over a copy of the list
            bullet[1] -= 15 # Speed
            if bullet[1] < 0: # Remove if off-screen
                bullets.remove(bullet)

        # Move Enemies (Downwards)
        for enemy in enemies[:]:
            enemy[1] += 5 # Speed
            
            # Check Collision with Player
            dist_to_player = math.hypot(enemy[0] - player_x, enemy[1] - player_y)
            if dist_to_player < 40: # Collision detected
                lives -= 1
                enemies.remove(enemy)
                if lives <= 0:
                    game_over = True
            
            # Remove if enemy goes off-screen
            elif enemy[1] > height:
                enemies.remove(enemy)

        # Check Collision: Bullet vs Enemy
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                # Distance between bullet and enemy
                dist_bullet_enemy = math.hypot(bullet[0] - enemy[0], bullet[1] - enemy[1])
                if dist_bullet_enemy < 30: # Hit!
                    score += 10
                    try:
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                    except:
                        pass # Prevent errors if already removed

    # --- DRAWING ---
    
    # Draw Player (Blue Circle)
    cv2.circle(frame, (player_x, player_y), 20, COLOR_PLAYER, cv2.FILLED)
    
    # Draw Bullets (Yellow)
    for bullet in bullets:
        cv2.circle(frame, (bullet[0], bullet[1]), 8, COLOR_BULLET, cv2.FILLED)

    # Draw Enemies (Red)
    for enemy in enemies:
        cv2.circle(frame, (enemy[0], enemy[1]), 20, COLOR_ENEMY, cv2.FILLED)

    # UI: Score and Lives
    cv2.putText(frame, f"Score: {score}", (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, COLOR_TEXT, 2)
    cv2.putText(frame, f"Lives: {lives}", (width - 120, 30), cv2.FONT_HERSHEY_PLAIN, 2, COLOR_TEXT, 2)

    # GAME OVER SCREEN
    if game_over:
        cv2.putText(frame, "GAME OVER", (width//2 - 150, height//2), cv2.FONT_HERSHEY_DUPLEX, 3, (0,0,255), 3)
        cv2.putText(frame, "Press 'r' to restart", (width//2 - 150, height//2 + 50), cv2.FONT_HERSHEY_PLAIN, 2, COLOR_TEXT, 2)

    # Display Frame
    cv2.imshow("Hand Gesture Space Defense", frame)

    # Key Controls
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'): # Quit
        break
    if key == ord('r'): # Restart
        game_over = False
        lives = 3
        score = 0
        bullets = []
        enemies = []

cap.release()
cv2.destroyAllWindows()