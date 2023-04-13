import urllib
import time

def getSchoolName(stringPage):#get name of school from h1 tags
	schoolNameIndex = stringPage.find('<label class="JumboMain">') + len('<label class="JumboMain">')#move to start of school name
	#print(stringPage[schoolNameIndex])
	schoolNameEndIndex = stringPage.find("</label>", schoolNameIndex)
	return(stringPage[schoolNameIndex:schoolNameEndIndex])

def getCoachInfo(stringPage):#get coach name and email by searching for sport name

	SportIndex = stringPage.find("Wrestling</label></td>")
	if(SportIndex == -1):#exit function with empty return code if school does not have sport
		return("")
	coachNameIndex = stringPage.find('modal"><b>', SportIndex) + len('modal"><b>')#move to start of coach name
	coachNameEndIndex = stringPage.find("</b>", coachNameIndex)
	coachName = stringPage[coachNameIndex:coachNameEndIndex].replace("<span>&nbsp;</span>", " ")
	
	
	coachEmailIndex = stringPage.find('mailto:',coachNameEndIndex) + len('mailto:')
	coachEmailEndIndex = stringPage.find('"', coachEmailIndex)
	coachEmail = stringPage[coachEmailIndex:coachEmailEndIndex]

	return(coachName + ", " + coachEmail)

#start acual program
final_txt = open("WAII.txt","w+")
num = 0
count404 = 0
while(True): #each letter has a differeent number of schools, go until 404ing

	num +=1
	
	print(num%50)
	
	if(num%50==0):
		print(num)
	
	if(count404>5):#wait until 5 404s in a row to go on to next letter
		break
		
	time.sleep(.2)
	URL = "https://schools.wiaawi.org/Directory/School/GetDirectorySchool?orgID=" + str(num)
	page = urllib.urlopen(URL)
	stringPage = page.read()#.decode("utf-8")#load webpage as string
	
	if(stringPage.find('<label class="JumboMain"></label>')!=-1):#move onto next letter once url 404s
		#print("404d "+URL)
		count404 += 1
		continue
	else:
		count404 = 0#reset counter if no 404
	
	
	coachName = getCoachInfo(stringPage)
	if(coachName==""):
		#print("skipped school")
		continue#skip school if no sport
	schoolName = getSchoolName(stringPage)
	
	#print(schoolName + ", "+coachName)
	final_txt.write(schoolName + ", "+coachName+"\n")
	
final_txt.close()
