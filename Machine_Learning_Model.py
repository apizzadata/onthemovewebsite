import numpy as np
import scipy
from sklearn import neighbors
import sys
import pickle
import csv
import os

'''
Variables:
	Sex: 1 or 2
	1 is Male
	2 is Female
	Age: number
	COB: Country of Birth Code.
	Occupation: Occupation Code.
	HEAP: Highest Education Leveal Achieved Code.
	Industry_Code: Industry Code.
Make sure you unzipped the files in one place.
'''

current_dir = os.getcwd()
#print current_dir

class Model:
	def __init__(self, Sex, Age, COB, Occupation, HEAP, Industry_Code):
		self.Sex = Sex
		self.COB = COB
		self.Occupation = Occupation
		self.HEAP = HEAP
		self.Industry_Code = Industry_Code
		try:
			self.Age = int(Age)
		except ValueError:
			print "Age needs to be a number"
		if self.Age < 30:
			self.Age_group = 29
		elif 30 <= self.Age <= 39:
			self.Age_group = 3039
		elif 40 <= Age <= 49:
			self.Age_group = 4049
		else:
			self.Age_group = 5099

		self.State_dict = {1:'New South Wales', 2:'Victoria', 3:'Queensland', 4:'South Australia', 5:'Western Australia', 6:'Tasmania', 7:'Northern Territory', 8:'Australian Capital Territory'}
	
	def Predict(self):
		self.xdata = np.array([self.Sex, self.Age_group, self.COB, self.Occupation, self.HEAP, self.Industry_Code])
		with open(current_dir+'\MLModel.pkl', 'rb') as f:
			clf = pickle.load(f)
			self.ycode = clf.predict(self.xdata)

		try:
			self.yresult = self.State_dict[int(self.ycode[0])]
			print "The majority of people with a similar background works in this state: "
			print self.yresult
		except:
			print "Model did not output a valid result"

	def JobList(self):
		self.State_dict_Abv = {1:'NSW', 2:'VIC', 3:'QLD', 4:'SA', 5:'WA', 6:'TAS', 7:'NT', 8:'ACT'}
		self.State_Abv = ['NSW', 'VIC', 'QLD', 'SA', 'WA', 'TAS', 'NT', 'ACT']
		State = self.State_dict_Abv[int(self.ycode[0])]
		jobdata = []
		with open(current_dir+'\JPO-coded.csv') as csvfile:
			contents = csv.reader(csvfile, delimiter=",")
			for row in contents:
				jobdata.append(row)
		jobdataa = np.array(jobdata)
		header = jobdata[0]
		joblist = np.array(filter(lambda jobdatai: self.State_dict_Abv[int(self.ycode[0])] == jobdatai[10], jobdataa))
		with open(current_dir+'\Jobs.csv', 'wb') as f:
			writer = csv.writer(f)
			writer.writerow(header)
			for jobi in joblist:
				writer.writerow(jobi)
    		f.close()
    		print "The list of jobs under " + self.yresult + " are saved in 'Jobs.csv' file"
		
if __name__ == "__main__":
	print "What is your gender? Type 1 for Male and 2 for Female"
	Sex = raw_input()
	print "How old are you? Please type an integer",
	Age = raw_input()
	print "What is your country of birth? Please type the country code from the 'Country of Birthd Information.txt' file. For example 22 is Ireland"
	COB = raw_input()
	print "What is your current or most recent occupation? Please type the Occupation code from the 'Occupation List.txt' file. For example 132 is 'Business Administration Managers'"
	Occupation = raw_input()
	print "What is your highest education level? Please type the Education Level code from the 'Education Level Information.txt' file. For example 31 is 'Bachelor Degree Level'"
	HEAP = raw_input()
	print "What is your current or most recent industry? Please type the Industry code from the 'Industry List.txt' file. For example 62 is 'Finance'"
	Industry_Code = raw_input()
	MLModel = Model(Sex, Age, COB, Occupation, HEAP, Industry_Code)
	
	#MLModel = Model(2, 28, 21, 132, 31, 62)
	
	MLModel.Predict()
	MLModel.JobList()
