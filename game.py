import pygame
import random
import time

pygame.init()

# --- Screen Setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Racer")

clock = pygame.time.Clock()

# --- Colors & Font ---
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
GREEN   = (0, 255, 0)
RED     = (255, 0, 0)
GRAY    = (50, 50, 50)
FONT_SIZE = 28
font = pygame.font.SysFont("monospace", FONT_SIZE)

# --- Text Segments (each ~100 words) ---
TEXTS = [
    # Segment 1: (Inspired by Pride and Prejudice)
    ("It is a truth universally acknowledged, that a single man in possession of a good fortune, "
     "must be in want of a wife. However little known the feelings or views of such a man may be on "
     "his first entering a neighbourhood, this truth is so well fixed in the minds of the surrounding "
     "families, that he is considered as the rightful property of some one or other of their daughters. "
     "My dear Mr. Bennet, have you heard that Netherfield Park is let at last? The news spread quickly "
     "throughout the village, stirring excitement and anticipation among all. Absolutely remarkable."),
    
    # Segment 2: (Inspired by Moby Dick)
    ("Call me Ishmael. Some years ago, never mind how long precisely, having little or no money in my purse, "
     "and nothing particular to interest me on shore, I thought I would sail about a little and see the watery "
     "part of the world. It is a way I have of driving off the spleen and regulating the circulation. Whenever "
     "I find myself growing grim about the mouth; whenever it is a damp, drizzly November in my soul; whenever "
     "I find myself involuntarily pausing before coffin warehouses; and especially when my hypos get such an upper "
     "hand of me beyond measure."),
    
    # Segment 3: (Inspired by A Tale of Two Cities)
    ("It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of foolishness, "
     "it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, it was the season of "
     "Darkness, it was the spring of hope, it was the winter of despair. We had everything before us, we had nothing "
     "before us, we were all going direct to Heaven, we were all going direct the other way. In short, the period was "
     "like the present period. A paradox that stirred deep hearts."),
    
    # Segment 4: (Inspired by The Hobbit)
    ("In a hole in the ground there lived a hobbit. Not a nasty, dirty, wet hole, filled with the ends of worms and an oozy "
     "smell, nor yet a dry, bare, sandy hole with nothing in it to sit down on or to eat; it was a hobbit-hole, and that means "
     "comfort. The hobbit was a cheerful creature, fond of food, drink, and good company. He loved to tell stories and share adventures, "
     "and his heart was full of quiet dreams and secret hopes. Yet, destiny awaited him beyond his cozy door. A grand quest unfolded before his eager eyes."),
    
    # Segment 5: (Inspired by Star Wars)
    ("In a galaxy far, far away, a struggle between light and dark unfolded. Brave heroes fought against oppressive empires, their "
     "destinies intertwined with the fate of countless worlds. Jedi knights, masters of the Force, stood as guardians of peace and justice, "
     "wielding wisdom and courage. Their battles were fierce, their sacrifices great, as they sought to restore balance in a tumultuous universe. "
     "Amid starry battles and ancient prophecies, hope shone like a beacon, uniting rebels and dreamers alike in a timeless quest for freedom. "
     "Legends were born on every battleground, and whispered promise of hope kindled the fire of rebellion."),
    
    # Segment 6: (Inspired by The Godfather)
    ("In the dark corridors of power, loyalty and betrayal danced a delicate waltz. A man of quiet determination, with eyes that spoke "
     "of both kindness and ruthlessness, wielded authority like a finely honed blade. His words, measured and deliberate, held the weight of "
     "unspoken promises and dangerous threats. In hushed tones, his orders resonated, leaving no room for defiance. Those who heard them knew that "
     "his offer was not merely a suggestion, but a decree that could not be ignored, for resistance carried a cost that few could bear. In that moment, "
     "silence reigned, sealing fates with an unyielding finality."),
    
    # Segment 7: (Inspired by Sherlock Holmes)
    ("In the quiet streets of London, beneath a veil of fog and mystery, a brilliant detective unraveled the secrets of the human mind. His keen "
     "observation and relentless pursuit of truth allowed him to see what others overlooked. Each clue was a thread in the intricate tapestry of a crime, "
     "and every seemingly insignificant detail held the key to a larger enigma. With a calm demeanor and razor-sharp intellect, he deciphered puzzles that "
     "confounded even the most learned scholars, leaving behind a legacy of justice and reason. His methods, though unorthodox, shone as a brilliant beacon in the darkest night."),
    
    # Segment 8: (Inspired by Game of Thrones)
    ("In the cold and unforgiving lands of Westeros, where honor is scarce and treachery lurks in every shadow, ancient houses clashed in a struggle "
     "for power and survival. The bitter winds carried whispers of prophecies and the fall of mighty kingdoms. Amid the snow and ice, heroes emerged from "
     "unexpected places, driven by duty and the desire for justice. As winter loomed over the realm, every man and woman steeled themselves for the trials ahead, "
     "knowing that the harsh season would test their very souls. In that moment, pure hope mingled with fear, as destiny beckoned them into the unknown."),
    
    # Segment 9: (Inspired by Taxi Driver)
    ("In the gritty underbelly of a restless city, a lone figure confronted the isolation and chaos that filled the streets. His voice, rough and unwavering, "
     "cut through the silence of dimly lit alleyways. Every word he uttered carried the weight of a lifetime spent battling inner demons and the harsh realities of urban life. "
     "Amid the blaring horns and flickering neon signs, his challenge resonated with those who felt forgotten, a defiant call to awaken and reclaim their dignity in a world gone mad. "
     "In that moment, a spark of rebellion ignited, urging every lost soul to rise and fight."),
    
    # Segment 10: (Inspired by Breaking Bad)
    ("In the quiet desperation of suburban life, a man discovered a hidden world of danger and possibility. His transformation was gradual yet undeniable, as he stepped "
     "away from mediocrity into a realm ruled by ambition and the pursuit of power. Each decision carried consequences that rippled through his existence, forever altering the lives "
     "of those around him. With a mind as sharp as a scalpel and a resolve forged in hardship, he embraced the chaos, turning his pain into a weapon against a world that had betrayed him. "
     "In that moment, destiny and despair merged into a singular, fateful choice.")
]

