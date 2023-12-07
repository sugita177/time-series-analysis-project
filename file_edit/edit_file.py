ROWS_PER_MONTH = 86
START_ROW = 15-1


with open("edited_data.csv", "w") as f:
    f.write("ds,y\n")

for year in range(1929, 2024):
    with open("../downloads/mtkdaily{}.txt".format(year), "r") as f:
        data_list = f.readlines()

    with open("edited_data.csv", "a") as f:
        for month in range(0, 12):
            if year == 2023 and month == 11:
                continue
            for day in range(0, 31):
                raw_data_row = data_list[START_ROW
                                         + month * ROWS_PER_MONTH
                                         + day * 2]
                data_row = raw_data_row.split()
                if len(data_row) < 2:
                    continue
                if int(data_row[0]) == day+1 and data_row[1] != "-":
                    str_month = str(month+1).zfill(2)
                    str_day = str(day + 1).zfill(2)
                    f.write("{}-{}-{},{}\n".format(year, str_month, str_day,
                                                   data_row[-1]))
