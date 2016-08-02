# Adam Knuckey
# August 2016
# Get Data from Lehigh's course site

import getpass,requests

s = requests.Session()

payload = {'username':raw_input('Username: '),'password':getpass.getpass('Password: ')}

r = s.get('https://coursesite.lehigh.edu/auth/saml/login.php') #Get the initial login page, which sets the MoodleSession cookie

r = s.get('https://coursesite.lehigh.edu/auth/saml/index.php?wantsurl=https%3A%2F%2Fcoursesite.lehigh.edu%2F',allow_redirects=True) #Follow the static link to the actual login page, which sets the PHP session ID

payload['RelayState'] = r.text[r.text.index('https://sso.cc.lehigh.edu/sso/module.php/core/'):r.text.index('https://sso.cc.lehigh.edu/sso/module.php/core/')+118] #Pull the 'RelayState' off of the page. It's a hidden value that is passed along with username and password when logging in

r = s.post(r.url+'?',data=payload,allow_redirects=True) #Call the same page again, this time with a post request containing your username, password, and the RelayState. This is what happens when the login form is submitted

payload = {'SAMLResponse': r.text[r.text.index('SAMLResponse" value="')+len('SAMLResponse" value="'):r.text.index('SAMLResponse" value="')+12650]} #The page redirects you to a different page after creating a SAMLRequest. The page you are redirected to contains a SAMLResponse code, which is pulled from the page and set as the payload, since it is passed to the next page in a post request

r = s.post("https://coursesite.lehigh.edu/simplesaml/module.php/saml/sp/saml2-acs.php/default-sp",data=payload,allow_redirects=True) #The final post request, which is passed the SAMLResponse. The page then redirects you to https://coursesite.lehigh.edu with all the necessary cookies/session vars to be logged in

print "Arrived at "+r.url+"!" #Logged in!

#From here you can use r.text or whatever python library to pull data off the page. When following links to other pages, make sure to use s.get(PAGE_URL) where PAGE_URL is the page url you want to go to
