# Creation Time and Published Time Are Not the Same: Estimating the Instagram Epoch

## Data

### IG_epoch_estimate.csv
The main dataset used for estimating the IG epoch. This contains data collected from 1000 shortcodes

* shortcode:
    The shortcode obtained from the Instagram post URL.
    
        Ex: URL - https://www.instagram.com/p/CGGOHDXhhK-/
    
        Shortcode - CGGOHDXhhK-
        
* media_id:
    The unique id assigned to each post by Instagram. This can be obtained from the JSON content.
 
        Ex: URL - https://www.instagram.com/p/CGGOHDXhhK-/    

        Media ID: 2415680307434230462
        
* creation_time (seconds wrt IG epoch):	
    Creation time of the ID calculated using the media_id/shortcode.
    
        1. Shortcode: CGGOHDXhhK-
        2. Media ID: 2415680307434230462
        3. Binary equivalent: 10000110000110001110000111000011010111100001100001001010111110
        4. Padding 64bits: 0010000110000110001110000111000011010111100001100001001010111110
        5. First 41 bits: 00100001100001100011100001110000110101111
        6. Converted back to decimal: 287971533231 milliseconds = 287971533.231 seconds        

* published_time (unix):	
    The published time of the post extracted from the JSON located in one of the <script> tags in the HTML body.

* published_time (utc):	
    The date-time obtained after converting the above unix time into UTC.
    
* epoch_estimate (utc):
    The estimated IG epoch values calculated using the creation time of the ID and the published time from the HTML.

        published_time: The value extracted from the HTML (taken_at_timestamp) which is the number of seconds from the UNIX epoch (say, Tp).
        creation_time: The value extracted from the shortcode/media ID which is the number of milliseconds from the  IG epoch (say, Tc).
        IG epoch = Tp - (Tc/1000) seconds


* is_multiple:
    Whether this post contains multiple media or not.   
    
        True: Multiple media post
        False: Single media post
        
* count:
    If it is a multiple media post, how many media items does it contain.
    
* is_video: 
    Is this an image or a  video?
    
        True: Single media video post
        False: Image (single or multiple media) 
        "Contains at least one video": A multiple media post which contains at least one video media item.
    
* vid_duration	
    The duration of the video.
    (The video durations are available for the single video posts only)
    
* delta:
    The difference between 2011-08-24T21:07:00Z and the date-time values in the IG epoch estimate column


### CGGOHDXhhK-.json
The JSON content  located in one of the <script> tags in the HTML body. This contains the published date-time (in Unix) of the IG post (https://www.instagram.com/p/CGGOHDXhhK-/).

### CKEYWF7gY4l.json
The JSON content of a multiple media post which contains an image and a video (https://www.instagram.com/p/CKEYWF7gY4l/).

## Code

### estimating_epoch.py

The code takes list of shortcodes as the input to extract the above mentioned data from instagram using the selenium webdriver. he epoch estimates are also computed in this same code.   

### calculate_delta.py

As the final step, the difference between 2011-08-24T21:07:00Z and the date-time values in the IG epoch estimate column is calculated using this code.

## Blog

This dataset is compiled as a part of the study conducted to study the discrepency between creation time of ID and publishing time of a post in Instagram.

### Link: https://ws-dl.blogspot.com/2021/02/2021-02-20-creation-time-and-published.html 
