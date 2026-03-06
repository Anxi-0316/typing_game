import tkinter as tk
import random
import time

# ----------------------------
# 题库与时间设置
# ----------------------------
WORD_BANK = {
    "Normal": [
        "apple",
        "banana",
        "cherry",
        "orange",
        "grape",
        "window",
        "mouse",
        "chair",
        "school",
        "pencil",
    ],
    "Hard": [
        "keyboard",
        "monitor",
        "internet",
        "python",
        "library",
        "function",
        "variable",
        "computer",
        "programming",
        "challenge",
    ],
    "Nightmare": [
        "extraordinary",
        "configuration",
        "communication",
        "development",
        "matplotlib",
        "architecture",
        "implementation",
        "sophisticated",
        "responsibility",
        "environment",
    ],
}

TIME_LIMIT = {"Normal": 10, "Hard": 8, "Nightmare": 6}

# ----------------------------
# 全域变数
# ----------------------------
score = 0
current_round = 0
total_round = 5
current_word = ""
time_left = 0
timer_id = None
start_time = 0
difficulty = "Normal"
game_running = False


# ----------------------------
# 功能函数
# ----------------------------
def set_difficulty(level):
    global difficulty
    difficulty = level
    difficulty_label.config(text=f"Difficulty: {difficulty}")


def start_game():
    global score, current_round, total_round, start_time, game_running

    try:
        total_round = int(entry_round.get())
        if total_round <= 0:
            total_round = 5
    except ValueError:
        total_round = 5

    score = 0
    current_round = 0
    start_time = time.time()
    game_running = True

    btn_start.config(state="disabled")
    entry_round.config(state="disabled")
    entry_word.config(state="normal")
    entry_word.delete(0, tk.END)
    entry_word.focus()

    result_label.config(text="")
    wpm_label.config(text="WPM: 0.00")
    score_label.config(text=f"Score: {score}/{total_round}")

    next_round()


def next_round():
    global current_round, current_word, time_left, timer_id

    if timer_id:
        root.after_cancel(timer_id)

    entry_word.delete(0, tk.END)
    result_label.config(text="")

    if current_round >= total_round:
        end_game()
        return

    current_round += 1
    round_label.config(text=f"Round: {current_round}/{total_round}")

    current_word = random.choice(WORD_BANK[difficulty])
    display_word_feedback("")

    time_left = TIME_LIMIT[difficulty]
    update_timer()


def update_timer():
    global time_left, timer_id

    timer_label.config(text=f"Time: {time_left}s")

    if time_left <= 0:
        result_label.config(text=f"Time's up! Correct word: {current_word}", fg="red")
        timer_id = root.after(1200, next_round)
    else:
        time_left -= 1
        timer_id = root.after(1000, update_timer)


def display_word_feedback(typed):
    """
    在题目显示区逐字变色：
    - 正确字母：绿色
    - 第一个错误位置：红色
    - 后面未输入或未比较：黑色
    """
    text_word.config(state="normal")
    text_word.delete("1.0", tk.END)

    error_found = False

    for i, ch in enumerate(current_word):
        color = "black"

        if i < len(typed):
            if not error_found:
                if typed[i] == ch:
                    color = "green"
                else:
                    color = "red"
                    error_found = True
            else:
                color = "black"

        text_word.insert(tk.END, ch, color)

    text_word.tag_config("green", foreground="green")
    text_word.tag_config("red", foreground="red")
    text_word.tag_config("black", foreground="black")
    text_word.config(state="disabled")


def on_typing(event=None):
    typed = entry_word.get()
    display_word_feedback(typed)


def submit_word(event=None):
    global score, timer_id

    if not game_running:
        return

    typed = entry_word.get().strip()

    if timer_id:
        root.after_cancel(timer_id)

    if typed == current_word:
        score += 1
        result_label.config(text="Correct!", fg="green")
    else:
        result_label.config(text=f"Wrong! Correct: {current_word}", fg="red")

    score_label.config(text=f"Score: {score}/{total_round}")

    root.after(1000, next_round)


def end_game():
    global game_running, timer_id

    game_running = False
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

    total_time = max(time.time() - start_time, 1)
    wpm = score / (total_time / 60)

    text_word.config(state="normal")
    text_word.delete("1.0", tk.END)
    text_word.insert(tk.END, "Game Over")
    text_word.config(state="disabled")

    round_label.config(text="Finished")
    timer_label.config(text=f"Total Time: {total_time:.1f}s")
    result_label.config(text=f"Final Score: {score}/{total_round}", fg="green")
    wpm_label.config(text=f"WPM: {wpm:.2f}")

    entry_word.delete(0, tk.END)
    entry_word.config(state="disabled")

    btn_start.config(state="normal")
    entry_round.config(state="normal")


# ----------------------------
# UI
# ----------------------------
root = tk.Tk()
root.title("Speed Typing Challenge")
root.geometry("600x450")
root.resizable(False, False)

title_label = tk.Label(root, text="Speed Typing Challenge", font=("Arial", 20, "bold"))
title_label.pack(pady=10)

top_frame = tk.Frame(root)
top_frame.pack(pady=5)

tk.Label(top_frame, text="Rounds:", font=("Arial", 12)).pack(side="left", padx=5)
entry_round = tk.Entry(top_frame, width=6, font=("Arial", 12), justify="center")
entry_round.insert(0, "5")
entry_round.pack(side="left", padx=5)

difficulty_label = tk.Label(root, text="Difficulty: Normal", font=("Arial", 12, "bold"))
difficulty_label.pack(pady=5)

difficulty_frame = tk.Frame(root)
difficulty_frame.pack(pady=5)

btn_normal = tk.Button(
    difficulty_frame, text="Normal", width=10, command=lambda: set_difficulty("Normal")
)
btn_hard = tk.Button(
    difficulty_frame, text="Hard", width=10, command=lambda: set_difficulty("Hard")
)
btn_nightmare = tk.Button(
    difficulty_frame,
    text="Nightmare",
    width=10,
    command=lambda: set_difficulty("Nightmare"),
)

btn_normal.grid(row=0, column=0, padx=5)
btn_hard.grid(row=0, column=1, padx=5)
btn_nightmare.grid(row=0, column=2, padx=5)

btn_start = tk.Button(
    root, text="Start Game", font=("Arial", 12, "bold"), command=start_game
)
btn_start.pack(pady=10)

round_label = tk.Label(root, text="Round: 0/0", font=("Arial", 12))
round_label.pack(pady=5)

timer_label = tk.Label(root, text="Time: 0s", font=("Arial", 12))
timer_label.pack(pady=5)

# 题目显示区（逐字变色）
text_word = tk.Text(root, height=2, width=20, font=("Consolas", 22, "bold"), bd=0)
text_word.pack(pady=15)
text_word.insert(tk.END, "Press Start")
text_word.config(state="disabled")

# 输入框
entry_word = tk.Entry(
    root, font=("Consolas", 16), width=20, justify="center", state="disabled"
)
entry_word.pack(pady=10)
entry_word.bind("<KeyRelease>", on_typing)
entry_word.bind("<Return>", submit_word)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack(pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=15)

score_label = tk.Label(bottom_frame, text="Score: 0/0", font=("Arial", 12, "bold"))
score_label.grid(row=0, column=0, padx=20)

wpm_label = tk.Label(bottom_frame, text="WPM: 0.00", font=("Arial", 12, "bold"))
wpm_label.grid(row=0, column=1, padx=20)

hint_label = tk.Label(root, text="Type the word and press Enter", font=("Arial", 10))
hint_label.pack(pady=5)

root.mainloop()
