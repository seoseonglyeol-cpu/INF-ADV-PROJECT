player = {
    "location": "연대앞 버스정류장",
    "hunger": True,
}

environment = {
    "time": 11,
}

map= [
    ["공학관", "백양로1", "백주년기념관"],
    ["공학원", "백양로1", "공터1"],
    ["연대앞 버스정류장", "정문", "세브란스병원/버스정류장"]
]

row, col = 2, 0

def move_action():
    global row, col
    
    while True:
        print(f"\n현재 위치: {map[row][col]}")
        direction = input("이동 방향을 입력하세요 (동, 서, 남, 북): ")
        
        # 이동 시도할 가상 좌표
        new_row, new_col = row, col
        
        if direction == "북":
            new_row -= 1
        elif direction == "남":
            new_row += 1
        elif direction == "서":
            new_col -= 1
        elif direction == "동":
            new_col += 1
        else:
            print("올바른 방향을 입력하세요.")
            continue

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            row, col = new_row, new_col
            print(f"{map[row][col]}(으)로 이동했습니다.")
            break 
        else:
            print("그 방향은 막혔어요.")

move_action()