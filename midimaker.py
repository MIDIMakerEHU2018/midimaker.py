'''
Created on 30 abr. 2018

@author: MIDIMaker
'''

import librosa
import sys
import os
import numpy as np
from midiutil.MidiFile import MIDIFile as MidiFile

#Estos parametros se utilizan cuando se emplea el metodo superflux en la deteccion de onset
sr0=44100
n_fft = 1024
hop_length = int(librosa.time_to_samples(1./200, sr=sr0))
#hop_length=512
lag = 2
n_mels = 138
fmin = 27.5
fmax = 16000.
max_size = 3


def findFramesInPulse(tempo, sr):
    #Hay que obtener la relacion entre la frecuencia de muestro utilizada y la que hay por defecto
    #porque la libreria esta adaptada para funcionar con la sr por defecto de 22050
            sheet.append([midi,val])
            #sheet.append(midi[0])
          
        else:
            #sheet.append(0)
            sheet.append([0, 0])
          
    return sheet

def normalizeComa(coma):
  
    norm = 0
    if coma > 0 and coma <0.1:
        norm = 0.0625
    else:
        if coma < 0.175:
            norm = 0.125
        else:
            if coma < 0.35:
                norm = 0.25
            else:
                if coma < 0.6:
                    norm = 0.5
                else:
                    if coma < 0.8:
                        norm = 0.75
                    else:
                        norm = 1
  
    return norm

#Devuelve la duracion en pulsos
def durStimation(frameInit, frameEnd, framePulse):
    dif = frameEnd - frameInit
    dur = dif / framePulse
    ent = int(dur)
    coma = dur - ent
  
    dur = ent + normalizeComa(coma)
  
    return dur

def maxNote(array):
    #El array que se recibe es el array de notas midi y lo que contiene es el numero de veces que se repite cada uno en un intervalo
    val = 0
    indexMax = 0
    #Se obtiene el indice que contiene la posicion con el numero mayor, que corresponde a la nota que mas veces se ha repetido en un intervalo y la que se va a indicar en la partitura
    for i in range(0, len(array)-1):
        if array[i] > val:
            val = array[i]
            indexMax = i
  
    return indexMax

def lastNote(array, frameL):
    i = frameL
    frame = len(array) -1
    found = 0
    while i < len(array) and found==0:
        if array[i][0] == 0:
            frame = i
            found = 1
        else:
            i = i+1
      
  
    return frame

def noteInInterval(array,frameL, frameH, noteAnt, guitar, framePulse):
    #Se calcula la duracion del intervalo
    dur = durStimation(frameInit=frameL, frameEnd=frameH-1, framePulse=framePulse)
    val=0
    if guitar==0: #Se obtiene la nota de mayor amplitud en el rango
        for j in range(frameL, frameH -1):
            if array[j][1] > val:
                val = array[j][1]
                note = array[j][0]
    else: #Se obtiene la nota que mas veces se repite en el rango
        arrayNotes=creatArray(109)#Es el array de las notas MIDI
        for j in range(frameL, frameH -1):
            arrayNotes[array[j][0]] = arrayNotes[array[j][0]] + 1
             
        note=maxNote(arrayNotes)
  
    #Esto corrige un fallo que se produce en estos instumentos aumentando una octava
    if onMethod==0 and note>84 and noteAnt <83:
        note = note - 12
    return [note,dur]

def durationAnalysis(y, sr, array, framePulse, guitar, onMethod):
  
    if onMethod==0:
        #Actualmente funciona bien con piano y la guitarra
        onenv = librosa.onset.onset_strength(y= y, sr = sr)
        frames=librosa.onset.onset_detect(onset_envelope=onenv, sr=sr)
    else:
        #Este es el metodo superflux onset detection. Sirve para instrumentos melodicos no-percusivos
      
        #ESTADO EXPERIMENTAL (flauta dulce)
        S = librosa.stft(y, hop_length=hop_length, n_fft=n_fft) #Esto funciona con flauta dulce
        '''
        METODOS EN ESTUDIO
        #S = librosa.feature.melspectrogram(y, sr=sr, n_fft=n_fft, hop_length=hop_length, fmin=fmin, fmax=fmax, n_mels=n_mels)
        #S=librosa.feature.chroma_stft(y=y, sr=sr, n_fft=n_fft, hop_length=hop_length)
        #S = librosa.cqt(y=y, sr=sr, hop_length=64, fmin=fmin, bins_per_octave=12)
        '''
        onenv=librosa.onset.onset_strength(S=librosa.power_to_db(S, ref=np.max), sr=sr0, hop_length=hop_length, lag=lag, max_size=max_size)
        frames = librosa.onset.onset_detect(onset_envelope=onenv, sr=sr0, hop_length=hop_length)
        #plt.plot(onenv)
        #plt.show()
      
  
    '''
    #En este caso se tiene en cuenta la energia EN ESTUDIO
    S = librosa.magphase(librosa.stft(y, window=np.ones, center=False))[0]
    ener=librosa.feature.rmse(S=S)
    frames=librosa.onset.onset_detect(y=y, sr = sr, onset_envelope=ener[0])
    '''
  
    #Aqui se estiman las duraciones
    frameH = 0
    frameL= 0
    noteAnt=0
    sheet = []
    for i in frames:
        if (frameH == frameL):
            #print(frameH)
            frameH = i
        else:
            frameL = frameH
            frameH = i
            pair= noteInInterval(array=array, frameL=frameL, frameH=frameH, noteAnt=noteAnt, guitar=guitar, framePulse=framePulse)
            sheet.append(pair)
            noteAnt=pair[0]
  
    #En esta parte se estudia la ultima vuelta       
    frameL = frameH
    frameH = lastNote(array, frameL)
    #arrayNotes=creatArray(109)
    pair=noteInInterval(array=array, frameL=frameL, frameH=frameH, noteAnt=noteAnt, guitar=guitar, framePulse=framePulse)
  
    #Se devuele un array que contiene la nota y su duracion
    sheet.append(pair)
    return sheet


