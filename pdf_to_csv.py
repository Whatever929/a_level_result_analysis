import tabula
import pathlib
import os
import pandas as pd

JSON_PATH = pathlib.Path("template.json")
JSON_PATH_2 = pathlib.Path("template2.json")
PDF_PATH = pathlib.Path("./statistics")
CSV_PATH = pathlib.Path("./csv")

CSV_PATH.mkdir(parents=True, exist_ok=True)

def pdf_to_csv(input_path):
    def parse_to_csv(input_path, template_path, length):
        dfs = tabula.read_pdf_with_template(input_path = pdf_path, template_path = JSON_PATH, pages="all")
        if length == 1:
            df1 = dfs[0]

        else:
            df1 = dfs[0]
            df2 = dfs[1]

        if length == 1:
            new_column = df1.iloc[0]
            new_column[0] = "Subject"
            df1.columns = new_column
            df1.drop(0, inplace=True)
        
        else:
            for i in [df1, df2]:
                new_column = i.iloc[0]
                new_column[0] = "Subject"
                i.columns = new_column
                i.drop(0, inplace=True)
        
        if length == 1:
            df_final = df1

        else:
            df_final = pd.concat([df1, df2], ignore_index=True)

        print("Preview:")
        print(df1.head(5))
        print(df2.head(5))
        if input("Proceed? ") != "":
            raise Exception()


        df_final.to_csv(CSV_PATH / input_path.with_suffix(".pdf").name, index=False)

    print(f"Now parsing {input_path.name}")
    try:
        parse_to_csv(input_path, JSON_PATH, 2)
    except Exception as e:
        print(e)
        try: 
            if input("Try alternative json? ") != "":
                raise Exception()
            print("Trying out alternative json....")
            parse_to_csv(input_path, JSON_PATH_2, 1)
        except Exception as e:
            print(e)
            print(f"Cannot parse pdf file {input_path.name}")
            with open("error.txt", "a") as f:
                f.write(input_path.name + "\n")
                return

if __name__ == "__main__":
    for i in os.listdir(PDF_PATH):
        pdf_path = PDF_PATH / i
        pdf_to_csv(pdf_path)
