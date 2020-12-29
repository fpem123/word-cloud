# word-cloud

This API make video title word cloud using youtuber channel url
This is used selenium and wordcloud module
When you enter channel url some part, this program crawling that channel and make word cloud image.

font: KBIZ 한마음고딕

## how to use

You can use API page, and need 1 parameter.

### ** Post parameter **

*** /find_youtuber ***

youtuber: This is youtuber channel name that you want.

 => exam: AI network or pewdiepew

result -> Channel name, some part of channel url.

*** /make_wordcloud ***

youtuber: This is youtuber part of channel url. That url can get /find_youtuber

 => exam: /channel/UCnyBeZ5iEdlKrAcfNbZ-wog or /user/pewdiepie

result -> Word cloud image

### ** With CLI **

#### /find_youtuber

curl -X POST "https://master-word-cloud-fpem123.endpoint.ainize.ai/word-cloud/find_youtuber" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "youtuber={youtuber}"

#### /make_wordcloud

curl -X POST "https://master-word-cloud-fpem123.endpoint.ainize.ai/word-cloud/make_wordcloud" -H "accept: images/*" -H "Content-Type: multipart/form-data" -F "youtuber={youtuber channel url}"

### ** With swagger **

Use API page: https://ainize.ai/fpem123/word-cloud?branch=master
