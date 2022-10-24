import sys
import matplotlib.pyplot as plt
import mariadb
import sys

mariaDBHost = "8.8.8.8"
DBUser = "admin"
DBPassword = "password"

try:
    conn = mariadb.connect(
        user=f"{DBUser}",
        password=f"{DBPassword}",
        host=f"{mariaDBHost}",
        port=3306,
        database="osu10"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

cur = conn.cursor()

cur.execute("SELECT DISTINCT user_id FROM `osu_user_stats` ORDER BY rank_score_index")

users = []

for userid in cur:
    users.append(userid[0])

cur.execute("""select user_id, max(pp)
                from osu_scores_high
                group by user_id""")

betterusers = []

for userid in cur.fetchall():
    rank = users.index(userid[0]) + 1
    usertop = (rank, userid[1])
    betterusers.append(usertop)

betterusers.sort()

# import and use the colormap
from osu_cmap import OSU_CMAP
plt.rcParams["axes.prop_cycle"] = plt.cycler("color", OSU_CMAP.colors)

x_val = [x[0] for x in betterusers]
y_val = [x[1] for x in betterusers]

with plt.style.context('./osu-news.mplstyle'):
    plt.plot(x_val,y_val)

    plt.title('User #1 score vs rank')
    plt.xlabel('Rank')
    plt.ylabel('PP')
    plt.legend(['PP'])

    plt.show()
