import sys, os, argparse
from sys import argv


if __name__=='__main__' :

    fichier_texte = sys.argv[1]

    f = open(fichier_texte, 'r')
    lignes = f.readlines()

    tier1 = []
    for l in lignes:
        if l.endswith('\n'):
            l = l[:-1]

        file, channel, debut, temp, label, conf, test = l.split(" ")

        tier1.append((debut, temp, label))

    # Creation d'une liste de tuple contenant les temps_debut temps_fin label avec les silences intermédiaires
    datas = []

    temps_fin = float(tier1[0][0])

    for j in range(0, len(tier1)):
        temps_debut = float(tier1[j][0])
        if temps_fin == temps_debut:
            datas.append((temps_debut, round(float(tier1[j][0]) + float(tier1[j][1]), 2), tier1[j][2]))
            temps_fin = round(float(tier1[j][0]) + float(tier1[j][1]), 2)
        elif temps_fin < temps_debut:
            # Rajout de silences quand les phonemes ne sont pas consecutifs
            datas.append((temps_fin, round(float(tier1[j][0]), 2), " "))
            datas.append((round(float(tier1[j][0]), 2), round(float(tier1[j][0]) + float(tier1[j][1]), 2),
                          tier1[j][2]))
            temps_fin = round(float(tier1[j][0]) + float(tier1[j][1]), 2)
        else:
            datas.append((temps_fin, temps_fin - 00.01 + float(tier1[j][1]), tier1[j][2]))
            temps_fin = temps_fin - 00.01 + float(tier1[j][1])

def est_silence(phon):
    return (phon=='sil' or phon==' ' or phon=="" or phon=='inh' or phon=='sil/inh')
    
#supprimer les silences
def remove_consecutive_silences(data):
    while data and est_silence(data[0][-1]):
        data.pop(0)
    while data and est_silence(data[-1][-1]):
        data.pop()
    return data

datas=remove_consecutive_silences(datas)


voyelles=['AE_S','A~_S','a~_S','E~_S','o~_S','E_S','a_S','e_S','i_S','O_S','o_S','u_S','y_S', 'i','e','ɛ','ɛː','y','ø','œ','ə','u','o','ɔ','a','ɑ','ɑ̃','ɔ̃','ɛ̃','œ̃','j','ɥ','w']

    # Fonction pour calcul duree silences, calcul duree voyelles, calcul débit parole
def calculate_metrics(datas):
    total_silence_duration = 0
    total_silence_count = 0
    total_vowel_duration = 0
    total_vowel_count = 0
    total_duration = datas[-1][1]

    for deb, fin, phon in datas:
        if est_silence(phon):
            total_silence_duration += fin - deb
            total_silence_count += 1
        elif phon in voyelles:
            total_vowel_duration += fin - deb
            total_vowel_count += 1

    average_silence_duration = total_silence_duration / total_silence_count if total_silence_count != 0 else 0
    phonation_time=total_duration-total_silence_duration
    speech_rate = total_vowel_count / phonation_time
    average_vowel_duration = total_vowel_duration / total_vowel_count if total_vowel_count != 0 else 0

    return average_silence_duration, speech_rate, average_vowel_duration

average_silence_duration, speech_rate, average_vowel_duration = calculate_metrics(datas)

print("Metrics for the entire data:")
print("Average Silence Duration: {:.4f}".format(round(average_silence_duration, 4)))
print("Speech Rate: {:.4f}".format(round(speech_rate, 4)))
print("Average Vowel Duration: {:.4f}".format(round(average_vowel_duration, 4)))

