import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import roc_curve, auc

import json
import pandas as pd
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud


traindata = pd.read_json('traindata.json')
count_vect = CountVectorizer()
x_train_counts = count_vect.fit_transform(traindata['text'])
print(x_train_counts.todense())

tfidf_trans = TfidfTransformer()
x_train_tfidf = tfidf_trans.fit_transform(x_train_counts)

print(x_train_tfidf)
devdata = pd.read_json('devdata.json')
print(devdata.iloc[[1]])

clf = SVC(gamma='auto')
clf.fit(x_train_tfidf,traindata['class'])

x_dev_counts = count_vect.transform(devdata['text'])

x_dev_tfidf = tfidf_trans.transform(x_dev_counts)
predicted = clf.predict(x_dev_tfidf)
print(np.mean(predicted == devdata['class']))
devdata.insert(2,"Prediction",predicted,True)
print(devdata)
devdata.to_csv('testres3.csv',index=False)

rtc = RandomForestClassifier(max_depth=12, random_state=0)
rtc.fit(x_train_tfidf, traindata['class'])
predicted2 = rtc.predict(x_dev_tfidf)
print(np.mean(predicted2 == devdata['class']))
devdata.insert(3,"RT Prediction",predicted,True)
print(devdata)
devdata.to_csv('testres2.csv',index=False)
print(rtc.feature_importances_)

featurelst = []
for i in range(0,len(rtc.feature_importances_)):
    if rtc.feature_importances_[i] != 0:
        featurelst.append((rtc.feature_importances_[i],count_vect.get_feature_names()[i]))
featurelst.sort()
print(featurelst)

# fprclf, tprclf = roc_curve(devdata['class'],predicted,pos_label="r/nba")
# roc_auc = auc(fprclf,tprclf)
#
# fprrtc, tprrtc = roc_curve(devdata['class'],predicted2,pos_label="r/nba")
# roc_auc2 = auc(fprrtc,tprrtc)

# plt.figure()
# lw = 2
# plt.plot(fprclf, tprclf, color='darkorange',
#          lw=lw, label='SVM ROC curve (area = %0.2f)' % roc_auc)
# plt.plot(fprrtc, tprrtc, color='yellow',
#          lw=lw, label='Random Forest ROC curve (area = %0.2f)' % roc_auc2)
# plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
# plt.xlim([0.0, 1.0])
# plt.ylim([0.0, 1.05])
# plt.xlabel('False Positive Rate')
# plt.ylabel('True Positive Rate')
# plt.title('Receiver operating characteristic example')
# plt.legend(loc="lower right")
# plt.show()

# svmlst = []
# for i in range(0,len(clf.)):
#     if rtc.feature_importances_[i] != 0:
#         featurelst.append((rtc.feature_importances_[i],count_vect.get_feature_names()[i]))
# featurelst.sort()
# print(featurelst)

wcstr = ""
for row in traindata['text']:
    wcstr += " " + row

wordcloud = WordCloud().generate(wcstr)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()

