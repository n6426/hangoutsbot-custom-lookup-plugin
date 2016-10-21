import logging
import hangups

from utils import unicode_to_ascii
import urllib.request

import plugins

logger = logging.getLogger(__name__)


def _initialise(bot):
    plugins.register_user_command(["lookup"])


def lookup(bot, event, *args):
    """find keywords in a specified spreadsheet"""

    if not bot.get_config_suboption(event.conv_id, 'spreadsheet_enabled'):
        yield from bot.coro_send_message(event.conv, _("Spreadsheet function disabled"))
        return

    """if not bot.get_config_suboption(event.conv_id, 'spreadsheet_url'):
        yield from bot.coro_send_message(event.conv, _("Spreadsheet URL not set"))
        return"""

    spreadsheet_url_this = bot.get_config_suboption(event.conv_id, 'spreadsheet_url_this')
    spreadsheet_url_next = bot.get_config_suboption(event.conv_id, 'spreadsheet_url_next')
    table_class = "waffle" # Name of table class to search. Note that 'waffle' seems to be the default for all spreadsheets
    search = 1
    keyword = ''

    if args[0].startswith('help'):
        htmlmessage = _('<b>lookup this "<keyword>"</b> will return the schedule for this week <br /> <b>lookup next "<keyword>"</b> will return the schedule for next week <br /> <b>lookup "<keyword>"</b> will return the schedule for both weeks <br /> <b>lookup help</b> will show this message')
        search = 0
    elif args[0].startswith('<'):
        counter_max = int(args[0][1:]) # Maximum rows displayed per query
        keyword = ' '.join(args[1:])
    else:
        counter_max = 50
        keyword = ' '.join(args)
    
    week_this = 0
    week_next = 0

    if 'this' in keyword:
        week_this = 1
        keyword =keyword.replace('this','')
    elif 'next' in keyword:
        week_next = 1
        keyword =keyword.replace('next','')
    else:
        week_this = 1 #defaults to search all
        week_next = 1 #defaults to search all

    if search == 1:
        htmlmessage = _('Results for keyword <b>{}</b>:<br />').format(keyword)

        logger.debug("{0} ({1}) has requested to lookup '{2}'".format(event.user.full_name, event.user.id_.chat_id, keyword))

        keyword_raw = keyword.strip().lower()
        keyword_ascii = unicode_to_ascii(keyword_raw)

        counter = 0
        days_counter = 0

        if week_this == 1: #THIS WEEK SEARCH

            html = urllib.request.urlopen(spreadsheet_url_this).read()
            data = []
            # Adapted from http://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
            from bs4 import BeautifulSoup


            soup = BeautifulSoup(str(html, 'utf-8'), 'html.parser')
            table = soup.find('table', attrs={'class':table_class})
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')

            for row in rows:
                col = row.find_all('td')
                cols = [ele.text.strip() for ele in col]
                data.append([ele for ele in cols]) # Get rid of empty values if ele
            #print (data)
            
            #days = [Names,Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday]
            #days = 
            #dates = 
            day = data[0]
            day.insert(0,'Name')
            date = data[1]
            
            day_s = [ele.strip() for ele in day]
            date_s = [ele.strip() for ele in date]
            """for dates in days_raw:
                for day in dates:
                    days_strip = [ele.text.strip() for ele in day]"""
            days = [ele for ele in day_s if ele]
            dates = [ele for ele in date_s if ele]
            dates.insert(0,' ')
            

            
            for row in data:
                broke = False
                for cell in row:#{
                    #print ("cell is " + cell)
                    cellcontent_raw = str(cell).lower().strip()
                    cellcontent_ascii = unicode_to_ascii(cellcontent_raw)
                    for beginning in row:#{ go back to the beginning of the row and compare all of the words
                        #print ("datapoint is " + beginning)
                        if keyword_raw in cellcontent_raw or keyword_ascii in cellcontent_ascii:
                            if counter < counter_max:
                                htmlmessage += _('<br />Row {}: ').format(counter+1)
                                for datapoint in row: #take the content of this entire row (so back to the beginning again) and add to msg
                                    #print ("datapoint the second time is " + datapoint)
                                    htmlmessage += _('<br>{0} {1}: {2}<br />').format(days[days_counter], dates[days_counter], datapoint)
                                    days_counter += 1
                                htmlmessage += '<br />'
                                days_counter = 0
                                broke = True
                                break  #prevent multiple subsequent cell matches appending identical rows                
                    #}

                    if broke:
                        counter +=1
                        break
                            
            if counter > counter_max:
                htmlmessage += _('<br />{0} rows found. Only returning first {1}.').format(counter, counter_max)
                if counter_max == 50:
                    htmlmessage += _('<br />Hint: Use <b>/bot lookup <{0} {1}</b> to view {0} rows').format(counter_max*2, keyword)

            if counter == 0:
                htmlmessage += _('No match found')

        if week_next == 1: #NEXT WEEK SEARCH

            html = urllib.request.urlopen(spreadsheet_url_next).read()
            data = []
            # Adapted from http://stackoverflow.com/questions/23377533/python-beautifulsoup-parsing-table
            from bs4 import BeautifulSoup


            soup = BeautifulSoup(str(html, 'utf-8'), 'html.parser')
            table = soup.find('table', attrs={'class':table_class})
            table_body = table.find('tbody')

            rows = table_body.find_all('tr')

            for row in rows:
                col = row.find_all('td')
                cols = [ele.text.strip() for ele in col]
                data.append([ele for ele in cols]) # Get rid of empty values if ele
            #print (data)
            
            #days = [Names,Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday]
            #days = 
            #dates = 
            day = data[0]
            day.insert(0,'Name')
            date = data[1]
            
            day_s = [ele.strip() for ele in day]
            date_s = [ele.strip() for ele in date]
            """for dates in days_raw:
                for day in dates:
                    days_strip = [ele.text.strip() for ele in day]"""
            days = [ele for ele in day_s if ele]
            dates = [ele for ele in date_s if ele]
            dates.insert(0,' ')
            

            
            for row in data:
                broke = False
                for cell in row:#{
                    #print ("cell is " + cell)
                    cellcontent_raw = str(cell).lower().strip()
                    cellcontent_ascii = unicode_to_ascii(cellcontent_raw)
                    for beginning in row:#{ go back to the beginning of the row and compare all of the words
                        #print ("datapoint is " + beginning)
                        if keyword_raw in cellcontent_raw or keyword_ascii in cellcontent_ascii:
                            if counter < counter_max:
                                htmlmessage += _('<br />Row {}: ').format(counter+1)
                                for datapoint in row: #take the content of this entire row (so back to the beginning again) and add to msg
                                    #print ("datapoint the second time is " + datapoint)
                                    htmlmessage += _('<br>{0} {1}: {2}<br />').format(days[days_counter], dates[days_counter], datapoint)
                                    days_counter += 1
                                htmlmessage += '<br />'
                                days_counter = 0
                                broke = True
                                break  #prevent multiple subsequent cell matches appending identical rows                
                    #}

                    if broke:
                        counter +=1
                        break
                            
            if counter > counter_max:
                htmlmessage += _('<br />{0} rows found. Only returning first {1}.').format(counter, counter_max)
                if counter_max == 50:
                    htmlmessage += _('<br />Hint: Use <b>/bot lookup <{0} {1}</b> to view {0} rows').format(counter_max*2, keyword)

            if counter == 0:
                htmlmessage += _('No match found')

    yield from bot.coro_send_message(event.conv, htmlmessage)
