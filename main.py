import os
import json
import pickle

map = [
    ["종합관", "본관", "경영관", "노천극장", "새천년관", "이윤재관"],
    ["백양관", "백양로5", "대강당", "음악관", "알렌관", "ABMRC"],
    ["중앙도서관", "독수리상", "학생회관", "루스채플", "재활병원", "치과대학"],
    ["체육관", "백양로3", "공터2", "광혜원", "어린이병원", "세브란스병원"],
    ["공학관", "백양로2", "백주년기념관", "안과병원", "제중관", None],
    ["공학원", "백양로1", "공터1", "암병원", "의과대학", None],
    ["연대앞 버스정류장", "정문", "스타벅스", "세브란스병원 버스정류장", None, None]
]

input_log = []
game_settings = {"난이도": None}
environment = {"현재시각": 11}
quest_config = {"events": {}, "answers": {}}

def load_quest_config(path="quest_config.pkl"):
    global quest_config
    try:
        with open(path, "rb") as f:
            quest_config = pickle.load(f)
    except FileNotFoundError:
        print(f"경고: '{path}' 파일을 찾을 수 없습니다.")

load_quest_config()
#'----------------------------------------------------------------------------------------------------------------'

class Quest:
    def __init__(self, 이름, 설명):
        self.이름 = 이름
        self.설명 = 설명

class Place:
    def __init__(self, 이름, *, 구매=None, 판매=None, 사건정보=None,
                 임무_받기=None, 임무_해결=None, 도착_이벤트=None):
        self.이름       = 이름
        self.구매       = 구매 or []
        self.판매       = 판매 or []
        self.사건정보   = 사건정보 or {}
        self.임무_받기  = 임무_받기 or []
        self.임무_해결  = 임무_해결
        self.도착_이벤트 = 도착_이벤트

    def 도착(self, player):
        if self.도착_이벤트:
            self.도착_이벤트(player)
        for 조건, 메시지 in self.사건정보.items():
            if 조건 is None or 조건 in player.임무:
                print(메시지)
        가능 = self.가능한_상호작용()
        if 가능:
            print(f"[상호작용 가능] {', '.join(가능)}")

    def 상호작용(self, player):
        게임종료 = False
        if self.임무_해결:
            게임종료 = self.임무_해결(player)
        if self.구매:
            _상점(self.이름, self.구매)
        if self.판매:
            _판매_상점(self.판매)
        if self.임무_받기:
            self._임무_받기_처리(player)
        return 게임종료

    def _임무_받기_처리(self, player):
        print(f"\n[{self.이름}] 받을 수 있는 임무:")
        for i, q in enumerate(self.임무_받기, 1):
            print(f"{i}. {q.이름}: {q.설명}")
        choice = input("번호를 선택하세요 (0: 취소): ")
        if choice == '0' or not choice.isdigit():
            return
        idx = int(choice) - 1
        if not (0 <= idx < len(self.임무_받기)):
            print("잘못된 선택입니다.")
            return
        q = self.임무_받기[idx]
        if q.이름 in player.임무:
            print(">> 이미 수행 중인 임무입니다.")
        else:
            player.임무.append(q.이름)
            print(f">> '{q.이름}' 임무를 받았습니다!")

    def 가능한_상호작용(self):
        가능 = []
        if self.구매:       가능.append("구매")
        if self.판매:       가능.append("판매")
        if self.임무_받기:  가능.append("임무")
        if self.임무_해결:  가능.append("보고/해결")
        return 가능

class Player:
    def __init__(self):
        self.배고픔 = True
        self.현제위치 = "연대앞 버스정류장"
        self.row = 6
        self.col = 0
        self.잔액 = 10000
        self.HP = 10
        self.가방 = ["체크카드"]
        self.임무 = []
        self.수사완료 = False
        self.위생수사완료 = False

    def move(self, direction):
        delta = {"북": (-1, 0), "남": (1, 0), "서": (0, -1), "동": (0, 1)}
        dr, dc = delta[direction]
        new_row, new_col = self.row + dr, self.col + dc

        if not (0 <= new_row < len(map) and 0 <= new_col < len(map[0])) or map[new_row][new_col] is None:
            print('>> "그 방향은 막혔어." (다시 입력해주세요)')
            return False

        damage = {"보통": 1, "어려움": 2}.get(game_settings.get("난이도"), 1)
        self.row, self.col = new_row, new_col
        self.현제위치 = map[new_row][new_col]
        self.HP -= damage
        return True

    def print_status(self):
        print(f"\n--- 현재 주인공 상태 ---")
        print(f"계좌 잔액: {self.잔액}원")
        print(f"HP: {self.HP} / 10")
        print(f"위치: {self.현제위치}")
        print(f"-----------------------")

        r, c = self.row, self.col
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

