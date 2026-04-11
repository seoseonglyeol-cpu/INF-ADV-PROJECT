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
    "col": 0,
    "잔액": 50000,           
    "HP": 10,             
    "가방": ["체크카드"]  
}

game_settings = {"난이도": None}

#'----------------------------------------------------------------------------------------------------------------'

def student_center_shop():
    print(f"\n[학생회관 상점]에 입성했습니다!")
    print(f"현재 잔액: {player['잔액']}원")
    print("1. 두쫀쿠 (5,000원) - HP 25 회복")
    print("2. 카페라떼 (2,500원) - HP 25 회복")
    print("0. 나가기")

    choice = input("구매할 물건을 선택하세요: ")

    if choice == '1':
        price = 5000
        if player["잔액"] >= price:
            player["잔액"] -= price
            player["가방"].append("두쫀쿠")
            print(">> 두쫀쿠를 구매하여 가방에 넣었습니다.")
        else:
            print(">> 잔액이 부족합니다.")
    elif choice == '2':
        price = 2500
        if player["잔액"] >= price:
            player["잔액"] -= price
            player["가방"].append("카페라떼")
            print(">> 카페라떼를 구매하여 가방에 넣었습니다.")
        else:
            print(">> 잔액이 부족합니다.")

#'----------------------------------------------------------------------------------------------------------------'

def show_player_status():
    print(f"\n--- 현재 주인공 상태 ---")
    print(f"계좌 잔액: {player['잔액']}원")
    print(f"HP: {player['HP']} / 10")
    print(f"위치: {player['현제위치']}")
    print(f"-----------------------")

show_player_status()

#'----------------------------------------------------------------------------------------------------------------'
def check_inventory():
    print(f"\n[가방 안의 물건들]")
    if not player["가방"]:
        print("가방이 비어 있습니다.")
    else:
        for i, item in enumerate(player["가방"], 1):
            print(f"{i}. {item}")
        
        choice = input("\n사용할 물건의 이름이나 번호를 입력하세요 (취소: 0): ")
        if choice != '0':
            print(f"{choice}은(는) 지금 사용할 수 없습니다.")

#'----------------------------------------------------------------------------------------------------------------'
def move():
    while True:
        command = input('\n명령어를 입력하세요 (북, 남, 서, 동, 가방, 상태, 종료): ')

        if command == "상태":
            show_player_status()
            continue
        elif command == "가방":
            check_inventory()
            continue
        elif command == "종료":
            break
        r, c = player["row"], player["col"]
        new_row, new_col = r, c

        if command == '북': new_row -= 1
        elif command == '남': new_row += 1
        elif command == '서': new_col -= 1
        elif command == '동': new_col += 1
        else:
            print("올바른 명령어를 입력하세요.")
            continue

        if 0 <= new_row < len(map) and 0 <= new_col < len(map[0]):
            if map[new_row][new_col] == "":
                print("그곳은 갈 수 없는 빈터야.")
            else:
                player["row"], player["col"] = new_row, new_col
                player["현제위치"] = map[new_row][new_col]

                if player["현제위치"] == "학생회관":
                    student_center_shop()
    
                
                player["HP"] -= 1
                print(f'>> {player["현제위치"]}(으)로 이동 완료. (HP 1 감소)')
                
                if player["HP"] <= 0:
                    print("\n HP가 0이 되었습니다. 쓰러졌습니다...")
                    break
        else:
            print('그 방향은 막혔어.')

move()

#'----------------------------------------------------------------------------------------------------------------'

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


#'----------------------------------------------------------------------------------------------------------------'
def use_item(item_name):
    recovery = 25
    
    if item_name in ["두쫀쿠", "카페라떼"]:
        player["HP"] += recovery
        player["가방"].remove(item_name)
        print(f"\n {item_name}을(를) 먹었습니다! HP가 {recovery}만큼 회복되었습니다.")
        print(f"현재 HP: {player['HP']}")
    else:
        print(f"\n{item_name}은(는) 먹을 수 있는 것이 아닙니다.")

#'----------------------------------------------------------------------------------------------------------------'

def check_inventory():
    print(f"\n[가방 안의 물건들]")
    if not player["가방"]:
        print("가방이 비어 있습니다.")
        return

    for i, item in enumerate(player["가방"], 1):
        print(f"{i}. {item}")
    
    choice = input("\n사용할 물건 번호를 입력하세요 (취소: 0): ")
    if choice.isdigit() and 0 < int(choice) <= len(player["가방"]):
        selected_item = player["가방"][int(choice)-1]
        use_item(selected_item)


#'----------------------------------------------------------------------------------------------------------------'

set_difficulty()
move()

#'----------------------------------------------------------------------------------------------------------------'



#'----------------------------------------------------------------------------------------------------------------'


