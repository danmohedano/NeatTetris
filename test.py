from neattetris.gamestates import GameStateRubik
end = 0
test = GameStateRubik(3)

print(test.up[:, :])
print(test.data)

while end == 0:
    test.visual()
    end = test.input()