# --- Text Wrapping Function ---
def wrap_text(text, font, max_width):
    """
    Wraps text into lines that fit within max_width (in pixels) without breaking words.
    """
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    if current_line:
        lines.append(current_line.strip())
    return lines

# --- Game Reset Function ---
def reset_game():
    """
    Chooses a random passage from TEXTS and wraps it into lines.
    We use a 20-pixel margin on each side.
    """
    target_text = random.choice(TEXTS)
    wrapped_lines = wrap_text(target_text, font, WIDTH - 40)
    return wrapped_lines

# --- Drawing Helper Functions ---
def draw_text_line(line, user_input, x, y):
    """
    Draws a line letter-by-letter.
    Correct letters appear in GREEN, incorrect ones in RED, and untyped letters in WHITE.
    """
    x_offset = x
    for i, char in enumerate(line):
        if i < len(user_input):
            color = GREEN if user_input[i] == char else RED
        else:
            color = WHITE
        char_surface = font.render(char, True, color)
        screen.blit(char_surface, (x_offset, y))
        x_offset += char_surface.get_width()

def draw_timer_bar(elapsed, time_limit):
    """
    Draws a full-width timer bar at the top of the screen that shrinks as time elapses.
    """
    full_width = WIDTH  # No horizontal margin.
    time_left = max(time_limit - elapsed, 0)
    bar_width = int((time_left / time_limit) * full_width)
    pygame.draw.rect(screen, GRAY, (0, 0, full_width, 20))
    pygame.draw.rect(screen, GREEN, (0, 0, bar_width, 20))

def calculate_wpm(completed_lines, current_line, current_input, elapsed):
    """
    Calculates Words Per Minute (WPM) based on correctly typed text.
    Only the correctly typed prefix of the current line is counted.
    """
    correct_text = " ".join(completed_lines)
    correct_prefix = ""
    for i, char in enumerate(current_line):
        if i < len(current_input) and current_input[i] == char:
            correct_prefix += char
        else:
            break
    if correct_prefix:
        correct_text = (correct_text + " " + correct_prefix).strip() if correct_text else correct_prefix
    word_count = len(correct_text.split())
    return int(word_count * 60 / elapsed) if elapsed > 0 else 0

