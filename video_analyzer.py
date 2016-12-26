import json
import pprint
class VideoAnalyzer:
    """ This class Analyse the video and generates stats per video"""
    def __init__(self,videos,dictionary):
        # Have arguments just in case we needed later
        self.__videos = videos
        self.__dictionary = dictionary

        # Create dictionary of words and categories
        # { "video_word" : ["cat1","cat2",..] }
        print("Extracting words from all videos")
        self.__wordList = self.__extract_words(videos)
        print("Removing duplicated words")
        self.__unique_words = self.__remove_duplicates(self.__wordList)
        print("Creating words to categories dictionary")
        # self.__words_categories_dict = self.__map_video_words(self.__unique_words)
        self.__words_categories_dict = self.read_file('out/words_to_categories.json')
        self.__videos_per_category_dic = {}

        self.__video_processed = {}
        self.__mapped_words = {}
        self.__total_words_found = 0
        self.__total_videos_categorized = 0
        self.__total_videos_no_categorized = 0

    def total_videos(self):
        return len(self.__videos)

    def total_categories(self):
        return len(self.__dictionary)

    def total_words(self):
        return len(self.__wordList)

    def total_unique_words(self):
        return len(self.__unique_words)

    def total_words_missed(self):
        return self.__total_words - self.__total_words_found

    def total_videos_categorized(self):
        return self.__total_videos_categorized

    def total_videos_no_categorized(self):
        return self.__total_videos_no_categorized

    def words_dictionary(self):
        return self.__words_categories_dict

    def process_videos(self):
        result = []
        count = 0
        for v in self.__videos:
        # for i in range (0,5):
        #     v = self.__videos[i]

            count += 1
            print("Processing video",v["postId"], " [",count," of ", len(self.__videos)," ]")
            obj = {}
            total_words = len(v["wordList"])
            total_found = 0
            total_missed = 0
            # Get categories
            video_cat = {}
            for word in v["wordList"]:
                cats = self.get_categories(word)
                if len(cats) > 0:
                    video_cat = self.__add_video_to_categories(cats,video_cat)
                    # video_cat.extend(self.get_categories(word))
                    total_found += 1
                else:
                    total_missed += 1

            # remove repeated
            # video_cat = self.__remove_duplicates(video_cat)

            if len(video_cat) == 0:
                self.__total_videos_no_categorized += 1
            else:
                self.__total_videos_categorized += 1

            # add video to category
            self.__videos_per_category_dic = self.__add_video_to_categories(video_cat,self.__videos_per_category_dic)

            obj = {
                "postId" : v["postId"],
                "total_words" : total_words,
                "total_words_found" : total_found,
                "total_words_missed" : total_missed,
                "total_categories" : len(video_cat),
                "categories" : video_cat
            }
            result.append(obj)
        self.__video_processed = result

    def __add_video_to_categories(self,categories,full_object):
        for cat in categories:
            if len(full_object) > 0:
                if cat in full_object:
                    full_object[cat] += 1
                else:
                    full_object[cat] = 1
            else:
                full_object[cat] = 1
        return full_object

    def summary(self):
        return {
            "stats" : {
                "total_videos" : self.total_videos(),
                "total_categories" : self.total_categories(),
                "total_words" : self.total_words(),
                "total_unique_words" : self.total_unique_words(),
                "videos_categorized" : self.total_videos_categorized(),
                "videos_no_categorized": self.total_videos_no_categorized()
            },
            "categories_per_videos": self.__video_processed,
            "videos_per_category": self.__videos_per_category_dic
        }

    def save_words_to_categories(self,path):
        with open(path, 'w') as fp:
            json.dump(self.words_dictionary(),fp)

    def read_file(self,path):
        with open(path) as data_file:
            data = json.load(data_file)
        return data

    def save_summary(self,path):
        with open(path, 'w') as fp:
            json.dump(self.summary(),fp)

    def get_categories(self,word):
        result = []
        for i in range (0,len(self.__dictionary)):
            for category,words in self.__dictionary[i].items():
                if any(word in s for s in words):
                    result.append(category)

        if len(result) > 0:
            return result[0:1]
        else:
            return result
        return result

    # Private methods

    # Return dictionary of words and categories
    def __map_video_words(self,words):
        # Create dictionary
        d = {}
        for word in words:
            d[word] = self.get_categories(word)
        return d


    #Return array with all the words no repeated
    def __extract_words(self,videos):
        wordsList = []
        for video in videos:
            wordsList.extend(video['wordList'])
        return wordsList

    def __remove_duplicates(self,words):
        return list(set(words))
