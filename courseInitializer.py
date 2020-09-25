# Watkins, jmw4dx
import pandas as pd

def initializeCourses():
    from login.models import Course

    df = pd.read_csv("louslistData.csv")

    print(df.info())

    iloc = df.iloc
    prevMnemonic = ""
    prevNumber = 0
    for i in range(9111):
        row = iloc[i, :]
        idNum = row["ClassNumber"]
        mnemonic = row["Mnemonic"]
        number = row["Number"]
        title = row["Title"]
        if (prevMnemonic == mnemonic) and (prevNumber == number):
            continue
        else:
            prevMnemonic = mnemonic
            prevNumber = number

        course = Course(idNumber=idNum, mnemonic=mnemonic, number=number, title=title)
        course.save()