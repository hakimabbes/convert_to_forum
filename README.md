# convert_to_forum
A simple project to format posts to communicate on various forums in different languages. 

The main input text to transform is the japan_expo2017_AMVFRANCE.txt.
The code is based on a dictionary that you can enrich as you want in Forum_dict.xlsx. 
Each column will get you an output for a template. 

The code uses REGEX to modify the dates so the change_date function will likely not work as expected on any text. 

#Usage

Open main_convert_to_forum and change first the home directory to the path where you dumped every input.
Input the text file name, the Japan Expo deadline, the last day of Japan Expo and the new ID of the contest (on the www.amv-france.com website). 
Then run and enjoy the text files output in the home directory you input.

But don't forget to check if everything looks fine! 
