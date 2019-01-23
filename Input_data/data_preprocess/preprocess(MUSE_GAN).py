
## 상단에 위치한 paths만 잘 맞게 바꿔주시고 실행하시면 됩니다.

####################################################################################
import numpy as np
import pretty_midi
import os
###############################################################################
path_input_midi = '/home/ktai17/Desktop/input_midi' #midi파일들만 넣어줌
path_input_preprocessed = '/home/ktai17/Desktop/input_preprocessed' #비워둠

os.chdir(path_input_midi)
os.getcwd()
print(len(os.listdir())) # the number of input midi files

list_midifile = os.listdir()
num = len(list_midifile)
list_midifile.sort()

list_test = []
####################################################################################

### original key
def original_save(midifile):
    global data2
    data1 = pretty_midi.PrettyMIDI(midifile) #midi_file을 로드
    data2 = data1.get_piano_roll() # piano_roll을 저장
    #print(data2.shape) # shape = (ptich, bars) = (128, bars)
    #pitch(음 높낮이)는 128로 로드된다.

    data22=np.delete(data2, [106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127], axis=0)
    #print(data22.shape)
    data23=np.delete(data22, [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21], axis=0)
    #print(data23.shape) # shape = (pitch, all_bars) = (84, all_bars)
    #MUSEGAN의 input으로 사용되는 음악의 높낮이는 84이므로, 128인 음악에서 44개의 음을 제거해주어야 한다.
    #가장 높은 음 22개와 가장 낮은 음 22개를 제거해주었다.

    data2 = data23
    #print(data2.shape) # shape = (pitch, all_bars) = (84, all_bars)

    data3 = data2.transpose(1, 0)
    #print(data3.shape) # shape = (all_bars, pitch) = (all_bars, 84)
    len = data3.shape[0] #all_bars
    len = int(len/96) #all_bars를 96으로 몇 번 나눌 수 있는가.
    #print(len)

    for j in range(0,len):
        temp = data3[j*96:(j+1)*96,:] #temp : (all_bars, 84)를 (96_bars, 84)들로 나눌 때, 한 단위의 list
        list_test.append([temp]) #list_test : temp들을 len개 만큼 얻어서 list_test에 append해준다.
    #print(np.array(list_test).shape) # shape = (len, 1, bars, pitch) = (len, 1, 96, 84)

### changed key(data augmentation)
def code_change_save(much): #much : 몇 개의 data를 augment할 것인가. ex. much=3이면, 원곡보다 1, 2, 3키를 올린 데이터들을 만들어준다.
    #print(data2.shape) # shape = (pitch, all_bars) = (84, all_bars)
    temp = np.zeros(shape=[much,data2.shape[1]])
    #print(temp.shape) # shape = (much, all_bars)
    temp2 = np.vstack((temp,data2)) # 0행렬을 data2행렬의 위쪽에 붙여준다.
    #print(temp2.shape) # shape = (much+84, all_bars)
    temp3 = temp2
    for i in range(much):
        temp3 = np.delete(temp3, (-1), axis=0)
    #print(temp3.shape) # shape = (much+84-much, all_bars) = (84, all_bars)
    data3 = temp3.transpose(1, 0)
    #print(data3.shape) # shape = (all_bars, 84)

    len = data3.shape[0] #all_bars
    len = int(len/96) #all_bars를 96으로 몇 번 나눌 수 있는가

    for j in range(0,len):
        temp4 = data3[j*96:(j+1)*96,:] #temp4 : (all_bars, 84)를 (96_bars, 84)들로 나눌 때, 한 단위의 list
        list_test.append([temp4]) #list_test : temp들을 len개 만큼 얻어서 list_test에 append해준다.

