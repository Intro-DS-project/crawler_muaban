#!/bin/sh
current_date_time=$(date +'%Y-%m-%d_%H-%M-%S')
scrapy crawl muaban -O "/app/data/${current_date_time}_muaban_output.json"