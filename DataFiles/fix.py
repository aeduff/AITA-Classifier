import csv

input_file = "aita_clean.csv"
output_file = "aita_clean_fixed.csv"

BODY_COLUMN_INDEX = 3
TITLE_COLUMN_INDEX = 2
VERDICT_COLUMN_INDEX = 5

with open(input_file, mode="r", encoding="utf-8") as infile:
    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile,  quoting=csv.QUOTE_ALL)
        for row in reader:
            # combine all lines in the body field into one
            if len(row) > BODY_COLUMN_INDEX:
                row[BODY_COLUMN_INDEX] = row[BODY_COLUMN_INDEX].replace("\n", " ")
            writer.writerow(row)

print(f"Fixed CSV saved as {output_file}")

assholeCount = 0
notTheAssholeCount = 0

with open(output_file, mode="r", encoding="utf-8") as infile:
    AHFile = open("AH.csv", mode="w", newline="", encoding="utf-8")
    NTAFile = open("NTA.csv", mode="w", newline="", encoding="utf-8")
    reader = csv.reader(infile)
    writer1 = csv.writer(AHFile,  quoting=csv.QUOTE_ALL)
    writer2 = csv.writer(NTAFile,  quoting=csv.QUOTE_ALL)
    print(next(reader))
    print(next(reader))

    for row in reader:
        if row[VERDICT_COLUMN_INDEX] == "asshole":
            assholeCount += 1 # asshole count
            if row[TITLE_COLUMN_INDEX] == "" or row[BODY_COLUMN_INDEX] == "": # ignore empty entries
                continue
            # fixing formatting issues
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('“', '""')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('“', '""')
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('”', '""')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('”', '""')
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('\\', '\\\\')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('\\', '\\\\')
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('"', r'\"')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('"', r'\"')
            writer1.writerow([row[VERDICT_COLUMN_INDEX], row[TITLE_COLUMN_INDEX], row[BODY_COLUMN_INDEX]])
        elif row[VERDICT_COLUMN_INDEX] == "not the asshole":
            if row[TITLE_COLUMN_INDEX] == "" or row[BODY_COLUMN_INDEX] == "": # ignore empty entries
                continue
            notTheAssholeCount += 1 # not the asshole count
            # fixing formatting issues
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('“', '""')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('“', '""')
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('”', '""')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('”', '""')
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('\\', '\\\\')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('\\', '\\\\')
            row[TITLE_COLUMN_INDEX] = (row[TITLE_COLUMN_INDEX]).replace('"', r'\"')
            row[BODY_COLUMN_INDEX] = (row[BODY_COLUMN_INDEX]).replace('"', r'\"')
            writer2.writerow([row[VERDICT_COLUMN_INDEX], row[TITLE_COLUMN_INDEX], row[BODY_COLUMN_INDEX]])

print(f"Asshole count: {assholeCount}")
print(f"Not the asshole count: {notTheAssholeCount}")



# divide into train, validation, and test sets
with open("AH.csv", mode="r", encoding="utf-8") as beforeAH, \
     open("NTA.csv", mode="r", encoding="utf-8") as beforeNTA:

    readerAH = list(csv.reader(beforeAH)) 
    readerNTA = list(csv.reader(beforeNTA))
    
    headersAH, dataAH = readerAH[0], readerAH[1:]
    headersNTA, dataNTA = readerNTA[0], readerNTA[1:]
    
    with open("AHTrain.csv", mode="w", newline="", encoding="utf-8") as afterAH1, \
         open("AHValidation.csv", mode="w", newline="", encoding="utf-8") as afterAH2, \
         open("AHTest.csv", mode="w", newline="", encoding="utf-8") as afterAH3, \
         open("NTATrain.csv", mode="w", newline="", encoding="utf-8") as afterNTA1, \
         open("NTAValidation.csv", mode="w", newline="", encoding="utf-8") as afterNTA2, \
         open("NTATest.csv", mode="w", newline="", encoding="utf-8") as afterNTA3:

        writerAH1 = csv.writer(afterAH1)
        writerAH2 = csv.writer(afterAH2)
        writerAH3 = csv.writer(afterAH3)
        writerNTA1 = csv.writer(afterNTA1)
        writerNTA2 = csv.writer(afterNTA2)
        writerNTA3 = csv.writer(afterNTA3)

        writerAH1.writerow(headersAH)
        writerAH2.writerow(headersAH)
        writerAH3.writerow(headersAH)
        writerNTA1.writerow(headersNTA)
        writerNTA2.writerow(headersNTA)
        writerNTA3.writerow(headersNTA)

        AH_train, AH_valid, AH_test = dataAH[:16000], dataAH[16000:18000], dataAH[18000:20000]
        NTA_train, NTA_valid, NTA_test = dataNTA[:16000], dataNTA[16000:18000], dataNTA[18000:20000]

        writerAH1.writerows(AH_train)
        writerAH2.writerows(AH_valid)
        writerAH3.writerows(AH_test)
        writerNTA1.writerows(NTA_train)
        writerNTA2.writerows(NTA_valid)
        writerNTA3.writerows(NTA_test)



