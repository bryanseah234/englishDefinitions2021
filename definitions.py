import os
import pathlib
import pdfminer.high_level
from tqdm import tqdm
import csv
from collections import Counter
from PyDictionary import PyDictionary
directory = pathlib.Path().absolute()

def quickSort(array):
    if len(array) > 1:
        ltepivot = []
        gtpivot = []
        pivot = array[-1]
        for i in range(0, len(array) - 1):
            if array[i] > pivot:
                gtpivot.append(array[i])
            else:
                ltepivot.append(array[i])
        ltepivot = quickSort(ltepivot)
        gtpivot = quickSort(gtpivot)
        pivotlist = []
        pivotlist.append(pivot)
        sortedarray = ltepivot + pivotlist + gtpivot
        return sortedarray
    else:
        return array
    

def get_definitions_of_words_from_pdf():
    pdfs_path = [] #list of 1 element, is the current directory 
    data = [] #list of words
    dics = [] #list of dictionarys
    uncommon = [] #list of words
    dictionary = PyDictionary()
    characters = "!@#$%‘\"©^&*(▪).\\|/{}[]<>●,-+=_~`\'"
    
    # common words which will be filter out (no definitions for these words... should have used a hashmap...
    commons = ['a', 'able', 'about', 'above', 'abovementioned', 'act', 'adams', 'adapt', 'add', 'afraid', 'after', 'again', 'against', 'age', 'ago', 'agree', 'air', 'all', 'allow', 'also', 'always', 'am', 'among', 'an', 'and', 'anger', 'animal', 'answer', 'any', 'appear', 'apple', 'are', 'area', 'arm', 'arrange', 'arrive', 'art', 'as', 'ask', 'at', 'atom', 'avoid', 'baby', 'back', 'bad', 'ball', 'band', 'bank', 'bar', 'base', 'based', 'basic', 'basis', 'bat', 'be', 'bear', 'beat', 'beauty', 'bed', 'been', 'before', 'began', 'begin', 'behind', 'being', 'believe', 'bell', 'best', 'better', 'between', 'big', 'bird', 'bit', 'black', 'block', 'blood', 'blow', 'blue', 'board', 'boat', 'body', 'bone', 'book', 'born', 'both', 'bottom', 'bought', 'box', 'boy', 'branch', 'bread', 'break', 'bright', 'bring', 'broad', 'broke', 'brother', 'brought', 'brown', 'build', 'burn', 'busy', 'but', 'buy', 'by', 'call', 'came', 'camp', 'can', 'capital', 'captain', 'car', 'card', 'care', 'carry', 'case', 'cat', 'catch', 'caught', 'cause', 'cell', 'cent', 'center', 'century', 'certain', 'chair', 'chance', 'change', 'character', 'characteristic', 'charge', 'chart', 'check', 'chick', 'chief', 'child', 'children', 'china', 'choose', 'chord', 'circle', 'city', 'claim', 'class', 'clean', 'clear', 'climb', 'clock', 'close', 'clothe', 'cloud', 'coast', 'coat', 'cold', 'collect', 'colony', 'color', 'column', 'come', 'common', 'company', 'compare', 'complete', 'condition', 'connect', 'consider', 'consonant', 'contain', 'continent', 'continue', 'control', 'cook', 'cool', 'copy', 'corn', 'corner', 'correct', 'cost', 'cotton', 'could', 'count', 'country', 'course', 'court', 'cover', 'cow', 'crease', 'create', 'crop', 'cross', 'crowd', 'cry', 'current', 'cut', 'dad', 'dance', 'danger', 'dark', 'david', 'day', 'dead', 'deal', 'dear', 'death', 'decide', 'decimal', 'deep', 'degree', 'depend', 'describe', 'desert', 'design', 'determine', 'develop', 'diana', 'dictionary', 'did', 'die', 'differ', 'differentiated', 'difficult', 'direct', 'discuss', 'distant', 'divide', 'division', 'do', 'doctor', 'does', 'dog', 'dollar', 'done', 'don’t', 'door', 'double', 'down', 'draw', 'dream', 'dress', 'drink', 'drive', 'drop', 'dry', 'duck', 'during', 'dylia', 'each', 'ear', 'early', 'earth', 'ease', 'east', 'eat', 'edge', 'effect', 'egg', 'eight', 'either', 'electric', 'element', 'else', 'end', 'enemy', 'energy', 'engine', 'enough', 'enter', 'equal', 'equate', 'especially', 'even', 'evening', 'event', 'ever', 'every', 'exact', 'example', 'except', 'excite', 'exercise', 'expect', 'experience', 'experiment', 'eye', 'face', 'facie', 'fact', 'facto', 'facts', 'fair', 'fall', 'falle', 'falls', 'false', 'family', 'famous', 'far', 'farm', 'fast', 'fat', 'father', 'favor', 'fear', 'feed', 'feel', 'feet', 'fell', 'felt', 'few', 'field', 'fig', 'fight', 'figure', 'fill', 'final', 'find', 'fine', 'finger', 'finish', 'fire', 'first', 'fish', 'fit', 'five', 'flat', 'floor', 'flow', 'flower', 'fly', 'follow', 'food', 'foot', 'for', 'force', 'forest', 'form', 'forward', 'found', 'four', 'fraction', 'free', 'fresh', 'friend', 'from', 'front', 'fruit', 'full', 'fun', 'game', 'garden', 'gas', 'gather', 'gave', 'general', 'gentle', 'get', 'girl', 'give', 'glad', 'glass', 'go', 'gold', 'gone', 'good', 'got', 'govern', 'grand', 'grass', 'gray', 'great', 'green', 'grew', 'ground', 'group', 'grow', 'guess', 'guide', 'gun', 'had', 'hair', 'half', 'hand', 'happen', 'happy', 'hard', 'has', 'hat', 'have', 'he', 'head', 'hear', 'heard', 'heart', 'heat', 'heavy', 'held', 'help', 'hence', 'her', 'here', 'high', 'hill', 'him', 'his', 'history', 'hit', 'hold', 'hole', 'home', 'hope', 'horse', 'hot', 'hour', 'house', 'how', 'however', 'hubei', 'huge', 'human', 'hundred', 'hunt', 'hurry', 'i', 'ice', 'idea', 'if', 'imagine', 'in', 'inch', 'include', 'india', 'indicate', 'industry', 'infrastructure', 'insect', 'instant', 'instrument', 'interest', 'invent', 'iron', 'is', 'isaac', 'islam', 'island', 'it', 'job', 'join', 'joy', 'jump', 'just', 'keep', 'kept', 'key', 'kill', 'kind', 'king', 'knew', 'know', 'korea', 'ks', 'lady', 'lake', 'land', 'language', 'large', 'last', 'late', 'laugh', 'law', 'lay', 'lead', 'learn', 'least', 'leave', 'led', 'left', 'leg', 'length', 'less', 'let', 'letter', 'level', 'lie', 'life', 'lift', 'light', 'like', 'line', 'liquid', 'list', 'listen', 'little', 'live', 'locate', 'log', 'lone', 'long', 'look', 'lost', 'lot', 'loud', 'love', 'low', 'machine', 'made', 'magnet', 'main', 'major', 'make', 'man', 'many', 'map', 'mark', 'market', 'mass', 'master', 'match', 'material', 'matter', 'may', 'me', 'mean', 'meant', 'measure', 'meat', 'media', 'meet', 'meets', 'melody', 'men', 'mercy', 'metal', 'method', 'middle', 'might', 'mile', 'milk', 'million', 'mind', 'mine', 'minute', 'miss', 'mix', 'modern', 'molecule', 'moment', 'money', 'month', 'moon', 'more', 'morning', 'most', 'mother', 'motion', 'mount', 'mountain', 'mouth', 'move', 'much', 'multiply', 'music', 'must', 'my', 'name', 'nation', 'natural', 'nature', 'nazis', 'near', 'necessary', 'neck', 'need', 'neighbor', 'never', 'new', 'newto', 'next', 'night', 'nine', 'no', 'noise', 'noon', 'nor', 'north', 'nose', 'note', 'nothing', 'notice', 'noun', 'now', 'number', 'numeral', 'object', 'observe', 'occur', 'ocean', 'of', 'off', 'offer', 'office', 'often', 'oh', 'oil', 'old', 'on', 'once', 'one', 'only', 'open', 'operate', 'opposite', 'or', 'order', 'organ', 'organisations', 'original', 'other', 'our', 'out', 'over', 'own', 'oxide', 'oxygen', 'ozone', 'page', 'paint', 'pair', 'paper', 'paragraph', 'parent', 'paris', 'part', 'particular', 'party', 'pass', 'past', 'patch', 'path', 'pattern', 'pay', 'people', 'perhaps', 'period', 'person', 'phrase', 'pick', 'picture', 'piece', 'pitch', 'place', 'plain', 'plan', 'plane', 'planet', 'plant', 'play', 'please', 'plural', 'poem', 'point', 'poor', 'populate', 'port', 'pose', 'position', 'possible', 'post', 'pound', 'power', 'practice', 'practitioners', 'prepare', 'present', 'press', 'pretty', 'print', 'probable', 'problem', 'process', 'produce', 'product', 'proper', 'property', 'protect', 'prove', 'provide', 'pull', 'push', 'put', 'quart', 'question', 'quick', 'quiet', 'quite', 'quotient', 'race', 'radio', 'rail', 'rain', 'raise', 'ran', 'range', 'rather', 'reach', 'read', 'ready', 'real', 'reason', 'receive', 'record', 'red', 'region', 'rehabilitated', 'remember', 'repeat', 'repercussions', 'reply', 'represent', 'require', 'responsibility', 'rest', 'result', 'rich', 'ride', 'right', 'ring', 'rise', 'river', 'road', 'rock', 'roll', 'room', 'root', 'rope', 'rose', 'round', 'row', 'rub', 'rule', 'run', 'safe', 'said', 'sail', 'salt', 'same', 'sand', 'sat', 'saudi', 'save', 'saw', 'say', 'scale', 'school', 'science', 'scientifically', 'score', 'sea', 'search', 'season', 'seat', 'second', 'section', 'see', 'seed', 'seem', 'segment', 'select', 'self', 'sell', 'send', 'sensationalise', 'sense', 'sent', 'sentence', 'separate', 'serve', 'set', 'settle', 'seven', 'several', 'shall', 'shape', 'share', 'sharp', 'she', 'sheet', 'shell', 'shine', 'ship', 'shoe', 'shop', 'shore', 'short', 'should', 'shoulder', 'shout', 'show', 'side', 'sight', 'sign', 'significantly', 'silent', 'silver', 'similar', 'simple', 'simultaneously', 'since', 'sing', 'single', 'sister', 'sit', 'six', 'size', 'skill', 'skin', 'sky', 'slave', 'sleep', 'slip', 'slow', 'small', 'smell', 'smile', 'snow', 'so', 'soft', 'soil', 'soldier', 'solution', 'solve', 'some', 'son', 'song', 'soon', 'sophisticated', 'sound', 'south', 'space', 'speak', 'special', 'speech', 'speed', 'spell', 'spend', 'spoke', 'spot', 'spread', 'spring', 'square', 'stand', 'star', 'start', 'state', 'station', 'stay', 'stead', 'steam', 'steel', 'step', 'stick', 'still', 'stone', 'stood', 'stop', 'store', 'story', 'straight', 'strange', 'stream', 'street', 'strengthening', 'stretch', 'string', 'strong', 'student', 'study', 'subject', 'substance', 'subtract', 'success', 'such', 'sudden', 'suffix', 'sugar', 'suggest', 'suit', 'summer', 'sun', 'supply', 'support', 'sure', 'surface', 'surprise', 'swim', 'syllable', 'symbol', 'system', 'table', 'tail', 'take', 'talk', 'tall', 'tamil', 'teach', 'team', 'technological', 'teeth', 'tell', 'temperature', 'ten', 'term', 'test', 'than', 'thank', 'that', 'the', 'their', 'them', 'then', 'there', 'these', 'they', 'thick', 'thin', 'thing', 'think', 'third', 'this', 'those', 'though', 'thought', 'thousand', 'three', 'through', 'throw', 'thus', 'tie', 'time', 'tiny', 'tire', 'to', 'together', 'told', 'tone', 'too', 'took', 'tool', 'top', 'total', 'touch', 'toward', 'town', 'track', 'trade', 'train', 'travel', 'treat', 'tree', 'trend', 'triangle', 'trip', 'trouble', 'truck', 'true', 'trust', 'try', 'tube', 'turn', 'twenty', 'twice', 'two', 'type', 'umber', 'under', 'unit', 'until', 'up', 'us', 'usage', 'use', 'using', 'usual', 'valley', 'value', 'vary', 'verb', 'very', 'video', 'view', 'village', 'visit', 'voice', 'vowel', 'wait', 'walk', 'wall', 'want', 'war', 'warm', 'was', 'wash', 'watch', 'water', 'wave', 'way', 'we', 'wear', 'weather', 'week', 'weeks', 'weight', 'well', 'went', 'were', 'west', 'what', 'wheel', 'when', 'where', 'whether', 'which', 'while', 'white', 'who', 'whole', 'whose', 'why', 'wide', 'wife', 'wild', 'will', 'win', 'wind', 'window', 'wing', 'winter', 'wire', 'wish', 'with', 'woman', 'women', 'wonder', 'won’t', 'wood', 'word', 'work', 'world', 'would', 'write', 'written', 'wrong', 'wrote', 'yard', 'year', 'yellow', 'yes', 'yet', 'you', 'young', 'your']

    
    print("CURRENT PDFS IN FOLDER:")
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            print(filename)
            pdfs_path.append(os.path.join(directory, filename))
        else:
            pass
    
    #----------------------------------------------------
    
    for pdf in pdfs_path:
        rawtext = pdfminer.high_level.extract_text(pdf)
        processedtext = repr(rawtext)
        for c in characters:
            processedtext = processedtext.replace(c, '')
        for i in processedtext.split(' '):
            data.append(i)
    
    for s in data: #s is a word
        word = s.strip('\n')
        word = word.strip('\\n')                    
        word = word.strip('\\n')
        word = word.replace('\\n', '')
        word = word.replace('\\t', '')
        word = word.replace('\\r', '')
        word = word.strip(' ')
        word = word.strip(',')
        word = word.strip('.')     

        if len(word) < 15 and len(word) > 4 and word.isalpha(): #can be changed
            for common in commons:
                if word.lower() == common.lower():
                    pass
                else:
                    uncommon.append(word)
        else:
            pass
        
    #----------------------------------------------------

    uniquewords = set(uncommon) #is a list
    
    sortedwords = quickSort(list(uniquewords)) #is a list
    
    countedwords = dict(Counter(sortedwords)) #is a dictionary

    #----------------------------------------------------

    lis = list(range(len(sortedwords)))
    with tqdm(total=len(sortedwords)) as p:
    
        for x in lis:

            w = sortedwords[x]
            
            definitions = dictionary.meaning(w)
            
            
            if definitions == None:
                pass
            
            else:

                try:
                    freq = countedwords[w]
                except:
                    freq = 1
                
                avail = definitions.keys()
                
                if 'Noun' in avail:
                    dic = {
                        'frequency': freq,
                        'word': w.upper(),
                        'definitions': definitions['Noun']}
                    dics.append(dic)
                        
                if 'Adjective' in avail:
                    dic = {
                        'frequency': freq,
                        'word': w.upper(),
                        'definitions': definitions['Adjective']}
                    dics.append(dic)

                if 'Verb' in avail:
                    dic = {
                        'frequency': freq,
                        'word': w.upper(),
                        'definitions': definitions['Verb']}
                    dics.append(dic)

                if 'Adverb' in avail:
                    dic = {
                        'frequency': freq,
                        'word': w.upper(),
                        'definitions': definitions['Adverb']}
                    dics.append(dic)

            try:
                p.update(1)
            except KeyboardInterrupt:
                print('interrupt')
                p.close()
    print(dics)
    
    #----------------------------------------------------'

    with open('definitions_of_words.csv', 'w', encoding='utf-8', newline='') as f:

        header = dics[0].keys()
        data = csv.DictWriter(f, fieldnames=header)
        data.writeheader()
        for dic in dics:
            if dic['frequency'] < 2 and dic['word']: #can be changed
                data.writerow(dic)
            else:
                pass
    
    return 'COMPLETED'

print(get_definitions_of_words_from_pdf())
