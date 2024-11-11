# Iterate down the major diagonal to find the minimum bid
# Go recursive to explore for better  --
# # Fail case is if current path is already > min bid
# # Else check L, R, and C (if it's >= 3 Cs in a row)
# # Recursive call is  ((x,y), loss_so_far, C-streak)
from utils import get_data
grid = []

if __name__ == "__main__":
    stage = 0
    data = get_data(stage, __file__, string=True)
    grid = data.split("\n")