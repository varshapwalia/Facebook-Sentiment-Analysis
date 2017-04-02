#please sir run it in python 2.7 enviroment

import urllib2
import json
import datetime
import csv
import time

#app_id = "<FILL IN>"
#app_secret = "<FILL IN>"
group_id = raw_input("Please Paste Public Group ID:")

#access_token = app_id + "|" + app_secret
access_token = raw_input("Please Paste Your Access Token:")
def request_until_succeed(url):
    req = urllib2.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib2.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception, e:
            print e
            time.sleep(5)

            print "Error for URL %s: %s" % (url, datetime.datetime.now())
            print "Retrying."

    return response.read()

def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22, 0x201D:0x22,
                            0xa0:0x20 }).encode('utf-8')

def getFacebookPageFeedData(group_id, access_token, num_statuses):

    # Construct the URL string;
    
    base = "https://graph.facebook.com/v2.8"
    node = "/%s/feed" % group_id 
    fields = "/?fields=message,link,permalink_url,created_time,type,name,id," + \
            "comments.limit(0).summary(true),shares,reactions." + \
            "limit(0).summary(true),from"
    parameters = "&limit=%s&access_token=%s" % (num_statuses, access_token)
    url = base + node + fields + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data

def getReactionsForStatus(status_id, access_token):


        # Reactions are only accessable at a single-post endpoint

    base = "https://graph.facebook.com/v2.6"
    node = "/%s" % status_id
    reactions = "/?fields=" \
            "reactions.type(LIKE).limit(0).summary(total_count).as(like)" \
            ",reactions.type(LOVE).limit(0).summary(total_count).as(love)" \
            ",reactions.type(WOW).limit(0).summary(total_count).as(wow)" \
            ",reactions.type(HAHA).limit(0).summary(total_count).as(haha)" \
            ",reactions.type(SAD).limit(0).summary(total_count).as(sad)" \
            ",reactions.type(ANGRY).limit(0).summary(total_count).as(angry)"
    parameters = "&access_token=%s" % access_token
    url = base + node + reactions + parameters

    # retrieve data
    data = json.loads(request_until_succeed(url))

    return data


def processFacebookPageFeedStatus(status, access_token):

    # The status is now a Python dictionary, 

   

    status_id = status['id']
    status_message = '' if 'message' not in status.keys() else \
            unicode_normalize(status['message'])
    link_name = '' if 'name' not in status.keys() else \
            unicode_normalize(status['name'])
    status_type = status['type']
    status_link = '' if 'link' not in status.keys() else \
            unicode_normalize(status['link'])
    status_permalink_url = '' if 'permalink_url' not in status.keys() else \
            unicode_normalize(status['permalink_url'])
    status_author = unicode_normalize(status['from']['name'])

  

    status_published = datetime.datetime.strptime(\
            status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) # EST
    # best time format for spreadsheet programs:
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S')

    # Nested items require chaining dictionary keys.

    num_reactions = 0 if 'reactions' not in status else \
            status['reactions']['summary']['total_count']
    num_comments = 0 if 'comments' not in status else \
            status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status else \
            status['shares']['count']

    # Counts of each reaction separately;
   
    reactions = getReactionsForStatus(status_id, access_token) \
            if status_published > '2016-02-24 00:00:00' else {}

    num_likes = 0 if 'like' not in reactions else \
            reactions['like']['summary']['total_count']

   

    num_likes = num_reactions if status_published < '2016-02-24 00:00:00' else \
            num_likes

    def get_num_total_reactions(reaction_type, reactions):
        if reaction_type not in reactions:
            return 0
        else:
            return reactions[reaction_type]['summary']['total_count']

    num_loves = get_num_total_reactions('love', reactions)
    num_wows = get_num_total_reactions('wow', reactions)
    num_hahas = get_num_total_reactions('haha', reactions)
    num_sads = get_num_total_reactions('sad', reactions)
    num_angrys = get_num_total_reactions('angry', reactions)

    # return a tuple of all processed data

    return (status_id, status_message, status_author, link_name, status_type, 
            status_link, status_permalink_url, status_published, num_reactions, num_comments, 
            num_shares,  num_likes, num_loves, num_wows, num_hahas, num_sads, 
            num_angrys)

def scrapeFacebookPageFeedStatus(group_id, access_token):
    with open('%s_facebook_statuses.csv' % group_id, 'wb') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "status_message", "status_author", 
            "link_name", "status_type", "status_link","permalink_url",
            "status_published", "num_reactions", "num_comments", 
            "num_shares", "num_likes", "num_loves", "num_wows", 
            "num_hahas", "num_sads", "num_angrys"])

        has_next_page = True
        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()

        print "Scraping %s Facebook Page: %s\n" % \
                (group_id, scrape_starttime)

        statuses = getFacebookPageFeedData(group_id, access_token, 100)

        while has_next_page:
            for status in statuses['data']:

                # Ensure it is a status with the expected metadata
                if 'reactions' in status:            
                    w.writerow(processFacebookPageFeedStatus(status, \
                                                            access_token))

                # output progress occasionally to make sure code is not
                # stalling
                num_processed += 1
                if num_processed % 100 == 0:
                    print "%s Statuses Processed: %s" % (num_processed, 
                            datetime.datetime.now())

            # chech for next page
            if 'paging' in statuses.keys():
                statuses = json.loads(request_until_succeed(\
                        statuses['paging']['next']))
            else:
                has_next_page = False


        print "\nDone!\n%s Statuses Processed in %s" % \
                (num_processed, datetime.datetime.now() - scrape_starttime)


if __name__ == '__main__':
    scrapeFacebookPageFeedStatus(group_id, access_token)



