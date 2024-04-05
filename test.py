open_ports={1:"open", 20:"open"}
i=0
vulnerabilities=[]
with open('vulnerabilities.txt', encoding='utf8') as file:
        for key in open_ports.keys():
            for line in file:
                parts = line.split(':')
                if int(parts[0]) == key:
                    vulnerabilities[i]=parts[1].strip()
            i+=1
        if not vulnerabilities:
            vulnerabilities.append("None")
 
for vul in vulnerabilities:
    print(vul)