'''
player = {
    "location": "연대앞 버스정류장",
    "hunger": True,
}

environment = {
    "time": 11,
}
'''
#'----------------------------------------------------------------------------------------------------------------'

'''
map= [
    ["공학관", "백양로1", "백주년기념관"],
    ["공학원", "백양로1", "공터1"],
    ["연대앞 버스정류장", "정문", "세브란스병원/버스정류장"]
]

row, col = 2, 0
'''
map= [
    [None, None, None, None, "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스병원"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", None],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", None],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스병원 버스정류장", None, None]
]


player = {
    "배고픔": True,
    "현제위치": "연대앞 버스정류장",
    "row": 6,  
    "col": 0   
}


def move():
    while True:
        r, c = player["row"], player["col"]
        print(f'\n--- 현재 위치: {map[r][c]} ---')
        
        direction = input('이동할 방향을 입력하세요 (북, 남, 서, 동 / 종료: q): ')
        
        if direction == 'q':
            break
            
        new_row, new_col = r, c
        
        if direction == '북':
            new_row -= 1
        elif direction == '남':
            new_row += 1
        elif direction == '서':
            new_col -= 1
        elif direction == '동':
            new_col += 1
        else:
            print('잘못된 입력입니다.')
            continue
    
        if 0 <= new_row < len(map) and 0 <= new_col < len(map[0]):
            if map[new_row][new_col] == "":
                print("그곳은 갈 수 없는 빈터야.")
            else:
                player["row"], player["col"] = new_row, new_col
                player["현제위치"] = map[new_row][new_col]
                print(f'>> {player["현제위치"]}(으)로 이동 완료.')
        else:
            print('그 방향은 막혔어.')

move()
'''
def move_action():
    global row, col
    
    while True:
        print(f"\n현재 위치: {map[row][col]}")
        direction = input("이동 방향을 입력하세요 (동, 서, 남, 북): ")
        

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
'''

#'----------------------------------------------------------------------------------------------------------------'

game_settings = {
    "난이도": None
}

def set_difficulty():
    print("--- 난이도 설정 ---")
    print("1. 쉬움")
    print("2. 보통")
    print("3. 어려움")
    
    while True:
        choice = input("원하는 난이도의 번호를 선택하세요: ")
        
        if choice == '1':
            game_settings["난이도"] = "쉬움"
            break
        elif choice == '2':
            game_settings["난이도"] = "보통"
            break
        elif choice == '3':
            game_settings["난이도"] = "어려움"
            break
        else:
            print("잘못된 입력입니다. 1, 2, 3 중에서 선택해주세요.")

    print(f"\n 현재 난이도: {game_settings['난이도']}")

set_difficulty()