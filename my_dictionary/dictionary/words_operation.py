from datetime import date, timedelta
from .models import Words
from random import randint
from loguru import logger
from django.db.models import Q

class Corrector():
    def __levenshtein_distance(self, s1, s2):
        d = {}
        lenstr1 = len(s1)
        lenstr2 = len(s2)
        for i in range(-1,lenstr1+1):
            d[(i,-1)] = i+1
        for j in range(-1,lenstr2+1):
            d[(-1,j)] = j+1

        for i in range(lenstr1):
            for j in range(lenstr2):
                if s1[i] == s2[j]:
                    cost = 0
                else:
                    cost = 1
                d[(i,j)] = min(
                            d[(i-1,j)] + 1, # deletion
                            d[(i,j-1)] + 1, # insertion
                            d[(i-1,j-1)] + cost, # substitution
                            )
                if i and j and s1[i]==s2[j-1] and s1[i-1] == s2[j]:
                    d[(i,j)] = min (d[(i,j)], d[i-2,j-2] + cost) # transposition
        return d[lenstr1-1,lenstr2-1]

    def __mark_difference(self, users_str, correct_str, start_mark, end_mark):
        #start and end of discrepancy
        index_1 = len(correct_str)-1
        index_2 = 0
        #is discrepancy index is les than null
        ltn = False
        #is discrepancy index is more than end
        mte = False
        #go from the start
        for c in range(len(correct_str)):
            if users_str[c] != correct_str[c]:
                index_1 = c
                break
            elif c==len(users_str)-1:
                #when users string is over, but discrepancy has not found
                #means that the inded of the next symbol is discrepancy
                index_1 = c+1
                break
        else:
            #when loop is over, but discrepancy has not found
            #means that users's string contain discrepancy after
            #the last symbol
            mte = True

        #go through the string from end and do the same
        for c in range(len(correct_str)):
            i = -c-1
            if users_str[i] != correct_str[i]:
                index_2 = len(correct_str)+i
                break
            elif len(users_str)==-i:
                #previous index is end of discrepancy
                index_2=len(correct_str)+i+1
                break
        else:
            ltn = True

        start_index = min(index_1, index_2)
        end_index = max(index_1, index_2)

        if ltn and (end_index == 1):
            #aassasin-assasin
            #|id|0123456|
            #|cr|assasin|
            #|fs|a      |
            #|fe|assasin|
            #|po|*      |
            end_index=0
        elif ltn and (end_index == 2):
            #qqqwerty-qqwerty
            #|id|0123456|
            #|cr|qqwerty|
            #|fs|qq     |
            #|fe|qqwerty|
            #|po|**     |
            end_index=1
        elif mte and (start_index == len(correct_str)-2):
            #qwertyy-qwerty
            #|id|012345|
            #|cr|qwerty|
            #|fs|qwerty|
            #|fe|     y|
            #|po|     *|
            start_index=len(correct_str)-1
        elif mte and (start_index == len(correct_str)-3):
            #qwertyyy-qwertyy
            #|id|0123456|
            #|cr|qwertyy|
            #|fs|qwertyy|
            #|fe|     yy|
            #|po|     **|
            start_index=len(correct_str)-2
        elif(start_index != end_index) and (start_index+1 != end_index):
                start_index += 1
                end_index -= 1
        marked_string = correct_str[:start_index] + start_mark + correct_str[start_index:end_index+1] + end_mark + correct_str[end_index+1:]
        return marked_string

    def check_answer(self, users_str, correct_str, start_mark, end_mark):
        if users_str == correct_str:
            return 1
        elif len(correct_str)<4:
            return 0
        else:
            levenshtein_distance = self.__levenshtein_distance(users_str, correct_str)
            if levenshtein_distance == 1:
                return self.__mark_difference(users_str, correct_str, start_mark, end_mark)
            else:
                return 0


