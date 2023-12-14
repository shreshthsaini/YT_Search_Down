# Search retrieval and video download from YouTube

This project is designed to search YouTube using a provided CSV file of keywords and download the returned list of videos using yt-dlp library. It automates the process of getting search results on Youtube with filter configuration and downloading videos with IDs.

## Prerequisites

Before running the code, make sure you have the following installed:

- Python 3.x
- yt-dlp
- pandas
- tqdm
- jsonschema 
- requests

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/shreshthsaini/YT_Search_Down.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Place your CSV file containing the search queries in the project directory.

2. Run the search script:
Given the large size of keyword csv files, we search in batches withing search script. Default `batch_size=10000`. 

    ```bash
    python yt-search_batches.py --csv_file sample_keywords.csv --extra_keyword " #shorts" --filter_criterion "CreativeCommons"

    ```

    Depending on different filter configuration, you modify your search results on YouTube.  
    Following filter_criterion are available:

            CC license videos = "CreativeCommons"
            HDR videos = "HDR"
            HDR videos under 4 mins. = "HDR_under4"
            CC license HDR videos = "CC_HDR"
            CC license 4K resolution HDR videos = "CC_HDR_4K"
            CC license HDR videos under 4 mins = "CC_HDR_under4"

    `NOTE`: you can add your own filter combinations by adding a new line your filter combination in Class `VideoFeatures` in `/youtube_search_python/youtubesearchpython/core/constants.py`. 

    - On YouTube, adjust your filters and search with random keyword 
        
        https://www.youtube.com/results?search_query=example&sp=EgcYA3AByAEB
    - Copy the key after `sp=`, and add to VideoFeature Class

            Eg: HDR_4K_4_20mins = 'EgcYA3AByAEB'


    Searched results will be saved in a csv file `./searched_csv/+filter_criterion+'_'+extra_keyword+'_'+csv_file_name+'_batch_no_'+'.csv'`

    <details>
        <summary> Sample Results</summary>

    ```json 
    {
        "result": [
            {
                "type": "video", 
                "id": "njX2bu-_Vw4", 
                "title": "2020 LG OLED l  The Black 4K HDR 60fps", 
                "publishedTime": "2 years ago", 
                "duration": "2:07", 
                "viewCount": {"text": "11,060,876 views", "short": "11M views"
                }, 
                "thumbnails": [
                    {
                                "url": "https://i.ytimg.com/vi/njX2bu-_Vw4/hq720.jpg?sqp=-oaymwEcCOgCEMoBSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDeu24J5UhhV1awrQfqOw5tSLF_BQ", 
                                "width": 360, 
                                "height": 202}, 
                                {"url": "https://i.ytimg.com/vi/njX2bu-_Vw4/hq720.jpg?sqp=-oaymwEcCNAFEJQDSFXyq4qpAw4IARUAAIhCGAFwAcABBg==&rs=AOn4CLDhlJAM2sch2I6HgklLa_1N8cAI1g", 
                                "width": 720, 
                                "height": 404
                    }
                ], 
                "richThumbnail": {
                                "url": "https://i.ytimg.com/an_webp/njX2bu-_Vw4/mqdefault_6s.webp?du=3000&sqp=CNL3jqAG&rs=AOn4CLB2WKnpxKtGEA4HCpLoMa7onKVueA", 
                                "width": 320, 
                                "height": 180
                }, 
                "descriptionSnippet": [
                    {
                        "text": "The Power of SELF-LIT PiXELS Meet all new LG OLED with 100 million of SELF-LIT PiXELS. When every pixel lights by itself,\xa0..."
                    }
                    ], 
                "channel": {
                            "name": "LG Global", 
                            "id": "UC2SIWgqcys7Gcb6JxsFTm1Q", 
                            "thumbnails": [
                                {
                                            "url": "https://yt3.ggpht.com/ZNlUENj7IntwhJbwX2UGPMjFIVTNI6EpkpHpxdStagp9UeCnbc-4t_q-yz1OHq2tuufWGu-5Ppk=s68-c-k-c0x00ffffff-no-rj", 
                                            "width": 68, 
                                            "height": 68
                                }
                            ], 
                            "link": "https://www.youtube.com/channel/UC2SIWgqcys7Gcb6JxsFTm1Q"
                }, 
                "accessibility": {
                                    "title": "2020 LG OLED l  The Black 4K HDR 60fps by LG Global 2 years ago 2 minutes, 7 seconds 11,060,876 views", 
                                    "duration": "2 minutes, 7 seconds"
                }, 
                "link": "https://www.youtube.com/watch?v=njX2bu-_Vw4", 
                "shelfTitle": None
                
                }
                ]
    }


    ```


    </details>




3. Run the download script:
    YouTube offers a variety of video formats and quality, our script tries to download the best quality video available.

    Two options are available for downloading videos: 
    - Download best video with MP4 format
    - Download best video with any format

    Saving format is: 
        `ID_duration.format`

    ```bash
    python download_YT_urls.py --csv_file ./searched_csv/CreativeCommons_#shorts_sample_keywords_batch_0.csv --save_folder ./Downloaded_videos/ --n_jobs 10

    ```

4. The downloaded videos will be saved in the `./Downloaded_videos` directory.

5. A `read_hdr_10bit.py` files is also provided in case the downloaded videos are in HDR-10.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## Acknowledgements
Authors thank the creators of `yt-dlp` 

## License

This project is licensed under the [MIT License](LICENSE).
