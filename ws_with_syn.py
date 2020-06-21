import argparse
import requests
from bs4 import BeautifulSoup
import sys , time
from requests import get
import os
from pathlib import Path

special_colored ='css-r5sw71-ItemAnchor etbu2a31'
common ='css-17d6qyx-WordGridLayoutBox et6tpn80'
URL2='https://www.thesaurus.com/browse/'



def scrap_synonyms(word):
    
    synonyms_list=[]
    response = get(URL2+word)
    soup= BeautifulSoup(response.text, 'html.parser')
    word_container =soup.find_all('a', class_ = special_colored) 
    
    if not word_container:
        word_container =soup.find_all('ul',class_=common)
        got=word_container[0].find_all('a')
        for word in got:
            synonyms_list.append(word.get_text())
            
    else :
        for word in word_container:
            synonyms_list.append(word.get_text())
    
    return str(synonyms_list)


parser = argparse.ArgumentParser()
parser.add_argument("readfile", help="read from this file",type=str)
parser.add_argument("textfile", help="write to this file",type=str)
args = parser.parse_args()
READ = args.readfile

Path("list").mkdir(parents=True, exist_ok=True)
outfile='list/'+ args.textfile


ox='https://www.oxfordlearnersdictionaries.com/definition/english/'

filew= open(outfile, 'w')     

def getIDS(word): 
        URL = ox+ word.strip() #[:-1]
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        ids = [tag['id'] for tag in soup.select('li[id]')]
        
        return ids,soup


def get_meaning(result):
    return result.find('span',attrs={'class':"def"}).get_text()

def get_example(results):
    
    d2=results.find('ul')
    if d2 is not None:
        for v in d2:
            T=v.find('span', class_='x')
            if T is not None:
            	Tw=T.get_text()
            	filew.write(Tw+'\n')
            else : break


        
def writeAll(idx,soup,word,idd):
    results = soup.find(id=idd) 
    meaning = get_meaning(results)
    synonyms = scrap_synonyms(word.lower())
    #print("    ")
    filew.write('\n')
    filew.write("@@@@@@"+'\n')
    filew.write(idx+": "+word.upper() +"meaning :"+meaning+'\n')
    filew.write('\n')
    filew.write("synonyms :"+synonyms+'\n')
    filew.write('\n')
    get_example(results)
        
    
       
        
file1 = open(READ,"r+")
mispel=[]
#if file1.mode == 'r':
f=file1.readlines() 
file_len=len(f)
print("Scrapping meaning:")
#animation = ["10%", "20%", "30%", "40%", "50%", "60%", "70%", "80%", "90%", "100%"]
animation = ["[■□□□□□□□□□]","[■■□□□□□□□□]", "[■■■□□□□□□□]", "[■■■■□□□□□□]", "[■■■■■□□□□□]", "[■■■■■■□□□□]", "[■■■■■■■□□□]", "[■■■■■■■■□□]", "[■■■■■■■■■□]", "[■■■■■■■■■■]"]
animlen=len(animation)
percent_count_on=file_len//animlen  # 333 % 10 = 33
i=0
reminder= file_len%animlen

for p,word in enumerate(f,1):
    ids,soup = getIDS(word.lower())
    
    if not ids:
    	mispel.append(word.strip()) 
  
    else:
#    print(ids)
        for ID in ids: 
            writeAll(str(p),soup,word,ID)

    if p % percent_count_on==0:
    	if i<animlen-1:
		    sys.stdout.write("\r" + animation[i % animlen])
		    sys.stdout.flush()
		    i+=1

sys.stdout.write("\r" + animation[i % animlen])
sys.stdout.flush()
print("\n")

for mis in mispel:
	print(mis , "spelling is incorrect")
print("\n")                    
file1.close()
filew.close()
    
   #senses_multiple


