# midimaker.py
Este script de Python convierte un archivo de audio a un archivo MIDI, de tal forma que se pueda abrir en algunos programa e interpretar como una partitura. Por el momento transcribe correctamente un audio con una única línea de melodía y un único instrumento, siendo este un piano, una guitarra o una flauta dulce (experimental).

Para conocer más curiosidades sobre este programa, visite nuestra Wiki: https://github.com/MIDIMakerEHU2018/midimaker.py/wiki

Y si quiere echar un vistazo al código tras nuestra página web para poder traducir los audios a partitura visite nuestro otro repositoro: https://github.com/MIDIMakerEHU2018/MIDIMakerWeb

## Librerías utilizadas
Librosa: para el análisis y tratamiento del audio
Brian McFee, Matt McVicar, Stefan Balke, Carl Thomé, Colin Raffel, Oriol Nieto, … Adrian Holovaty. (2018, February 17). librosa/librosa: 0.6.0 (Version 0.6.0). Zenodo. http://doi.org/10.5281/zenodo.1174893

MIDIUtil: para la creación de archivos MIDI.
https://pypi.org/project/MIDIUtil/


## Instalación
Para poder utilizar este programa es necesario instalar las librerías y sus dependencias. Hay que recalcar que este script funciona correctamente si se utliza PYTHON 3. Si se utilizase Python 2 el script no funcionaría correctamente.
### Instalación mediante pip
Instalación de librosa (también se instalarán las librerías de las que depende librosa):

`sudo pip3 install librosa`

Instalación de MIDIUtil:

`sudo pip3 install MIDIUtil`
