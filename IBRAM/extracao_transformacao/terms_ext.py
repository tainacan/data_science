import re
import csv

with open ('dicionario2.txt', 'rt') as in_file:  # Open file lorem.txt for reading of text data.
    contents = in_file.read()# Read the entire file into a variable named contents.
in_file.close()

#(?<=Def. )(.*)(?=\n) - RegExp para pegar definições
#(?<=\n)(.*)(?=\nDef. ) - RegExp para pegar os nomes

termos = re.findall(r'(?<=\n)(.*)(?=\s+Def. )', contents)

definicoes = re.findall(r'(?<=\nDef. )(.*)(?=\s+)', contents)


with open("dicionario.csv", "w", newline='', encoding="utf-8") as f:
    
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['Termos', 'Definições'])
    for i in range(len(termos)):
        writer.writerow([termos[i], definicoes[i]])
