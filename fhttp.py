import re

st = '''
1
2 http://www.sina.com 3  
4 https://www.sina.com 5 
6 http://doershd.com/wp-content/uplpaper.jpg 8
9 https://doershd.com/wp-content/uplpaper.png 10
11 http://doershd.com/wp-content/uplpaper.gif 12
dklskjaf
'''
html_text = st
http_link = re.compile(r'http[s]?://[^\s]+')
http_img = re.compile(r'.jpg|.png|.gif')
hs = http_link.findall(st)
for h in hs:
    if http_img.search(h):
        img = '<br><img border="0" src="%s" width="600" height="450"><br>' %h
        orl = re.compile(h)
        html_text = orl.sub(img,html_text)
        print img
    else:
        text = '<a href="%s">%s</a>' %(h, h)
        orl = re.compile(h)
        html_text = orl.sub(text,html_text)
        print text

print '========================'
print html_text
print '========================'
line = re.compile(r'\n+')
html_text = line.sub('<br>',html_text)
print '========================'
print html_text
    