player = Player()
final_destination = "이윤재관"

#'----------------------------------------------------------------------------------------------------------------'

def save_game():
    save_data = {
        "주인공_상태": {
            "HP": player.HP,
            "잔액": player.잔액,
            "가방": player.가방,
            "배고픔": player.배고픔,
            "수사완료": player.수사완료,
            "위생수사완료": player.위생수사완료
        },
        "주인공_위치": {
            "명칭": player.현제위치,
            "row": player.row,
            "col": player.col
        },
        "임무": player.임무,
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
            player.HP, player.잔액 = s["HP"], s["잔액"]
            player.가방, player.배고픔 = s["가방"], s["배고픔"]
            player.수사완료 = s.get("수사완료", False)
            player.위생수사완료 = s.get("위생수사완료", False)

            w = data['주인공_위치']
            player.현제위치, player.row, player.col = w["명칭"], w["row"], w["col"]

            player.임무 = data.get("임무", [])
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
    if not player.임무:
        print("수행 중인 임무가 없습니다.")
    else:
        for i, mission in enumerate(player.임무, 1):
            print(f"{i}. {mission}")

def trigger_special_event():
    try:
        with open("events.json", "r", encoding="utf-8") as f:
            events = json.load(f)
        current_loc = player.현제위치
        if current_loc in events:
            event = events[current_loc]
            print(f"\n[특별상황 발생!] {event['메시지']}")
            for key, value in event["효과"].items():
                setattr(player, key, getattr(player, key) + value)
                print(f">> {key}이(가) {value}만큼 변동되었습니다.")
    except FileNotFoundError:
        pass

#'----------------------------------------------------------------------------------------------------------------'

def _정문_도착(player):
    print("경비원: '학교에서 어떤 일들이 일어나고있는지 소식들이 모이는 독수리상에서 알아보자.'")
    mission = "독수리상 방문"
    if mission not in player.임무:
        player.임무.append(mission)
        print(f">> '{mission}' 임무를 받았습니다!")

def _독수리상_방문_해결(player):
    if "독수리상 방문" in player.임무:
        player.임무.remove("독수리상 방문")
        print("[임무 완료] 독수리상 방문!")
    return False

def _본관_해결(player):
    if "교내 부조리 수사" not in player.임무:
        print("특별한 용무가 없습니다.")
        return False
    answer = input("교내 어디에 부조리가 있나? ").strip()
    correct = quest_config["answers"].get("교내 부조리 수사", "")
    if answer == correct:
        player.임무.remove("교내 부조리 수사")
        player.수사완료 = True
        print(f"담당자: '{correct}이군요! 즉시 처리하겠습니다.'")
        print("[임무 완료] 수업들으러 이윤재관 가야지!")
    else:
        print("담당자: '확실하지 않네요. 다시 조사해보세요.'")
    return False

def _세브란스_해결(player):
    if "교내 위생사건 수사" not in player.임무:
        print("특별한 용무가 없습니다.")
        return False
    answer = input("교내 어디에 식중독 원인이 있나? ").strip()
    correct = quest_config["answers"].get("교내 위생사건 수사", "")
    if answer == correct:
        player.임무.remove("교내 위생사건 수사")
        player.위생수사완료 = True
        print(f"의사: '{correct}의 문제군요! 즉시 조치하겠습니다.'")
        print("[임무 완료] 수업들으러 이윤재관 가야지!")
    else:
        print("의사: '확실하지 않네요. 다시 조사해보세요.'")
    return False

def _이윤재관_해결(player):
    if player.수사완료 and player.위생수사완료:
        print("교수님: '부조리와 식중독 수사를 완료했구나! 수업은 이걸로 끝입니다. 또 만나요~'")
        return True
    elif player.수사완료:
        print("교수님: '부조리 수사를 완료했구나! 식중독 원인도 찾아주세요~'")
    elif player.위생수사완료:
        print("교수님: '식중독 수사를 완료했구나! 부조리도 찾아주세요~'")
    else:
        print("교수님: '아직 수사가 남아있어요. 다 끝내고 오세요!'")
    return False

#'----------------------------------------------------------------------------------------------------------------'

def _상점(상점명, 메뉴):
    print(f"\n[{상점명}]")
    print(f"현재 잔액: {player.잔액}원")
    for i, (이름, 가격, _) in enumerate(메뉴, 1):
        print(f"{i}. {이름} ({가격:,}원)")
    print("0. 나가기")
    choice = input("구매할 물건을 선택하세요: ")
    if choice == '0' or not choice.isdigit():
        return
    idx = int(choice) - 1
    if not (0 <= idx < len(메뉴)):
        print(">> 잘못된 선택입니다.")
        return
    이름, 가격, _ = 메뉴[idx]
    if player.잔액 < 가격:
        print(">> 잔액이 부족합니다.")
        return
    player.잔액 -= 가격
    player.가방.append(이름)
    print(f">> {이름}을(를) 구매하여 가방에 넣었습니다.")

판매_그룹1 = {"체육관", "공학관", "공학원", "재활병원", "어린이병원", "종합관", "노천극장"}
판매_그룹2 = {"중앙도서관", "백양관", "대강당", "백주년기념관", "안과병원", "암병원",
             "새천년관", "알렌관", "제중관", "의과대학", "치과대학", "세브란스병원",
             "본관", "경영관"}

def _판매_상점(메뉴):
    판매_가능 = [item for item in player.가방 if item in {이름 for 이름, _, _ in 메뉴}]
    if not 판매_가능:
        print(">> 판매할 수 있는 물건이 없습니다.")
        return
    메뉴_맵 = {이름: (가격, hp) for 이름, 가격, hp in 메뉴}
    print(f"\n[판매] 현재 잔액: {player.잔액}원")
    for i, item in enumerate(판매_가능, 1):
        가격, hp = 메뉴_맵[item]
        print(f"{i}. {item} → {가격:,}원 + HP +{hp}")
    print("0. 나가기")
    choice = input("판매할 물건을 선택하세요: ")
    if choice == '0' or not choice.isdigit():
        return
    idx = int(choice) - 1
    if not (0 <= idx < len(판매_가능)):
        print(">> 잘못된 선택입니다.")
        return
    item = 판매_가능[idx]
    가격, hp = 메뉴_맵[item]
    player.가방.remove(item)
    player.잔액 += 가격
    player.HP += hp
    print(f">> {item}을(를) {가격:,}원에 판매했습니다. HP +{hp}")
    print(f"현재 잔액: {player.잔액}원 / HP: {player.HP}")

#'----------------------------------------------------------------------------------------------------------------'

PLACES = {
    "정문": Place("정문", 도착_이벤트=_정문_도착),
    "독수리상": Place("독수리상",
        임무_받기=[
            Quest("교내 부조리 수사", "교내 어딘가에서 부조리가 일어나고있다. 공터1 탐색 → 본관에 보고"),
            Quest("교내 위생사건 수사", "학생들이 단체로 식중독에 걸렸다. 스타벅스 탐색 → 세브란스병원에 보고"),
        ],
        임무_해결=_독수리상_방문_해결),
    "이윤재관": Place("이윤재관", 임무_해결=_이윤재관_해결),
    "본관": Place("본관",
        판매=[("두쫀쿠", 6000, 10), ("카페라떼", 3000, 5)],
        임무_해결=_본관_해결),
    "세브란스병원": Place("세브란스병원",
        판매=[("두쫀쿠", 6000, 10), ("카페라떼", 3000, 5)],
        임무_해결=_세브란스_해결),
    "학생회관": Place("학생회관",
        구매=[("두쫀쿠", 5000, 10), ("카페라떼", 3000, 5)]),
    "스타벅스": Place("스타벅스",
        구매=[("두쫀쿠", 4000, 10), ("카페라떼", 2000, 5)]),
    "ABMRC": Place("ABMRC",
        구매=[("두쫀쿠", 4000, 10), ("카페라떼", 2000, 5)]),
    "중앙도서관": Place("중앙도서관",
        판매=[("두쫀쿠", 6000, 10), ("카페라떼", 3000, 5)],
        사건정보={None: "빌런이 키오스크 배석 자리를 짐으로 차지하고 비켜주지 않고 있습니다."}),
    "공터2": Place("공터2",
        사건정보={None: "학생회관에서 버린 음식물쓰레기가 부패하여 학생회관으로 흘러들어가고 있습니다!"}),
}
for _장소 in 판매_그룹1:
    PLACES[_장소] = Place(_장소, 판매=[("두쫀쿠", 7000, 10), ("카페라떼", 4000, 5)])
for _장소 in 판매_그룹2:
    if _장소 not in PLACES:
        PLACES[_장소] = Place(_장소, 판매=[("두쫀쿠", 6000, 10), ("카페라떼", 3000, 5)])

for _quest, _장소 in quest_config.get("answers", {}).items():
    _메시지 = quest_config.get("events", {}).get(_장소)
    if _메시지:
        if _장소 not in PLACES:
            PLACES[_장소] = Place(_장소)
        PLACES[_장소].사건정보[_quest] = f"[단서] {_메시지}"

#'----------------------------------------------------------------------------------------------------------------'

def use_item(item_name):
    아이템_효과 = {"두쫀쿠": 10, "카페라떼": 5}
    if item_name in 아이템_효과:
        hp = 아이템_효과[item_name]
        player.HP += hp
        player.가방.remove(item_name)
        print(f"\n{item_name}을(를) 먹었습니다! HP가 {hp} 만큼 회복되었습니다.")
        print(f"현재 HP: {player.HP}")
    elif item_name == "체크카드":
        print("\n 체크카드는 결제 시에 '상호작용'을 통해 자동으로 사용됩니다. ")
    else:
        print(f"\n{item_name}은(는) 먹을 수 있는 것이 아닙니다.")

#'----------------------------------------------------------------------------------------------------------------'

def check_inventory():
    print(f"\n[가방 안의 물건들]")
    if not player.가방:
        print("가방이 비어 있습니다.")
        return
    for i, item in enumerate(player.가방, 1):
        print(f"{i}. {item}")
    choice = input("\n사용할 물건의 이름이나 번호를 입력하세요 (취소: 0): ")
    if choice == "0":
        return
    selected_item = None
    if choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(player.가방):
            selected_item = player.가방[idx]
    elif choice in player.가방:
        selected_item = choice
    if selected_item:
        use_item(selected_item)
    else:
        print("가방에 그런 물건은 없습니다")

#'----------------------------------------------------------------------------------------------------------------'

def 입력_받기():
    command = input('\n명령어를 입력하세요 (북, 남, 서, 동, 상호작용, 가방, 상태, 임무, 저장, 불러오기, 종료): ')
    input_log.append(command)
    return command

def _빈_효과():
    return {"종료": False, "이동됨": False}

def _이동_작업(direction):
    def 작업():
        효과 = _빈_효과()
        if player.move(direction):
            효과["이동됨"] = True
        return 효과
    return 작업

def _상태_작업():
    player.print_status()
    return _빈_효과()

def _임무_작업():
    show_missions()
    return _빈_효과()

def _가방_작업():
    check_inventory()
    return _빈_효과()

def _저장_작업():
    save_game()
    return _빈_효과()

def _불러오기_작업():
    load_game()
    return _빈_효과()

def _상호작용_작업():
    place = PLACES.get(player.현제위치)
    게임_종료 = place.상호작용(player) if place else False
    효과 = _빈_효과()
    효과["종료"] = 게임_종료
    return 효과

def _종료_작업():
    효과 = _빈_효과()
    효과["종료"] = True
    return 효과

def _알_수_없는_명령():
    print("잘못된 명령입니다")
    return _빈_효과()

def 입력에_따른_작업을_설정하기(command):
    작업_맵 = {
        "북":       _이동_작업("북"),
        "남":       _이동_작업("남"),
        "서":       _이동_작업("서"),
        "동":       _이동_작업("동"),
        "상태":     _상태_작업,
        "임무":     _임무_작업,
        "가방":     _가방_작업,
        "저장":     _저장_작업,
        "불러오기": _불러오기_작업,
        "상호작용": _상호작용_작업,
        "종료":     _종료_작업,
    }
    return 작업_맵.get(command, _알_수_없는_명령)

def 결과를_상태에_반영(효과):
    if 효과["종료"]:
        return True

    if 효과["이동됨"]:
        target = player.현제위치
        print(f'\n현재위치: {target}')
        print(f"HP: {player.HP}")
        trigger_special_event()
        place = PLACES.get(target)
        if place:
            place.도착(player)

    if player.HP <= 0:
        print("\nHP가 0이 되었습니다. 게임 오버!")
        return True

    return False

def game_loop():
    종료 = False
    while not 종료:
        사용자의_입력 = 입력_받기()
        작업           = 입력에_따른_작업을_설정하기(사용자의_입력)
        결과           = 작업()
        종료           = 결과를_상태에_반영(결과)

#'----------------------------------------------------------------------------------------------------------------'

def set_difficulty():
    print("--- 난이도 설정 ---")
    print("1. 쉬움")
    print("2. 보통")
    print("3. 어려움")
    choice = input("원하는 난이도의 번호를 선택하세요: ")
    diff = {"1": "쉬움", "2": "보통", "3": "어려움"}
    game_settings["난이도"] = diff.get(choice, "보통")
    print(f"\n 현재 난이도: {game_settings['난이도']}")

#'----------------------------------------------------------------------------------------------------------------'

set_difficulty()
game_loop()
