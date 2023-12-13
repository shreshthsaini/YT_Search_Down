import os
import sys
import pandas as pd
import numpy as np
from tqdm import tqdm
import argparse

import warnings
warnings.filterwarnings('ignore')

from youtube_search_python.youtubesearchpython.search import * 

#--------------------------------------------------------------*****--------------------------------------------------------------#
def verify_merge(df_temp, df, df_prev, keyword): 
    #now compare the IDs are unique or not
    for k in range(len(df_temp)):
        if df_temp['id'][k] in df['id'].values:
            print('ID already exists: ',df_temp['id'][k])
            df_temp.drop(k, inplace=True)
        #remove is exists in previously collected data/csv
        elif len(df_temp)!=0:
            if df_temp['id'][k] in df_prev:
                print('ID already exists in previous csv: ',df_temp['id'][k])
                df_temp.drop(k, inplace=True)    
        # adding keyword column
        df_temp['keyword'] = keyword

    return df_temp

def search_YT(csv_file, extra_keyword, batch_size, limit, filter_criterion, searched_csv_root='./searched_csv/'):
    
    # Create directory for saving csv file batches
    keyword_batch_root = searched_csv_root+csv_file.split("/")[-1].split(".")[0]
    print("Keywords Batch Files Directory: ", keyword_batch_root)
    os.makedirs(keyword_batch_root, exist_ok=True)

    # Read keywords from csv file
    keywords = list(pd.read_csv(csv_file, on_bad_lines='skip')['keyword'].values)
    # print keywords length
    print('Keywords length: ',len(keywords))

    """ 
        Check the previous generated csv files and remove searches if ID already exists
        NOTE: Checking previous search results. 
    """
    df_prev = []
    for i in os.listdir(searched_csv_root):
        if os.path.isfile(searched_csv_root+i):
            df_prev += pd.read_csv(searched_csv_root+i)['id'].values.to_list()

    """ 
        NOTE: Divide keywords in batches and save the csv file after each batch to avoid losing collected data due to long run time or system stalls
    """
    for b in tqdm(range(0,len(keywords),batch_size)):
        
        print('Current Batch: ',b/batch_size)
        batch_keywords = keywords[b:b+batch_size]

        # Save the batch of keywords to csv file; can be used to resume the search
        pd.DataFrame(batch_keywords).to_csv(keyword_batch_root+'/batch_'+ str(int(b/batch_size))+'.csv', index=False)

        # Empty dataframe with columns for storing search results
        df = pd.DataFrame(columns=['type', 'id', 'title', 'publishedTime', 'duration', 'viewCount', 'thumbnails', 'richThumbnail', 'descriptionSnippet', 'channel', 'accessibility', 'link', 'shelfTitle'])

        # Iterate over each keyword in the batch
        for keyword in batch_keywords:      
            print('Keyword: ',keyword)
            
            """ 
                Core search function
                return: search results in json format 
            """
            try: 
                # Using getattr to access the filter attribute
                selected_filter = getattr(VideoFeatures, filter_criterion)
                # Initialize search object
                search_HDR = CustomSearch(keyword+extra_keyword, selected_filter, limit = limit)
            except:
                print('Error occured: ',search_HDR.result())
                print("keyword: ",keyword)
                continue

            # Check if the IDs are unique or not before merging
            df_temp = pd.DataFrame(search_HDR.result()['result'])
            df_temp = verify_merge(df_temp, df, df_prev, keyword)

            # if dataframe lenght zero skip updating. 
            if len(df_temp) == 0:
                print('Length of the dataframe: ',len(df_temp))
                continue

            #print 1 title
            print('First result: ',search_HDR.result()['result'][0]['title'])

            #appending in the dataframe df 
            df = df.append(df_temp)

            #next set of 20 results with iteration
            for i in tqdm(range(1,limit//20)):
                try:
                    search_HDR.next()
                    df_temp = pd.DataFrame(search_HDR.result()['result'])
                except:
                    print('Error occured: ',search_HDR.result())
                    print("keyword: ",keyword)
                    continue
                    
                # Check if the IDs are unique or not
                df_temp = verify_merge(df_temp, df, df_prev, keyword)

                # if dataframe lenght zero break the loop 
                if len(df_temp) == 0:
                    print('Length of the dataframe: ',len(df_temp))
                    break

                # Merge the dataframes
                df = df.append(df_temp)
                #print('Next results: ',search_HDR.result()['result'][0]['title'])

        # Saving as csv file after each batch
        df.to_csv(searched_csv_root+filter_criterion+"_"+extra_keyword.split(" ")[-1]+"_"+csv_file.split(".")[0].split("/")[-1]+'_batch_'+str(int(b/batch_size))+'.csv', index=False)
        # print the csv length and first 5 rows
        print('CSV length: ',len(df))
        print(df.head())


#--------------------------------------------------------------*****--------------------------------------------------------------#
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv_file", help="Path to the CSV file")
    parser.add_argument("--extra_keyword", type=str, default="", help="Use this spaced keyword or hastag to impprove the searching. #shorts tend to return YT Shorts") # 
    parser.add_argument("--batch_size", type=int, default=10000, help="Batch size")
    parser.add_argument("--limit", type=int, default=10000, help="Irrespective of the limit, the results are always 20. Thus need to use next() to get the next 20 results and so on")
    parser.add_argument("--filter_criterion", default="CreativeCommons", help="Filter criterion")
    args = parser.parse_args()
    
    search_YT(args.csv_file, args.extra_keyword, args.batch_size, args.limit, args.filter_criterion)

#--------------------------------------------------------------*****--------------------------------------------------------------#
if __name__ == "__main__":
    main()


""""
IMPORTANT: 

For batchwise: check all batches of csv and drop duplicate ids as it was not handled in this batchwise code!!

"""
