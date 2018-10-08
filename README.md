Description:

This will count the frequency of words in a body of text.   It also has the ability to download all the text from an entire website or a single URL.  Once the text is downloaded you can analyze the text's word frequency.  

Example usage:

Sample output from Ku Klux Klan’s websites
https://motiondesignstudio.wordpress.com/2016/03/14/word-frequency-on-ku-klux-klans-websites/

#Download a website using the sitemap and display its text without html
example=wordFrequency(url="http://myurl.net/sitemap.xml")
example.crawl_sitemap( retry_rate=15) 

#Download ALL the pages from a website and display its text without html
example=wordFrequency(url="http://mustpassarobotsfile.com/")
example.scrape_all_websites_text( link_regex='/*', max_depth=-1, retry_rate = 15, robots_file='http://mustpassarobotsfile.com/robots.txt' )

#Download a SINGLE webpage and display its text without html
example=wordFrequency(url="http://myurl.net/")
print ( example.display_text_only( ) )

#Download a SINGLE webpage and display its text
example=wordFrequency(url="http://myurl.net/")
print ( example.download( num_retries=2 ) )


#Search for specific amount of words left or right of a specified word
example=wordFrequency(file_source="my_text_file.txt", number_to_display = 20)
print ( example.get_surrounding_words("Christmas", 4, 4) )

#Search for words and display word frequncy in a local text file
#example=wordFrequency(file_source="localTextFile.txt", number_to_display = 20)
#print ( example.frequency_in_file() )

The downloaded pages require some additional cleaning.  

] Use this to clean data [

This line is an attempt to clean the output in one command.

perl -pe 's/<url :::.*?<\/url>//g'  <o1.txt | sed -re 's/\\\\n/ /g;s/\\\\t/ /g;s/\\\\r/ /g;s/\\n/ /g;s/\\\\x[^\\]*/ /g;s/\\x[^\\]*/ /g;s/\('\'''\'', "b'\''//g;'  > o3.txt

To remove this >  ('', "b'   do below.

sed -re $'s/[(]\'\', \"b\'//g' < o3.txt > o4.txt

('', 'b'

sed -re $'s/[(]\'\', \'b\'//g' < o4.txt > o5.txt

To remove \\\'

sed -r "s/\\\\\\\'/\'/g" <o5.txt >o6.txt

To remove \'

sed -r "s/\\\'/\'/g" <o6.txt >o7.txt

] Very Important [

Do not set retry_rate = 15 below 15 you might get banned from a website.

When you scrape an entire website always check to see if they have a robots files and set it like this.

robots_file='http://mustpassarobotsfile.com/robots.txt

These files are necessary stopwords.txt and default_robots.txt.

] Future Functionality [

- Examine the most common word(s) shared by different outputs?
- Search for a string frequency such “Acrobatic Yoga”
- Count and list how many links a website has
- Search for call to action words
- Search for pronouns to predict the writes gender and mindset
