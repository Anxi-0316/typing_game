import tkinter as tk
import random
import time

# 題庫
word_list = ["apple", "banana", "cherry", "keyboard", "window"]

# 全域變數
score = 0
current_round = 0
total_round = 5
current_word = ""
time_left = 0
timer_id = None
start_time = 0


# 開始遊戲
def start_game():
    """开始游戏，读取回合数"""
    global score, current_round, total_round, start_time
    try:
        total_round = int(entry_round.get())
        if total_round <= 0:
            total_round = 5  # 最小回合数
    except:
        total_round = 5  # 默认回合数

    score = 0
    current_round = 0
    start_time = time.time()
    btn_start.config(state="disabled")
    next_round()


# 抽下一題
def next_round():
    global current_round, current_word, time_left, timer_id
    entry_word.delete(0, tk.END)
    feedback_label.config(text="")

    if current_round >= total_round:
        end_game()
        return

    current_round += 1
    label_round.config(text=f"Round: {current_round}/{total_round}")

    current_word = random.choice(word_list)
    label_word.config(text=current_word)

    time_left = 10
    update_timer()


# 更新倒數計時
def update_timer():
    global time_left, timer_id
    label_timer.config(text=f"Time: {time_left}s")

    if time_left <= 0:
        feedback_label.config(text=f"Time's up! Correct: {current_word}", fg="red")
        root.after(1000, next_round)
    else:
        time_left -= 1
        timer_id = root.after(1000, update_timer)


# 提交答案
def check_word(event=None):
    global score
    if entry_word.get() == current_word:
        feedback_label.config(text="Correct!", fg="green")
        score += 1
    else:
        feedback_label.config(text=f"Wrong! Correct: {current_word}", fg="red")
    if timer_id:
        root.after_cancel(timer_id)
    root.after(1000, next_round)


# 遊戲結束
def end_game():
    global start_time, timer_id
    # 停掉正在跑的倒數計時
    if timer_id:
        root.after_cancel(timer_id)
        timer_id = None

    total_time = time.time() - start_time
    wpm = score / (total_time / 60)
    label_word.config(text="Game Over!")
    feedback_label.config(text=f"Score: {score}/{total_round}   WPM: {wpm:.2f}")
    btn_start.config(state="normal")


# --- Tkinter UI ---
root = tk.Tk()
root.title("Speed Typing Challenge")
root.geometry("500x400")

tk.Label(root, text="Speed Typing Challenge", font=("Arial", 20)).pack(pady=10)

frame_round = tk.Frame(root)
frame_round.pack()
tk.Label(frame_round, text="Rounds:", font=("Arial", 14)).pack(side="left")
entry_round = tk.Entry(frame_round, width=5, font=("Arial", 14))
entry_round.pack(side="left", padx=5)

btn_start = tk.Button(root, text="Start Game", font=("Arial", 14), command=start_game)
btn_start.pack(pady=10)

label_round = tk.Label(root, text="Round: 0/0", font=("Arial", 14))
label_round.pack(pady=5)

label_word = tk.Label(root, text="", font=("Arial", 24))
label_word.pack(pady=20)

entry_word = tk.Entry(root, font=("Arial", 16))
entry_word.pack(pady=10)
entry_word.bind("<Return>", check_word)

label_timer = tk.Label(root, text="Time: 0s", font=("Arial", 14))
label_timer.pack(pady=5)

feedback_label = tk.Label(root, text="", font=("Arial", 14))
feedback_label.pack(pady=5)

root.mainloop()
