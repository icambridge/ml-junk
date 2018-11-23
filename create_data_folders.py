import shutil
import pandas

df = pandas.read_csv("hockey_jerseys_processed.csv")

legit_count = 0
fake_count = 0
for i, url, legit, file in df.itertuples(index=False):
    if legit == 1:
        legit_count = legit_count + 1
        if legit_count > 1300:
            folder = "validation"
        else:
            folder = "training"
        sub_folder = "legit"
    else:
        fake_count = fake_count + 1
        if fake_count > 300:
            folder = "validation"
        else:
            folder = "training"
        sub_folder = "fake"

    base_filename = file.split("/")[1]
    new_filename = "data/%s/%s/%s" % (folder, sub_folder, base_filename)

    shutil.copyfile("./"+file,new_filename)
    print("Copying " + file + " to " + new_filename)

print(fake_count)
print(legit_count)