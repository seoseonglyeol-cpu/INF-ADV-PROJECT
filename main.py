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
    "잔액": 10000,           
    "HP": 10,             
    "가방": ["체크카드"],
    "임무": [],
    "수신완료": False,
    "위생수사완료": False
}
final_destination ="이윤재관"
game_settings = {"난이도": None}
environment = {"현재시각": 11}

difficulty_settings={
    "쉬움":1,
    "보통":2,
    "어려움":5
}
#'----------------------------------------------------------------------------------------------------------------'
def save_game():
    save_data = {
        "주인공_상태": {
            "HP": player["HP"],
            "잔액": player["잔액"],
            "가방": player["가방"],
            "배고픔": player["배고픔"],
            "수사완료": player ["수사완료"],
            "위생수사완료": player["위생수사완료"]
        },
        "주인공_위치": {
            "명칭": player["현제위치"],
            "row": player["row"],
            "col": player["col"]
        },
        "임무": player["임무"],
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
            file_path = input("파일 경로를 직접 입력하세요: ") 
        elif 0 < int(choice) <= len(files):
            file_path = files[int(choice)-1]
    else:
        file_path = choice 

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            s = data["주인공_상태"]
            player["HP"], player["잔액"] = s["HP"], s["잔액"]
            player["가방"], player["배고픔"] = s["가방"], s["배고픔"]
            player["수사완료"] = s.get("수사완료", False)
            player["위생수사완료"] = s.get("위생수사완료", False)
            
            w= data['주인공_위치']
            player["현제위치"], player["row"], player["col"] = w["명칭"], w["row"], w["col"]

            player["임무"] = data.get("임무", [])
            game_settings["난이도"] = data.get("난이도", "보통")
            
            global input_log
            input_log = data.get("입력기록", [])

            print(f"\n'{file_path}' 파일을 성공적으로 불러왔습니다!")
            print("게임을 이어서 진행합니다.\n") 


    except FileNotFoundError:
        print(f" 에러: '{file_path}' 파일을 찾을 수 없습니다. 경로를 다시 확인해주세요.")     
    except Exception as e:
        print(f"에러 발생: {e}")

def show_missions():
    print(f"\n[현재 임무 목록]")
    if not player["임무"]:
        print("수행 중인 임무가 없습니다.")
    else:
        for i, mission in enumerate(player["임무"], 1):
            print(f"{i}. {mission}")

def investigation_interaction():
    current_loc = player["현제위치"]
    
    if "교내 부조리 수사" not in player["임무"]:
        print(f"[{current_loc}] 조용한 장소입니다. 별다른 특이사항은 없습니다.")
        return

    if current_loc == "공터1":
        print(f"\n[현장 발견!] {current_loc}에서 부조리 정황을 포착했습니다!")
        print("결정적 증거를 확보했습니다. 이제 이윤재관에 보고하세요.")
        player["수사완료"] = True 
    else:
        print(f"[{current_loc}] 여기는 깨끗합니다. 다른 곳을 수사해보세요.")

def eagle_statue_interaction():
    print(f"\n [독수리상] 앞에 도착했습니다. 신비로운 기운이 느껴집니다.")
    print("수행 가능한 새로운 임무가 있습니다:")
    print("1. 교내 부조리 수사")
    print("2. 이윤재관 보고 임무 받기")

    choice = input("받고 싶은 임무의 번호를 선택하세요: ")

    if choice == '1':
        mission_name = "교내 부조리 수사"
        if mission_name not in player["임무"]:
            player["임무"].append(mission_name)
            print(f">> '{mission_name}' 임무를 받았습니다!")
        else:
            print(">> 이미 수행 중인 임무입니다.")
            
    elif choice == '2':
        mission_name = "이윤재관에 보고하기"
        if mission_name not in player["임무"]:
            player["임무"].append(mission_name)
            print(f"'{mission_name}' 임무를 받았습니다!")
        else:
            print("이미 수행 중인 임무입니다.")

def lee_yoon_jae_interaction():
    print(f"\n [이윤재관]에 도착했습니다.")
    

    if "이윤재관에 보고하기" in player["임무"]:
        print("조교: '오셨군요! 독수리상에서 보낸 보고를 확인했습니다.'")
        print("[임무 완료] 수업을 들을 수 있게 되었습니다!")
        player["임무"].remove("이윤재관에 보고하기") 
    else:
        print("조교: '독수리상에서 임무를 먼저 받고 오세요. 여기서는 그냥 들어올 수 없습니다.'")


    if "교내 부조리 수사" in player["임무"]:
        if player["수사완료"]:
            print("조교: '수고하셨습니다! 공터1의 부조리 보고를 접수했습니다.'")
            print("[임무 완료] 정의를 실현했습니다!")
            player["임무"].remove("교내 부조리 수사") 
        else:
            print("조교: '부조리 수사 임무를 받으셨군요. 증거를 찾아서 다시 오세요'")
    
    if "교내 위생사건 수사" in player["임무"]:
        if player["위생수사완료"]:
            print("조교: '세상에, 상한 우유였다니! 신속한 보고 감사합니다.'")
            print("[임무 완료] 추가 식중독 피해를 막았습니다!")
            player["임무"].remove("교내 위생사건 수사")
        else:
            print("조교: '식중독 사건이 심각합니다. 어서 원인을 찾아와 주세요.'")


    print(f"\n [{final_destination} 511호]에 도착했습니다.") #
    
    has_mission = "이윤재관에 보고하기" in player["임무"]
    
    if has_mission:
        if player["수사완료"] and player["위생수사완료"]:
            print("[MISSION COMPLETE]")
            print("모든 수사 결과를 성공적으로 보고했습니다.")
            print("송도에서 신촌으로의 성공적인 입성을 축하합니다!")
        else:
            print("조교: '수사 임무를 모두 마친 뒤에 보고하러 오세요.'")
    else:
        print("조교: '아직 독수리상에서 받은 공식 임무가 없으시네요.'")

def hygiene_investigation():
    current_loc = player["현제위치"]
    
    if "교내 위생사건 수사" not in player["임무"]:
        return 

    if current_loc == "스타벅스":
        print(f"\n[단서 발견!] {current_loc}의 우유 보관 상태가 엉망입니다!")
        print("상한 우유가 식중독의 원인임을 밝혀냈습니다. 이윤재관에 보고하세요.")
        player["위생수사완료"] = True 
    else:
        print(f"[{current_loc}] 이곳의 위생 상태는 양호합니다. 다른 먹거리 장소를 찾아보세요.")

def trigger_special_event():
    try:
        with open("events.json", "r", encoding="utf-8") as f:
            events = json.load(f)
        
        current_loc = player["현제위치"]
    
        if current_loc in events:
            event = events[current_loc]
            print(f"\n [특별상황 발생!] {event['메시지']}")
            
            for key, value in event["효과"].items():
                player[key] += value
                print(f">> {key}이(가) {value}만큼 변동되었습니다.")
                
    except FileNotFoundError:
        pass

def gate_interaction():
    print(f"\n [정문]에 도착했습니다")
    print("경비원: '독수리상에 가서 임무를 먼저 받고, 나중에 이윤재관으로 보고하러 가세요...'")
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

    r,c = player["row"], player["col"]

    neighbors = {
        "북": (r - 1, c),
        "남": (r + 1, c),
        "서": (r, c - 1),
        "동": (r, c + 1)
    }
    
    print("\n[주변 정보]")
    for direction, (nr, nc) in neighbors.items():
        if 0 <= nr < len(map) and 0 <= nc < len(map[0]):
            target = map[nr][nc]
            if target:
                print(f" {direction}: {target}")
            else:
                print(f" {direction}: (빈 공간)")
        else:
            print(f" {direction}: (막힘)")
    print(f"-----------------------")

def get_action(command):
    작업매핑 = {
        "상태": show_player_status,
        "가방": check_inventory,
        "저장": save_game,
        "불러오기": load_game
    }
    작업 = 작업매핑.get(command)
    return 작업

def get_avaiable_actions(location):

    actions=[]

    if location == '학생회관':
        actions = ["구매", "판매"]
    elif location == "독수리상":
        actions == ["임무 수락"]
    elif location in ["이윤재관", "공터1", "스타벅스"]:
        actions = ["보고", "수사"]
    
    return actions



#'----------------------------------------------------------------------------------------------------------------'

def use_item(item_name):
    if item_name in ["두쫀쿠", "카페라떼"]:
        player["HP"] += 25
        player["가방"].remove(item_name)
        print(f"\n {item_name}을(를) 먹었습니다! HP가 25 만큼 회복되었습니다.")
        print(f"현재 HP: {player['HP']}")
    elif item_name == "체크카드":
        print("\n 체크카드는 결제 시에 '상호작용'을 통해 자동으로 사용됩니다. ")
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
        
    choice = input("\n사용할 물건의 이름이나 번호를 입력하세요 (취소: 0): ")
    if choice =="0":
        return
    selected_item = None

    if choice.isdigit():
        idx= int(choice) -1
        if 0 <= idx <= len(player["가방"]):
            selected_item = player["가방"][idx]
            
    elif choice in player["가방"]:
            selected_item = choice

    if selected_item:
        use_item(selected_item)
    else: 
        print("가방에 그런 물건은 없습니다")
    

#'----------------------------------------------------------------------------------------------------------------'

            
def process_movement(direction):
    global input_log

    r, c = player["row"], player["col"]
    new_row, new_col = r, c

    if direction == '북': new_row -= 1
    elif direction == '남': new_row += 1
    elif direction == '서': new_col -= 1
    elif direction == '동': new_col += 1

    if not (0 <= new_row < len(map) and 0 <= new_col < len(map[0])) or map[new_row][new_col] is None:
        print('>> "그 방향은 막혔어." (다시 입력해주세요)')
        return

    target = map[new_row][new_col]
    player["row"], player["col"] = new_row, new_col
    player["현제위치"] = target

    damage_map = {"쉬움": 1, "보통": 2, "어려움": 3}
    loss = damage_map.get(game_settings.get("난이도", "보통"), 1)
    player["HP"] -= loss

    print(f'\n--- [{target}](으)로 이동 완료 ---')
    print(f"시스템: HP가 {loss} 감소했습니다. (현재 HP: {player['HP']})")

    if target == "공터1" and "교내 부조리 수사" in player["임무"]:
        print(">> [단서 발견] 바닥에 누군가 흘린 듯한 장부가 떨어져 있습니다!")
    elif target == "스타벅스" and "교내 위생사건 수사" in player["임무"]:
        print(">> [단서 발견] 매장 구석에서 유통기한이 지난 우유 팩을 발견했습니다.")

    print("\n[ 주변 상호작용 가능 목록 ]")
    possible_actions = []
    
    if target == "독수리상": possible_actions.append("임무 받기")
    elif target == "이윤재관": possible_actions.append("임무 보고")
    elif target == "학생회관": possible_actions.append("상점 이용")
    elif target == "정문": possible_actions.append("경비원과 대화")
    
    if possible_actions:
        print(f" 수행 가능: {', '.join(possible_actions)}")
        print(" (원하실 경우 '상호작용' 명령어를 입력하세요.)")
    else:
        print(" 가능한 상호작용이 없습니다.")

def move():
    while True:
        command = input('\n명령어를 입력하세요 (북, 남, 서, 동, 상호작용, 가방, 상태, 임무, 저장, 불러오기, 종료): ')
        input_log.append(command)

        match command:
            case "상태":
                show_player_status()
            case "임무":
                show_missions()
            case "가방":
                check_inventory()
            case "저장":
                save_game()
            case "불러오기":
                load_game()
            case "상호작용": 
                curr= player ["현제위치"] 
                if curr == "정문": gate_interaction()
                elif curr == "독수리상": eagle_statue_interaction()
                elif curr == "이윤재관": lee_yoon_jae_interaction()
                elif curr == "학생회관": student_center_shop()
            
                investigation_interaction()
                hygiene_investigation()
                trigger_special_event()

            case "북" | "남" | "서" | "동":
                process_movement(command)
                if player["HP"] <=0:
                    print("\nHP가 0이 되엇습니다. 죽었어욧")
            case "종료":
                break
            case _: print("잘못된 명령입니다")


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


