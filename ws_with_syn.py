import argparse
import requests
from bs4 import BeautifulSoup
import sys , time
from requests import get
import os
from pathlib import Path
import numpy as np
start_time = time.time()
special_colored ='css-r5sw71-ItemAnchor etbu2a31'
common ='css-17d6qyx-WordGridLayoutBox et6tpn80'
URL2='https://www.thesaurus.com/browse/'

delays = [7, 4, 6, 2, 10,5]


def scrap_synonyms(word):
    
    synonyms_list=[]
#     delay = np.random.choice(delays)
#     time.sleep(delay)
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
missed= 'list/missed_'+args.textfile

ox='https://www.oxfordlearnersdictionaries.com/definition/english/'

filew= open(outfile, 'w')     

def getIDS(word): 
        URL = ox+ word.strip() #[:-1]
        delay = np.random.choice(delays)
        time.sleep(delay)
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

def example_sentence(word,results):
#     delay = np.random.choice(delays)
#     time.sleep(delay)
    page = requests.get('https://wordsinasentence.com/'+word.strip()+'-in-a-sentence/')
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup.find_all('p')[0].get_text()[:5]=='Oops!' :
        get_example(results)
        return 
    for pera in soup.find_all('p') :
        if pera.get_text()=='' or pera.get_text()[:11]=='Most Search':break
        filew.write(pera.get_text()+'\n\n')
    return 

                
      
def bangla_meaning(word):
    a='http://www.kitkatwords.com/dictionary/translate/?lang=Bengali&shabd='
    b='&searched=Search'
#     delay = np.random.choice(delays)
#     time.sleep(delay)
    page=requests.get(a+word+b)
    soup = BeautifulSoup(page.content ,'html.parser')
    sf=soup.find('ul', class_ = 'Word-Meaning')
    if sf: 
        res=sf.find_all('a')
        L=len(res)
        bangla_list=[]
        if res:
            for m in res:
                bangla_list.append(m.get_text())      
        filew.write(str(bangla_list))
        
def writeAll1(idx,soup,word,idd):
    results = soup.find(id=idd) 

    meaning = get_meaning(results)
    
    #print("    ")
    filew.write('\n')
    filew.write("@@@@@@"+'\n')
    filew.write(idx+": "+word.upper() +"meaning :"+meaning+'\n')
    
def writeAll2(idx,soup,word,idd,mc):
    results = soup.find(id=idd) 
    meaning = get_meaning(results)
    if mc is 0:
        filew.write(idx+": "+word.upper() +"meaning 1:"+meaning+'\n')
    if mc > 0:
        filew.write("meaning "+str(mc+1)+":"+meaning+'\n')
        

def write_only_syn_exm(word,soup,idd):
    results = soup.find(id=idd) 
    bangla_meaning(word)
    synonyms = scrap_synonyms(word.lower())
    filew.write('\n')
    filew.write("synonyms :"+synonyms+'\n')
    filew.write('\n')
    example_sentence(word,results)    


       
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

c=0
for p,word in enumerate(f,1):
    #print(p,word)
    ids,soup = getIDS(word.lower())
    
    if not ids:
        mispel.append(word.strip()) 
  
    else:
#    print(ids)
        c+=1
        
        if len(ids) is 1:
            for ID in ids:
                try :
                    writeAll1(str(c),soup,word,ID)
                    filew.write('\n')
                    write_only_syn_exm(word,soup,ID)
                except : 
                    c-=1
                    mispel.append(word.strip()) 
                    break

        else:
            filew.write('\n')
            filew.write("@@@@@@"+'\n')
            for meaning_count,ID in enumerate(ids):
                writeAll2(str(c),soup,word,ID,meaning_count)
            filew.write("\n") 
            write_only_syn_exm(word,soup,ID)

    if p % percent_count_on==0:
        
        if (i<animlen-1):
    
            sys.stdout.write("\r" + animation[i % animlen])
            sys.stdout.flush()
            i+=1

sys.stdout.write("\r" + animation[i % animlen])
sys.stdout.flush()
print("\n")

filem= open(missed, 'w') 
def example_sentence2(word,c):
#     delay = np.random.choice(delays)
#     time.sleep(delay)
    page = requests.get('https://wordsinasentence.com/'+word.strip()+'-in-a-sentence/')
    soup = BeautifulSoup(page.content, 'html.parser')
    if soup.find_all('p')[0].get_text()[:5]=='Oops!' :
        print(mis , "spelling is incorrect")
        filem.write(mis)
        filem.write('\n')        
        return c
    
    filew.write('@@@@@@'+'\n') 
    filew.write(str(c)+ " " +word+"  meaning :\n")
    bangla_meaning(word)
    filew.write('\n') 
    synonyms = scrap_synonyms(word.lower())
    filew.write("synonyms :"+synonyms+'\n')
    filew.write('\n') 
    for pera in soup.find_all('p') :
        if pera.get_text()=='' or pera.get_text()[:11]=='Most Search':break
        filew.write(pera.get_text()+'\n\n')
    return c+1


if mispel :
    for mis in mispel:
        c=example_sentence2(mis.strip(),c)

print("\n")

file1.close()
filew.close()
filem.close()

end=time.time() - start_time
end/=3600
print("time in hour",end)
