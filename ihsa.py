import urllib
import time

def getSchoolName(stringPage):#get name of school from h1 tags
	schoolNameIndex = stringPage.find("<H1>") + len("<H1>")#move to start of school name
	#print(stringPage[schoolNameIndex])
	schoolNameEndIndex = stringPage.find("</H1>", schoolNameIndex)
	return(stringPage[schoolNameIndex:schoolNameEndIndex])


def getCoachInfo(stringPage):#get coach name and email by searching for sport name

	coachNameIndex = stringPage.find("Boys Wrestling")
	if(coachNameIndex == -1):#exit function with empty return code if school does not have sport
		return("")
	coachNameIndex += len("Boys Wrestling Head Coach</B>: ")#move to start of coach name
	coachNameEndIndex = stringPage.find('&', coachNameIndex)
	coachName = stringPage[coachNameIndex:coachNameEndIndex]
	
	if(coachName.find("TBA")!=-1):
		return("")#if coach is TBA, skip school

	
	coachEmailIndex = coachNameEndIndex + len("&nbsp;<A HREF='mailto:")
	coachEmailEndIndex = stringPage.find('"', coachEmailIndex)
	coachEmail = stringPage[coachEmailIndex:coachEmailEndIndex]

	return(coachName + ", " + coachEmail)

#start acual program
final_txt = open("IHSA.txt","w+")
num1 = ""
num2 = ""
for alpha in range(1,27): # interate through each letter
	if(alpha<10):#pad num1 to 2 digits minimum
		num1 = "0"+str(alpha)
	else:
		num1 = str(alpha)


	subNum = 1 # subletter index tracker
	print(alpha)
	count404 = 0
	while(True): #each letter has a differeent number of schools, go until 404ing
	
		if(count404>5):#wait until 5 404s in a row to go on to next letter
			break
			
		time.sleep(.1)
		if(subNum<10):#pad num2 to 2 digits minimum
			num2 = "0"+str(subNum)
		else:
			num2 = str(subNum)

		#print(num1, num2)
		
		subNum += 1
		URL = "https://www.ihsa.org/data/school/schools/"+num1+num2+".htm"
		page = urllib.urlopen(URL)
		stringPage = page.read()#.decode("utf-8")#load webpage as string
		
		if(stringPage.find("The page you are attempting to view has not been posted yet")!=-1):#move onto next letter once url 404s
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
