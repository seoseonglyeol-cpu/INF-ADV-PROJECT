'''
player = {
    "location": "연대앞 버스정류장",
    "hunger": True,
}

'''
#'----------------------------------------------------------------------------------------------------------------'
import os
import json

map= [
    [None, None, None, None, "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스병원"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", None],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", None],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스병원 버스정류장", None, None]
]

input_log=[]

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
environment = {"현재시각": 11}
#'----------------------------------------------------------------------------------------------------------------'
def save_game():
    save_data = {
        "주인공_상태": {
            "HP": player["HP"],
            "잔액": player["잔액"],
            "가방": player["가방"],
            "배고픔": player["배고픔"]
        },
        "주인공_위치": {
            "명칭": player["현제위치"],
            "row": player["row"],
            "col": player["col"]
        },
        "현재시각": environment["현재시각"],
        "난이도": game_settings["난이도"],
        "입력기록": input_log 
    }
    
    with open("savefile.json", "w", encoding="utf-8") as f:
        json.dump(save_data, f, ensure_ascii=False, indent=4)
    print("\n게임 상태가 'savefile.json'에 저장되었습니다.")
    print("게임을 이어서 진행합니다.")

#'----------------------------------------------------------------------------------------------------------------'

def load_game():
    print("\n[불러오기] 모드")
    

    files = [f for f in os.listdir('.') if f.endswith('.json')]
    
    if files:
        print("현재 폴더의 저장된 파일들:")
        for i, f in enumerate(files, 1):
            print(f"{i}. {f}")
        print("0. 경로 직접 입력 (상대경로/절대경로)")
    else:
        print("현재 폴더에 저장된 파일이 없습니다.")
        print("0. 경로 직접 입력")

    choice = input("\n선택 (번호 또는 경로): ")

    file_path = ""
    if choice.isdigit():
        if choice == '0':
            file_path = input("파일 경로를 직접 입력하세요: ") #
        elif 0 < int(choice) <= len(files):
            file_path = files[int(choice)-1]
    else:
        file_path = choice 

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            player["HP"] = data["주인공_상태"]["HP"]
            player["잔액"] = data["주인공_상태"]["잔액"]
            player["가방"] = data["주인공_상태"]["가방"]
            player["배고픔"] = data["주인공_상태"]["배고픔"]
            player["현제위치"] = data["주인공_위치"]["명칭"]
            player["row"] = data["주인공_위치"]["row"]
            player["col"] = data["주인공_위치"]["col"]
            
            environment["현재시각"] = data["현재시각"]
            game_settings["난이도"] = data["난이도"]
            
            global input_log
            input_log = data.get("입력기록", [])

            print(f"\n'{file_path}' 파일을 성공적으로 불러왔습니다!")
            print("게임을 이어서 진행합니다.\n") 
            
    except FileNotFoundError:
        print(f"에러: '{file_path}' 파일을 찾을 수 없습니다.")
    except Exception as e:
        print(f"에러 발생: {e}")

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

#'----------------------------------------------------------------------------------------------------------------'

def use_item(item_name):
    if item_name in ["두쫀쿠", "카페라떼"]:
        player["HP"] += 25
        player["가방"].remove(item_name)
        print(f"\n {item_name}을(를) 먹었습니다! HP가 25 만큼 회복되었습니다.")
        print(f"현재 HP: {player['HP']}")
    else:
        print(f"\n{item_name}은(는) 먹을 수 있는 것이 아닙니다.")


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
        command = input('\n명령어를 입력하세요 (북, 남, 서, 동, 가방, 상태, 저장, 불러오기, 종료): ')
        input_log.append(command)

        if command == "상태":
            show_player_status()
            continue
        elif command == "가방":
            check_inventory()
            continue
        elif command == "불러오기":
            load_game()
            continue
        elif command == "저장": 
            save_game()
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
            target= map[new_row][new_col] 
            if target is None:
                print('그 방향은 없어요')
            else:
                player["row"], player["col"] = new_row, new_col
                player["현제위치"] = target
                player["HP"] -= 1
                print(f'{player["현제위치"]}(으)로 이동. (HP -1)')

                if player["현제위치"] == "학생회관":
                    student_center_shop()
     
                if player["HP"] <= 0:
                    print("\n HP가 0이 되었습니다. 쓰러졌습니다...")
                    break
        else:
            print('그 방향은 막혔어.')


#'----------------------------------------------------------------------------------------------------------------'

def set_difficulty():
    print("--- 난이도 설정 ---")
    print("1. 쉬움")
    print("2. 보통")
    print("3. 어려움")
    choice = input("원하는 난이도의 번호를 선택하세요: ")
    diff = {"1":"쉬움", "2":"보통", "3": "어려움"}
    game_settings["난이도"] = diff.get(choice, "보통")
    print(f"\n 현재 난이도: {game_settings['난이도']}")


#'----------------------------------------------------------------------------------------------------------------'

#'----------------------------------------------------------------------------------------------------------------'


#'----------------------------------------------------------------------------------------------------------------'

set_difficulty()
move()

#'----------------------------------------------------------------------------------------------------------------'



#'----------------------------------------------------------------------------------------------------------------'


