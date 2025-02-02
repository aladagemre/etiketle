# -*- coding: utf-8 -*-
import csv
import datetime
import logging

from etiketle.posts.models import RedditPost

logger = logging.getLogger(__name__)


class RedditPostImporter:
    def __init__(self, dataset):
        self.dataset = dataset

    def start(self) -> int:
        """
        Starts the import process
        :return: the number of posts imported.
        """
        posts = []
        with open(self.dataset.file.path) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                created_at = datetime.datetime.strptime(row["created_utc"], "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=datetime.timezone.utc
                )
                post = RedditPost(
                    dataset=self.dataset,
                    created_at=created_at,
                    subreddit=row["subreddit"],
                    url=row["url"],
                    data=row,
                )
                posts.append(post)

            if posts:
                RedditPost.objects.bulk_create(posts)
                return len(posts)
            else:
                logger.error("No posts to import")
        return 0