def createSheet(sheet):
    #Cada elemento de la partitura contiene: [nota, duracion]
    myMidi = MidiFile(1)
    time = 0
    print(tempo)
    myMidi.addTempo(track=0, time=time, tempo=tempo)
    for i in sheet:
        if i[0] != 0:
            myMidi.addNote(track=0, channel=0, pitch=i[0], time=time, duration=i[1], volume=100)
        time = time + i[1]
      
    name= os.path.splitext(os.path.basename(sys.argv[1]))[0] + '.mid'
    path= '/home/iban/MIDIMakerWeb/public/downloads/'+name
    myFile = open(path, 'wb')
    myMidi.writeFile(myFile)
    myFile.close()
    return
  


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Faltan argumentos')
        print('Llamada de la forma: python3 midimaker.py <nombre del archivo> <instrumento>')
        exit()
      
    '''
    Combinaciones:
        inst1 = 1 es adecuado cuando se trata de cuerda pulsada o tecla, cuando hay un elemento percusivo
        Piano -> inst1 = 1 inst2 = 0 onMethod=0
        Guitarra -> inst1 = 1 inst2 = 1 onMethod=0
        Flauta Dulce (flauta) (experimental) -> inst1=1 inst2=1 onMethod=1
      
        (En proceso)
        Violin ->
        Cello ->
        Flauta Travesera ->
      
    '''
  
    if len(sys.argv) == 2:
    #print(inst1, inst2, onMethod)
  
    #Cargamos el audio, muestrea automaticamente a 22050 a no ser que se lo indiquemos
    print('Cargando Audio')
  
    path='/home/iban/MIDIMakerWeb/public/uploads/'+sys.argv[1]
  
    if (onMethod == 0):
        y,sr = librosa.load(path)
    else:
        y,sr = librosa.load(path, sr=sr0)
    print('Frecuencia de muestreo:',sr)


    '''
    Se plantea separar percusion y melodia cuando sean senales mas complejas
    #Con esta funcion se separa percusion y melodia
    #yHarmony, yPercussion = librosa.effects.hpss(y)
    '''
  
    ###########################################################
    #Se calcula el tempo
    print('Calculando Tempo:')
    #Utiliza las caracteristicas de percusion, que suelen ser mas precisas para obtener el tempo {'frames', 'samples', 'time'}
    #tempo, beats = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop, units='frames')
    tempo = librosa.beat.tempo(y=y, sr=sr)
    print('Tempo:')
    print(tempo)
    tempo = int(round(tempo[0]))
  
    #Se obtienen los frames que hay en 1 pulso
    framePulse = findFramesInPulse(tempo, sr)
    print('Frames en 1 pulso:')
    print(framePulse)
  
    ############################################################
  
    print('Ahora comieza la magia')
    print('Inicio del proceso de traduccion')

    #Devuelve un array con la nota en cada instante de tiempo y su amplitud -> [[pitch0, amp0],[pitch1, amp1],[pitch2, amp2],[pitch3, amp3],...]
    array = findNote(y, sr,inst1, onMethod=onMethod)
    print('Fin del proceso de traduccion')
  
    #print(array)
    print('Estimando duraciones')
    sheet = durationAnalysis(y= y, sr=sr, array=array, framePulse=framePulse, guitar=inst2, onMethod=onMethod)
    print('Duraciones estimadas')
      
    #Se crea el archivo Midi
    print('Creando la partitura')
    createSheet(sheet)
    print('Disfrute de la musica')
  
    pass