### shape change(from (total_bars, 1, 96, 84) to (total_bars3, 6, 4, 96, 84, 8))
def shape_change(tete):
    global tete12
    tete1=np.transpose(tete, [3,2,1,0])
    #print(tete1.shape) # shape = (84, 96, 1, total_bars)
    tete2=np.array([tete1])
    #print(tete2.shape) # shape = (1, 84, 96, 1, total_bars)
    tete3=np.transpose(tete2, [4,3,2,1,0])
    #print(tete3.shape) # shape = (total_bars, 1, 96, 84, 1)
    tete4=np.concatenate((tete3[:]))
    #print(tete4.shape) # shape = (total_bars, 96, 84, 1)
    tete5=np.array(tete4[:int(tete4.shape[0]-tete4.shape[0]%24),:,:,:])
    #print(tete5.shape) # shape = (total_bars2, 96, 84, 1)
    # (total_bars2) = (total_bars)-(total_bars를 24로 나누었을 때 생기는 나머지)를 계산해주는 이유는
    # tete6을 구할 때, total_bars를 (24 x (total_bars/24))의 차원으로 나누어주기 위함이다.
    tete6=np.reshape(tete5, (int(tete5.shape[0]/24), 24, 96, 84, 1))
    #print(tete6.shape) # shape = (total_bars3, 24, 96, 84, 1)
    # (total_bars3) = (total_bars2)/24
    tete7=np.reshape(tete6, (tete6.shape[0], 6, 4, 96, 84, 1))
    #print(tete7.shape) # shape = (total_bars3, 6, 4, 96, 84, 1)
    tete8=np.transpose(tete7, (5,4,3,2,1,0))
    #print(tete8.shape) # shape = (1, 84, 96, 4, 6, total_bars3)
    pepe=np.zeros_like(tete8)
    #print(pepe.shape) # shape = (1, 84, 96, 4, 6, total_bars3)
    tete9=np.concatenate((pepe,tete8), axis=0)
    #print(tete9.shape) # shape = (2, 84, 96, 4, 6, total_bars3)
    tete10=np.concatenate((tete9,pepe), axis=0)
    #print(tete10.shape) # shape = (3, 84, 96, 4, 6, total_bars3)
    tete10=np.concatenate((tete10,pepe), axis=0)
    #print(tete10.shape) # shape = (4, 84, 96, 4, 6, total_bars3)
    tete10=np.concatenate((tete10,pepe), axis=0)s
    #print(tete10.shape) # shape = (5, 84, 96, 4, 6, total_bars3)
    tete10=np.concatenate((tete10,pepe), axis=0)
    #print(tete10.shape) # shape = (6, 84, 96, 4, 6, total_bars3)
    tete10=np.concatenate((tete10,pepe), axis=0)
    #print(tete10.shape) # shape = (7, 84, 96, 4, 6, total_bars3)
    tete10=np.concatenate((tete10,pepe), axis=0)
    #print(tete10.shape) # shape = (8, 84, 96, 4, 6, total_bars3)
    tete11=(tete10!=0)
    #0이 아닌 성분을 True, 0인 성분을 False로 만들어서 tete11이라는 list로 만들어준다.
    #즉, tete11은 True, False로 되어있는 list이다.
    #print(tete11.shape) # shape = (8, 84, 96, 4, 6, total_bars3)
    tete12=np.transpose(tete11, [5,4,3,2,1,0])
    #print(tete12.shape) # shape = (total_bars3, 6, 4, 96, 84, 8)

####################################################################################

### Data preprocessing & augmentation
#data의 dimension을 musegan의 input의 형태로 맞추어줌.
#한 곡에 대하여 키를 변형시켜 data augmentation하는 과정을 d번 거쳐 d+1배 개의 파일로 만들어 준 다음,
#원키를 1개와 변형된 키 d개를 포함하여 d+1개의 행렬을 하나의 list(list_test)로 합쳐줌.
#이 과정을 폴더 안에 있는 모든 num개의 midi file들에 대하여 해줌
c = np.zeros(shape=(1,96,84))
d = 1

for h in range(num):
    original_save(list_midifile[h])
    list_test.append(c)
    for i in range(d):
        code_change_save(i)
        list_test.append(c)

### Changing shape of the data
tete = np.array(list_test)
#print(tete.shape) #shape = (total_bars, 1, 96, 84)
# total_bars = num x {(각 곡에 대한 len x (d+1)}

shape_change(tete) #tete -> tete12
#print(tete12.shape)

### npy로 저장
os.chdir(path_input_preprocessed)
np.save('preprocessed.npy',tete12)
