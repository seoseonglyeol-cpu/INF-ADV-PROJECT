player={
    "배고픔": True,
    "현제위치": "연대앞 버스정류장"
    
}

environment={
    "현재시각": 11
}

print("---주인공 상태---")
print(f'배고픔: {player["배고픔"]}')
print(f'현재 위치: {player["현제위치"]}')
print(f'현재 시각: {environment["현재시각"]}시')


map=[
    ["공학관", "백양로1", "백주년기념관"],
    ["공학원", "백양로", "공터1"],
    ["연대앞 버스정류장", "정문", "세브란스병원"]
]

def move():
    while True:
        r, c = player["row"], player["col"]
        print(f'현재 위치: {map[r][c]}')
        direction = input('이동할 방향을 입력하세요 (w: 위, s: 아래, a: 왼쪽, d: 오른쪽): ')
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
            print('잘못된 입력입니다. 다시 시도하세요.')
            continue
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            player["row"], player["col"] = new_row, new_col
            print(f'이동 완료. 현재 위치: {map[new_row][new_col]}')
            break
        else:
            print('이동할 수 없는 방향입니다. 다시 시도하세요.')

'''

player={
    "배고픔": True,
    "현제위치": "연대앞 버스정류장",
    "row": 2,
    "col": 0
}

#tiempo y hora
environment={
    "현재시각": 11
}

#nivel del juego
settings={
    "난이도": None
}
'''
#nivel del juego
def set_difficulty():
    while True:
        print('난이도를 선택하세요:')
        print('1. 쉬움')
        print('2. 보통')
        print('3. 어려움')
        choice = input('선택: ')
        if choice == '1':
            settings['난이도'] = '쉬움'
            break
        elif choice == '2':
            settings['난이도'] = '보통'
            break
        elif choice == '3':
            settings['난이도'] = '어려움'
            break
        else:
            print('잘못된 선택입니다. 다시 시도하세요.')
    print(f'난이도가 {settings["난이도"]}로 설정되었습니다.')