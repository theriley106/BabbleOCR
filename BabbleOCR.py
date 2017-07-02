import pytesseract
import Image
import re

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def OCR(picture, listofwords):
	text = pytesseract.image_to_string(Image.open(picture)).replace('\n', ' ').split(' ')
	e = []
	for f in text:
		e.append(f)
	wordintext = len(text)
	anchorwords = []
	for words in listofwords:
		a = True
		for tex in text:
			if levenshtein(words, tex) == 0 and a == True:
				text.remove(tex)
				anchorwords.append(tex)
	results = []
	for i in range(len(listofwords)):
		similarity = len(set(listofwords[i: i + wordintext]).intersection(anchorwords))
		results.append([similarity, listofwords[i: i + wordintext]])
	regex = re.compile('[^a-zA-Z]')
	correct = []
	a = sorted(results,key=lambda x: x[0], reverse=True)
	for i in range(5):
		correct.append([levenshtein(''.join(map(str, a[i][1])), ''.join(map(str, e))), str(a[i][1]).encode('ascii', 'ignore')])
	return str(re.sub(r'\W+', ' ', str(sorted(correct,key=lambda x: x[0])))).replace(' u ', ' ')