class TestItem:
    def __init__(self, user_id):
        self.user_id = user_id

    @logger.catch
    def make_question(self, random=True):
        word = self._get_word(random)
        if word == '':
            return False
        else:
            self._question = {
                'id':word.id,
                'answer':word.foreign_word,
                'russian_word':word.russian_word,
                'help':''
            }
            if word.context == '':
                self._question['question'] = word.russian_word
                self._question['read_aloud'] = word.foreign_word
            else:
                self._question['question'] = word.context.replace(word.foreign_word, f'({word.russian_word})')
                self._question['read_aloud'] = word.context.replace(word.foreign_word, f'<b>{word.foreign_word}</b>')
            return True


    def send_card(self, word_id, is_remembered):
        self._change_boxes(word_id, is_remembered)

    def set_question(self, question):
        self._question = question

    def get_question(self):
        return self._question

    def send_users_answer(self, user_answer, help, starc_mark, end_mark):
        self.help = help
        self.user_answer = user_answer
        self._is_users_answer_correct = self._check_answer(starc_mark, end_mark)

    def is_users_answer_correct(self):
        return self._is_users_answer_correct

    @logger.catch
    def _check_answer(self, starc_mark, end_mark):
    #seems stupid, but in prospect here will be more smart algoritm taking into account
    #typo, registr (in some languages it does matter), translit etc
        corector = Corrector()
        corection_result = corector.check_answer(self.user_answer, self._question['answer'], starc_mark, end_mark)
        
        if corection_result == 0:
            return False
        else:
            if self.help != '':
                help_used = False
            else:
                help_used = True
            self._change_boxes(self._question['id'], help_used)
            if corection_result != 1:
                if self._question['read_aloud'] != self._question['answer']:
                    self._question['read_aloud'] = self._question['read_aloud'].replace(self._question['answer'], corection_result)
                else:
                    self._question['read_aloud'] = corection_result

            return True


    def _change_boxes(self, word_id, is_next_box):
        word = Words.objects.filter(pk=word_id, user_id=self.user_id).first()
        if not is_next_box:
            word.box_number = 0
        else:
            if word.box_number != 6:
                word.box_number = word.box_number + 1
        word.asking_date=self._get_revise_date(word.box_number)
        word.save(update_fields = ["asking_date", "box_number"])

    def get_help(self):
        if self.help == "":
            self.help = '*'*len(self._question['answer'])
        index = self.help.find('*')
        if index != -1:
            self.help = self._question['answer'][:index+1]+((len(self.help)-index-1)*'*')
        return self.help

    def _get_word(self, random):
        try:
            today_date = date.today()
            relevant_words = Words.objects.filter(asking_date__lte=today_date, user_id=self.user_id)
            if random:
                relevant_words = relevant_words.order_by('?')
            if relevant_words.exists():
                word = relevant_words.first()
            else:
                word = ""
        except Exception as error:
            word = ""
            logger.error(f'Method get_word. Error {str(error)}')
        finally:
            return word    

    def _get_revise_date(self, box_number):
        today_date = date.today()
        if box_number == 0:
            interval = timedelta(days=1)
        elif box_number == 1:
            interval = timedelta(days=2)
        elif box_number == 2:
            interval = timedelta(days=3)
        elif box_number == 3:
            interval = timedelta(days=7)
        elif box_number == 4:
            interval = timedelta(days=14)
        elif box_number == 5:
            interval = timedelta(days=30)
        elif box_number == 6:
            interval = timedelta(days=randint(30,40))    
        return today_date+interval

@logger.catch
def get_words_list(user_id, search_query):
    words_list = Words.objects.filter(user_id=user_id)
    search_query = search_query.replace(' ', '')
    if search_query != "":
        words_list = words_list.filter(
                Q(russian_word__icontains=search_query) |
                Q(foreign_word__icontains=search_query) |
                Q(foreign_word__icontains=search_query)
            )
    return words_list

@logger.catch
def get_dictionary_statistics(user_id):
    words_list = Words.objects.filter(user_id=user_id)
    statistics = {
        'words_total_number':words_list.count(),
        'words_for_today_number':words_list.filter(asking_date__lte=date.today()).count(),
        'learned_words_number':words_list.filter(box_number=6).count()
    }
    return statistics