# combine train, validation, and test files
NTATrain = open("NTATrain.csv", mode="r", encoding="utf-8")
NTAValidation = open("NTAValidation.csv", mode="r", encoding="utf-8")
NTATest = open("NTATest.csv", mode="r", encoding="utf-8")
AHTrain = open("AHTrain.csv", mode="r", encoding="utf-8")
AHValidation = open("AHValidation.csv", mode="r", encoding="utf-8")
AHTest = open("AHTest.csv", mode="r", encoding="utf-8")

readerNTATrain = csv.reader(NTATrain)
readerNTAValidation = csv.reader(NTAValidation)
readerNTATest = csv.reader(NTATest)
readerAHTrain = csv.reader(AHTrain)
readerAHValidation = csv.reader(AHValidation)
readerAHTest = csv.reader(AHTest)

combinedTrain = open("combinedTrain.csv", mode="w", newline="", encoding="utf-8")
combinedValidation = open("combinedValidation.csv", mode="w", newline="", encoding="utf-8")
combinedTest = open("combinedTest.csv", mode="w", newline="", encoding="utf-8")

writerTrain = csv.writer(combinedTrain)
writerValidation = csv.writer(combinedValidation)
writerTest = csv.writer(combinedTest)

for row in readerNTATrain:
    writerTrain.writerow(row)
for row in readerAHTrain:
    writerTrain.writerow(row)

for row in readerNTAValidation:
    writerValidation.writerow(row)
for row in readerAHValidation:
    writerValidation.writerow(row)

for row in readerNTATest:
    writerTest.writerow(row)
for row in readerAHTest:
    writerTest.writerow(row)


bodyIndex = 2
titleIndex = 1
verdictIndex = 0

# turn into json files with title and body combined
combinedTrain = open("combinedTrain.csv", mode="r", encoding="utf-8")
combinedValidation = open("combinedValidation.csv", mode="r", encoding="utf-8")
combinedTest = open("combinedTest.csv", mode="r", encoding="utf-8")

readerTrain = csv.reader(combinedTrain)
readerValidation = csv.reader(combinedValidation)
readerTest = csv.reader(combinedTest)

jsonTrain = open("train.jsonlist", mode="w", encoding="utf-8")
jsonValidation = open("validation.jsonlist", mode="w", encoding="utf-8")
jsonTest = open("test.jsonlist", mode="w", encoding="utf-8")

for row in readerTrain:
    jsonTrain.write(f'{{"verdict": "{row[verdictIndex]}", "body": "[TITLE] {row[titleIndex]} [BODY] {row[bodyIndex]}"}}\n')
for row in readerValidation:
    jsonValidation.write(f'{{"verdict": "{row[verdictIndex]}", "body": "[TITLE] {row[titleIndex]} [BODY] {row[bodyIndex]}"}}\n')
for row in readerTest:
    jsonTest.write(f'{{"verdict": "{row[verdictIndex]}", "body": "[TITLE] {row[titleIndex]} [BODY] {row[bodyIndex]}"}}\n')



# combine test train and validation files for each category
NTATrain = open("NTATrain.csv", mode="r", encoding="utf-8")
NTAValidation = open("NTAValidation.csv", mode="r", encoding="utf-8")
NTATest = open("NTATest.csv", mode="r", encoding="utf-8")
AHTrain = open("AHTrain.csv", mode="r", encoding="utf-8")
AHValidation = open("AHValidation.csv", mode="r", encoding="utf-8")
AHTest = open("AHTest.csv", mode="r", encoding="utf-8")

readerNTATrain = csv.reader(NTATrain)
readerNTAValidation = csv.reader(NTAValidation)
readerNTATest = csv.reader(NTATest)
readerAHTrain = csv.reader(AHTrain)
readerAHValidation = csv.reader(AHValidation)
readerAHTest = csv.reader(AHTest)

combinedAH = open("combinedAH.csv", mode="w", newline="", encoding="utf-8")
combinedNTA = open("combinedNTA.csv", mode="w", newline="", encoding="utf-8")

writerAH = csv.writer(combinedAH)
writerNTA = csv.writer(combinedNTA)

for row in readerNTATrain:
    writerNTA.writerow(row)
for row in readerNTAValidation:
    writerNTA.writerow(row)
for row in readerNTATest:
    writerNTA.writerow(row)

for row in readerAHTrain:
    writerAH.writerow(row)
for row in readerAHValidation:
    writerAH.writerow(row)
for row in readerAHTest:
    writerAH.writerow(row)


