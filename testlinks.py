import sys, requests, json, re, datetime, argparse
from lxml import html

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--output')

args = parser.parse_args()

links = []
for line in sys.stdin:
    line = line.strip()
    r = requests.get(line)    
    tree = html.fromstring(r.content)
    title = tree.find(".//title").text
    preview = tree.xpath("//img[@class='freebirdFormviewerViewItemsEmbeddedobjectImage']/@src")
    if preview:
        preview = preview[0]
    datematch = re.search('^\s*(\d{1,2}/\d{1,2})', title)
    date = datematch.group(0) 
    dated = datetime.datetime.strptime(date,'%m/%d').replace(year=2021) 
    links.append({
        "date" : dated.timestamp(),
        "url" : line,
        "title" : title,
        "preview" : preview
    })
    print("Downloaded {0}".format(title))
    
def sbDate(e):
    return e['date']    

links.sort(key=sbDate)

outputfile = ""
print("Building HTML...")
for link in links:
    linkstr = '''
        <div class="col">
            <div class="card">
                <img src="{preview}" class="card-img-top" style="height:300px;object-fit:contain" />
                <div class="card-body"> 
                    <h5 class="card-title">{title}</h5>
                    <a class="btn btn-primary" href="{link}">Vote</a>                
                </div>
            </div>
        </div>
    '''
    outputfile += linkstr.format(link=link['url'], preview=link['preview'], title=link['title'])
    # print(linkstr.format(link=link['url'], preview=link['preview'], title=link['title']))
print("Writing...")
if args.output:
    f = open(args.output, "w")
    f.write(outputfile)
    f.close()