# --- Main Game Loop ---
def main():
    running = True
    time_limit = 10  # seconds
    game_over = False
    timer_started = False
    start_time = 0
    elapsed = 0

    target_lines = reset_game()  # Get a new passage.
    current_line_index = 0      # Current line being typed.
    current_input = ""          # User's input for the current line.
    completed_lines = []        # List of completed lines.
    result_wpm = 0

    while running:
        dt = clock.tick(60) / 1000
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN:
                    if not timer_started:
                        timer_started = True
                        start_time = time.time()
                    if event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    # We ignore the Enter key; progression requires a trailing space.
                    elif event.key == pygame.K_RETURN:
                        pass
                    else:
                        if event.unicode:
                            current_input += event.unicode

            # "Play again?" button click.
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                button_text = "Play again?"
                button_surface = font.render(button_text, True, BLACK)
                button_width = button_surface.get_width() + 20
                button_height = button_surface.get_height() + 10
                button_rect = pygame.Rect(0, 0, button_width, button_height)
                button_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
                if button_rect.collidepoint(event.pos):
                    game_over = False
                    timer_started = False
                    start_time = 0
                    elapsed = 0
                    target_lines = reset_game()
                    current_line_index = 0
                    current_input = ""
                    completed_lines = []
                    result_wpm = 0

        if timer_started and not game_over:
            elapsed = time.time() - start_time
            if elapsed >= time_limit:
                game_over = True
                elapsed = time_limit  # Cap elapsed for display.
                current_target = target_lines[current_line_index] if current_line_index < len(target_lines) else ""
                result_wpm = calculate_wpm(completed_lines, current_target, current_input, elapsed)

        # --- Drawing ---
        # Always draw the full-width timer bar at the top.
        draw_timer_bar(elapsed, time_limit)

        # Only draw passage text if the game is not over.
        if not game_over:
            # Display 4 lines: current line + next 3 (if available)
            line_count = 4
            line_spacing = FONT_SIZE + 10
            base_y = HEIGHT // 2 - (line_count * line_spacing) // 2
            x_start = 20

            for idx in range(line_count):
                line_idx = current_line_index + idx
                if line_idx >= len(target_lines):
                    break
                y = base_y + idx * line_spacing
                if idx == 0:
                    # Current line (with user input)
                    draw_text_line(target_lines[line_idx], current_input, x_start, y)
                else:
                    # Other lines (displayed in white)
                    line_surface = font.render(target_lines[line_idx], True, WHITE)
                    screen.blit(line_surface, (x_start, y))

            # --- Check for Line Completion ---
            current_target_line = target_lines[current_line_index] if current_line_index < len(target_lines) else ""
            # The current line is complete if the input matches exactly and then a trailing space is typed.
            if (current_input.startswith(current_target_line) and 
                len(current_input) > len(current_target_line) and 
                current_input[len(current_target_line)] == " " and 
                current_input[len(current_target_line):].strip() == ""):
                completed_lines.append(current_target_line)
                current_line_index += 1
                current_input = ""
                # If all lines in the passage are complete, load a new passage.
                if current_line_index >= len(target_lines):
                    target_lines = reset_game()
                    current_line_index = 0
                    completed_lines = []

        # --- Game Over Screen ---
        if game_over:
            # When the game is over, the passage text is not drawn.
            result_text = f"{result_wpm} Words per minute"
            result_surface = font.render(result_text, True, WHITE)
            result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            screen.blit(result_surface, result_rect)

            button_text = "Play again?"
            button_surface = font.render(button_text, True, BLACK)
            button_width = button_surface.get_width() + 20
            button_height = button_surface.get_height() + 10
            button_rect = pygame.Rect(0, 0, button_width, button_height)
            button_rect.center = (WIDTH // 2, HEIGHT // 2 + 50)
            pygame.draw.rect(screen, GREEN, button_rect)
            screen.blit(button_surface, (button_rect.x + 10, button_rect.y + 5))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
